"""
Milestone 5 — Grounded generation.

Ties the pipeline together (Retrieval -> Generation in the architecture diagram):

  1. retrieve() pulls the top-k most relevant chunks from ChromaDB.
  2. Those chunks are formatted into a numbered context block.
  3. Groq (llama-3.3-70b-versatile) answers using ONLY that context.
  4. The answer is returned with the de-duplicated source links it drew from.

The grounding instruction lives in SYSTEM_PROMPT: the model is told to answer
only from the provided documents and to refuse when they're insufficient.
"""

import os

from dotenv import load_dotenv
from groq import Groq

from embed import retrieve, SOURCES, DEFAULT_TOP_K

load_dotenv()

# --- Configuration ------------------------------------------------------------
LLM_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "Answer the question using only the information in the provided documents. "
    "If the documents don't contain enough information to answer, say "
    "'I don't have enough information on that.'"
)

# Phrase the model emits when the documents don't support an answer. Used to
# suppress source links on a refusal (citing sources for "I don't know" is
# misleading).
REFUSAL_MARKER = "don't have enough information"


# --- Groq client --------------------------------------------------------------
_client = None


def get_client():
    """Create (and cache) the Groq client, reading the key from the environment."""
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Copy .env.example to .env and add your "
                "key from https://console.groq.com"
            )
        _client = Groq(api_key=api_key)
    return _client


# --- Prompt assembly ----------------------------------------------------------
def build_context(hits):
    """Format retrieved chunks into a numbered context block for the prompt.

    Each block names its source so the model can attribute claims if it wants.
    """
    blocks = []
    for i, hit in enumerate(hits, start=1):
        name, _url = SOURCES.get(hit["source"], (hit["source"], None))
        blocks.append(f"[Document {i}] {name}\n{hit['text']}")
    return "\n\n".join(blocks)


def unique_sources(hits):
    """De-duplicate the retrieved hits' sources, preserving retrieval order.

    Returns a list of {"name", "url"} dicts — the links shown with the answer.
    """
    seen = set()
    sources = []
    for hit in hits:
        if hit["source"] in seen:
            continue
        seen.add(hit["source"])
        name, url = SOURCES.get(hit["source"], (hit["source"], None))
        sources.append({"name": name, "url": url})
    return sources


# --- Generation ---------------------------------------------------------------
def answer_question(question, top_k=DEFAULT_TOP_K):
    """Run the full RAG pipeline for one question.

    Returns a dict:
        {
            "question": <str>,
            "answer":   <str, grounded in the retrieved chunks>,
            "sources":  [{"name", "url"}, ...]  (empty if the model refused),
            "hits":     <raw retrieval hits, for inspection/eval>,
            "refused":  <bool>,
        }
    """
    hits = retrieve(question, top_k=top_k)
    context = build_context(hits)
    user_message = f"Documents:\n\n{context}\n\nQuestion: {question}"

    client = get_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0,  # deterministic — important for reproducible evaluation
    )
    answer = response.choices[0].message.content.strip()

    refused = REFUSAL_MARKER in answer.lower()
    # Don't attach source links to a refusal.
    sources = [] if refused else unique_sources(hits)

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "hits": hits,
        "refused": refused,
    }


if __name__ == "__main__":
    # Quick manual smoke test.
    result = answer_question("What is the course lottery like at Haverford?")
    print(result["answer"])
    print("\nSources:")
    for s in result["sources"]:
        print(f"  - {s['name']}: {s['url']}")

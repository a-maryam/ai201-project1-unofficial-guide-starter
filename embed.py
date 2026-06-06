"""
Milestone 4 — Embedding, vector store, and retrieval.

Implements the Retrieval Approach from planning.md and the middle of the
architecture diagram (Chunking -> Embedding -> Vector Store -> Retrieval):

  - Chunks come from ingest.py (load_documents + chunk_document).
  - Embedding model: all-MiniLM-L6-v2 via sentence-transformers.
  - Vector store: ChromaDB (persisted locally to chroma_db/).
  - Each chunk is stored with its metadata (source, chunk method, chunk index).
  - retrieve() embeds a query and returns the top-k most similar chunks.

Run this file directly to (re)build the index and run the evaluation queries:

    python embed.py
"""

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import load_documents, chunk_document

# --- Configuration (from planning.md "Retrieval Approach") --------------------
CHROMA_DIR = Path(__file__).parent / "chroma_db"   # gitignored local store
COLLECTION_NAME = "unofficial_guide"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"              # sentence-transformers
DEFAULT_TOP_K = 10                                 # raised from 5: the first-year
                                                   # course guidance ranked outside
                                                   # the top 5 (see Evaluation)

# The five evaluation questions from planning.md ("Evaluation Plan").
EVAL_QUESTIONS = [
    "What is CS240 about?",
    "What is Professor Wonacott like?",
    "What is the course lottery like at Haverford?",
    "What is the CS department like?",
    "What courses should a first-year student take to start CS, "
    "and are they difficult?",
]

# Distance above which a match is considered weak (cosine space). Used to avoid
# dressing up a low-relevance chunk with a confident-looking citation. See the
# 0.6-0.7 "weak match" guidance in the project notes.
WEAK_MATCH_THRESHOLD = 0.6

# Maps each document filename to (human-readable source name, URL), straight
# from the source table in README.md / planning.md. The numeric filename prefix
# matches the row number in that table. Used to turn a raw filename into a
# proper citation in generated answers.
SOURCES = {
    "1_haverford_lotteries.txt": (
        "Haverford Registrar — Lottery Guidelines",
        "https://www.haverford.edu/registrar/lotteries",
    ),
    "2_college_confidential.txt": (
        "College Confidential — Math/CS 4+1 with UPenn",
        "https://talk.collegeconfidential.com/t/math-computer-science-4-1-w-upenn/1869266",
    ),
    "3_rmp_wonacott.txt": (
        "RateMyProfessor — David Wonnacott",
        "https://www.ratemyprofessors.com/professor/752469",
    ),
    "4_rmp_prof_lindell.txt": (
        "RateMyProfessor — Steven Lindell",
        "https://www.ratemyprofessors.com/professor/2238783",
    ),
    "5_reddit_haverford_cs.txt": (
        "Reddit r/Pennsylvania — Is Haverford decent for CS?",
        "https://www.reddit.com/r/Pennsylvania/comments/10630z4/is_haverford_college_decent_for_comp_sci_looking/",
    ),
    "6_clerk_shortage_CS.txt": (
        "Haverford Clerk — Open Letter on CS Faculty Shortage",
        "https://haverfordclerk.com/open-letter-on-the-shortage-of-computer-science-faculty/",
    ),
    "7_rmp_nguyen.txt": (
        "RateMyProfessor — Dung Nguyen",
        "https://www.ratemyprofessors.com/professor/3122048",
    ),
    "8_rmp_dougherty.txt": (
        "RateMyProfessor — John Dougherty",
        "https://www.ratemyprofessors.com/professor/2349369",
    ),
    "9_rmp_friedler.txt": (
        "RateMyProfessor — Sorelle Friedler",
        "https://www.ratemyprofessors.com/professor/2041582",
    ),
    "10_reddit_cs_2.txt": (
        "Reddit r/Haverford — How is the CS & Math department?",
        "https://www.reddit.com/r/Haverford/comments/1kkygm5/how_is_the_computer_science_and_math_departments/",
    ),
    "11_haverford_cs_reqs.txt": (
        "Haverford CS — Major/Minor Requirements",
        "https://www.haverford.edu/academics/computer-science-major-minor-and-concentration",
    ),
    "12_catalog.txt": (
        "Haverford CS — Course Catalog",
        "https://www.haverford.edu/computer-science/courses/course-catalog",
    ),
}


# --- Embedding model ----------------------------------------------------------
_model = None


def get_embedding_model():
    """Load (and cache) the all-MiniLM-L6-v2 sentence-transformers model.

    The model is loaded lazily so that simply importing this module is cheap.
    """
    global _model
    if _model is None:
        print(f"Loading embedding model: {EMBED_MODEL_NAME} ...")
        _model = SentenceTransformer(EMBED_MODEL_NAME)
    return _model


def embed_texts(texts):
    """Embed a list of strings into a list of vectors (Python lists of floats)."""
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


# --- Vector store -------------------------------------------------------------
def get_collection():
    """Open (or create) the persistent ChromaDB collection.

    Uses cosine similarity so that retrieval distance reflects semantic
    closeness regardless of vector magnitude.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def get_chunks():
    """Load every document and chunk it (delegates to ingest.py).

    Returns a flat list of chunk dicts: {"source", "method", "chunk_index", "text"}.
    """
    chunks = []
    for doc in load_documents():
        chunks.extend(chunk_document(doc))
    return chunks


def build_index(reset=True):
    """Embed all chunks and store them in ChromaDB with their metadata.

    Args:
        reset: if True, drop any existing collection first so the index is
               rebuilt cleanly (avoids stale or duplicated chunks).

    Returns the number of chunks indexed.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass  # collection didn't exist yet — nothing to delete

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    chunks = get_chunks()
    print(f"Embedding {len(chunks)} chunks with {EMBED_MODEL_NAME} ...")

    documents = [c["text"] for c in chunks]
    embeddings = embed_texts(documents)

    # Metadata travels with each chunk so retrieval can attribute its sources.
    metadatas = [
        {
            "source": c["source"],
            "method": c["method"],
            "chunk_index": c["chunk_index"],
        }
        for c in chunks
    ]
    # Unique, stable id per chunk: filename + its index within that file.
    ids = [f"{c['source']}::{c['chunk_index']}" for c in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Indexed {collection.count()} chunks into '{COLLECTION_NAME}' "
          f"(stored at {CHROMA_DIR}).")
    return len(chunks)


# --- Retrieval ----------------------------------------------------------------
def retrieve(query, top_k=DEFAULT_TOP_K):
    """Retrieve the `top_k` chunks most similar to `query`.

    Embeds the query with the same model used for indexing, then asks ChromaDB
    for the nearest chunks by cosine distance.

    Returns a list of dicts (best match first):
        {
            "text":        <chunk text>,
            "source":      <originating filename>,
            "method":      <"fixed" | "paragraph">,
            "chunk_index": <int>,
            "distance":    <cosine distance; lower = more similar>,
        }
    """
    collection = get_collection()

    query_embedding = embed_texts([query])
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    # Chroma returns parallel lists nested one level deep (one per query).
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    hits = []
    for text, meta, distance in zip(documents, metadatas, distances):
        hits.append(
            {
                "text": text,
                "source": meta["source"],
                "method": meta["method"],
                "chunk_index": meta["chunk_index"],
                "distance": distance,
            }
        )
    return hits


def format_citation(hit, include_url=True):
    """Turn a retrieved hit into a human-readable citation string.

    Looks the hit's filename up in SOURCES to get a friendly source name and
    URL; falls back to the raw filename for any source not in the table. The
    chunk index is always included so the exact passage can be traced back.

    Example: "Haverford Registrar — Lottery Guidelines (chunk 8) — https://..."
    """
    name, url = SOURCES.get(hit["source"], (hit["source"], None))
    citation = f"{name} (chunk {hit['chunk_index']})"
    if include_url and url:
        citation += f" — {url}"
    return citation


# --- Main: build the index and run the evaluation queries ---------------------
def main():
    build_index(reset=True)

    for question in EVAL_QUESTIONS:
        hits = retrieve(question)
        weak = "  [!] weak top match" if hits[0]["distance"] > WEAK_MATCH_THRESHOLD else ""
        print(f"\nQuery: {question!r}{weak}\n")
        for rank, hit in enumerate(hits, start=1):
            preview = hit["text"].replace("\n", " ")[:160]
            print(f"  [{rank}] dist={hit['distance']:.3f}  {format_citation(hit)}")
            print(f"      {preview}...\n")


if __name__ == "__main__":
    main()

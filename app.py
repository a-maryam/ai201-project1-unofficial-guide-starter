"""
Milestone 5 — Query interface (Gradio web UI).

A minimal interface: type a question, get a grounded answer with its source
links. All retrieval + generation happens in generate.answer_question().

Run with:

    python app.py

then open the local URL it prints (default http://127.0.0.1:7860).
"""

import gradio as gr

from generate import answer_question

TITLE = "The Unofficial Guide — Haverford CS"
DESCRIPTION = (
    "Ask about CS courses, professors, the course lottery, and the department "
    "at Haverford. Answers are grounded only in the collected documents; the "
    "sources used are linked below each answer."
)

EXAMPLE_QUESTIONS = [
    "What is the course lottery like at Haverford?",
    "What is Professor Wonacott like?",
    "What is the CS department like?",
]


def format_sources(sources):
    """Render the source list as a Markdown bullet list of links."""
    if not sources:
        return ""
    lines = ["", "**Sources:**"]
    for s in sources:
        if s["url"]:
            lines.append(f"- [{s['name']}]({s['url']})")
        else:
            lines.append(f"- {s['name']}")
    return "\n".join(lines)


def respond(question):
    """Answer a question and return Markdown (answer + source links)."""
    if not question or not question.strip():
        return "Please type a question."

    result = answer_question(question)
    return result["answer"] + "\n" + format_sources(result["sources"])


demo = gr.Interface(
    fn=respond,
    inputs=gr.Textbox(
        lines=2,
        label="Your question",
        placeholder="e.g. What is the course lottery like at Haverford?",
    ),
    outputs=gr.Markdown(label="Answer"),
    title=TITLE,
    description=DESCRIPTION,
    examples=EXAMPLE_QUESTIONS,
    flagging_mode="never",
)


if __name__ == "__main__":
    demo.launch()

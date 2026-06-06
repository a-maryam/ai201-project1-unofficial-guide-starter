"""
End-to-end tests — runs all 5 evaluation questions from planning.md through the
full pipeline (retrieve -> Groq generation -> answer + sources) and checks the
results.

Run with:

    python test_e2e.py

Requires GROQ_API_KEY in .env and a built ChromaDB index (run `python embed.py`
first). Exits non-zero if any check fails.

The checks are deliberately lenient — exact LLM phrasing varies, so each
answerable question passes if ANY of its expected keywords appears. CS240 is the
known corpus gap (no H240 description exists), so it is expected to refuse.
"""

import sys

from generate import answer_question, REFUSAL_MARKER

# Per-question expectations.
#   keywords      -> at least one must appear in the answer (case-insensitive)
#   expect_refusal -> the model should say it lacks information
CASES = [
    {
        "question": "What is CS240 about?",
        "expect_refusal": True,  # no H240 description in the corpus
        "keywords": [],
    },
    {
        "question": "What is Professor Wonacott like?",
        "expect_refusal": False,
        "keywords": ["wonnacott", "wonacott", "explain", "passionate",
                     "friendly", "long", "lecture"],
    },
    {
        "question": "What is the course lottery like at Haverford?",
        "expect_refusal": False,
        "keywords": ["lottery", "register", "registrar", "waitlist", "enroll"],
    },
    {
        "question": "What is the CS department like?",
        "expect_refusal": False,
        "keywords": ["theoretical", "department", "supportive", "small",
                     "growing", "professor"],
    },
    {
        "question": "What courses should a first-year student take to start CS, "
                    "and are they difficult?",
        "expect_refusal": False,
        "keywords": ["intro", "105", "106", "107", "accelerated", "first"],
    },
]


def check_case(case):
    """Run one question and return (passed, list_of_problems)."""
    result = answer_question(case["question"])
    answer = result["answer"]
    problems = []

    # 1. Always: a non-empty answer comes back.
    if not answer.strip():
        problems.append("empty answer")

    refused = REFUSAL_MARKER in answer.lower()

    if case["expect_refusal"]:
        # 2a. Known corpus gap -> should refuse, and carry no source links.
        if not refused:
            problems.append("expected a refusal but got a substantive answer")
        if result["sources"]:
            problems.append("refusal should not list sources")
    else:
        # 2b. Answerable -> should not refuse, should cite sources, and should
        #     mention at least one expected keyword.
        if refused:
            problems.append("unexpected refusal")
        if not result["sources"]:
            problems.append("no sources returned")
        if not any(kw in answer.lower() for kw in case["keywords"]):
            problems.append(
                f"none of the expected keywords {case['keywords']} appeared"
            )

    return (not problems), problems, result


def main():
    passed = 0
    failed = 0

    for case in CASES:
        ok, problems, result = check_case(case)
        status = "PASS" if ok else "FAIL"
        print(f"\n[{status}] {case['question']}")
        print(f"  answer: {result['answer'][:200].strip()}"
              f"{'...' if len(result['answer']) > 200 else ''}")
        if result["sources"]:
            names = ", ".join(s["name"] for s in result["sources"])
            print(f"  sources: {names}")
        for p in problems:
            print(f"  - {p}")

        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed (of {len(CASES)})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

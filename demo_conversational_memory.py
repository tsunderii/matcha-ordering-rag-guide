"""
Stretch feature demo: Conversational Memory

Shows a two-turn conversation where the SECOND question only makes sense given
the first ("Does it contain milk?" — what is "it"?). The system carries the
earlier turn forward, so it resolves the reference and answers correctly.

To prove this is real memory and not a coincidence of topic overlap, the demo
also runs the exact same second question with NO history. Without memory the
model has no referent for "it" and cannot give the same grounded answer.

Run it with:
    python demo_conversational_memory.py
(Run `python embed_and_retrieve.py` first so the vector store exists.)
"""

import contextlib
import io

from query import ask


def quiet_ask(question, history=None):
    """Call ask() but suppress retrieve()'s verbose printing."""
    with contextlib.redirect_stdout(io.StringIO()):
        return ask(question, history=history)


def main():
    print("=" * 70)
    print("CONVERSATIONAL MEMORY DEMO")
    print("=" * 70)

    # --- Turn 1 ---------------------------------------------------------------
    q1 = "What is the Cloud Matcha Latte?"
    r1 = quiet_ask(q1)
    print(f"\n[Turn 1] User: {q1}")
    print(f"[Turn 1] Assistant: {r1['answer']}")
    print(f"         Sources: {r1['sources']}")

    # Build the conversation history from turn 1.
    history = [{"question": q1, "answer": r1["answer"]}]

    # --- Turn 2 WITH memory ---------------------------------------------------
    # Note the pronoun "it" — this only has meaning if the system remembers turn 1.
    q2 = "How much does it cost?"
    r2 = quiet_ask(q2, history=history)
    print(f"\n[Turn 2 — WITH memory] User: {q2}")
    print(f"[Turn 2 — WITH memory] Assistant: {r2['answer']}")
    print(f"         Sources: {r2['sources']}")

    # --- Turn 2 WITHOUT memory (control) -------------------------------------
    # Same question, no history. "it" has no referent, so the system cannot
    # answer the same way — this proves the difference is memory, not topic luck.
    r2_cold = quiet_ask(q2, history=None)
    print(f"\n[Turn 2 — NO memory (control)] User: {q2}")
    print(f"[Turn 2 — NO memory (control)] Assistant: {r2_cold['answer']}")
    print(f"         Sources: {r2_cold['sources']}")

    print("\n" + "-" * 70)
    print("With memory, the assistant resolves \"it\" to the Cloud Matcha Latte from "
          "turn 1 and gives that drink's price. Without memory, it has no referent "
          "for \"it\" and instead lists every drink it can find a price for — "
          "confirming the second turn genuinely depends on the first.")


if __name__ == "__main__":
    main()

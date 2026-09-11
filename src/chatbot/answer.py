# chatbot/answer.py

from src.chatbot.citations import collect_citations


def synthesize_answer(verified_paths, llm):
    """
    verified_paths: List[ReasoningPath]
    llm: callable(prompt) -> str
    """

    if not verified_paths:
        return {
            "answer": "I don’t know based on the available MetaKGP data.",
            "citations": []
        }

    # Pick the longest verified path (more evidence)
    best_path = max(verified_paths, key=lambda p: len(p.nodes))

    claims = "\n".join(
        f"- {n.claim}" for n in best_path.nodes
    )

    prompt = f"""
You are writing a final answer using VERIFIED facts only.

RULES:
- Use ONLY the facts below
- Do NOT add new information
- Do NOT infer missing details
- Keep the answer concise and factual

FACTS:
{claims}

Write a coherent answer.
"""

    answer = llm(prompt).strip()

    citations = collect_citations(best_path)

    return {
        "answer": answer,
        "citations": citations
    }

# verification/hallucination_hunter.py

def hallucination_hunter(path, llm):
    combined_claims = "\n".join(
        f"- {n.claim}" for n in path.nodes
    )

    combined_text = "\n".join(
        n.text for n in path.nodes
    )

    prompt = f"""
You are checking for hallucinations.

CLAIMS:
{combined_claims}

SOURCE TEXT:
{combined_text}

Question:
Do the claims introduce ANY detail, name, date,
or relationship NOT present in the source text?

Answer ONLY:
NO_HALLUCINATION or HALLUCINATION
"""

    response = llm(prompt).strip().upper()
    return response == "NO_HALLUCINATION"

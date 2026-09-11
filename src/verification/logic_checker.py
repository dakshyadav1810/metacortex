# verification/logic_checker.py

def logic_checker(path, llm):
    if len(path.nodes) < 2:
        return True

    premises = "\n".join(
        f"- {n.claim}" for n in path.nodes[:-1]
    )
    conclusion = path.nodes[-1].claim

    prompt = f"""
You are evaluating logical consistency.

PREMISES:
{premises}

CONCLUSION:
{conclusion}

Does the conclusion logically follow from the premises?

Answer ONLY:
YES or NO
"""

    response = llm(prompt).strip().upper()
    return response == "YES"

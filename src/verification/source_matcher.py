# verification/source_matcher.py

def source_matcher(path, llm):
    """
    path: ReasoningPath
    llm: callable(prompt) -> str
    """

    for node in path.nodes:
        prompt = f"""
Check whether the following claim is explicitly supported
by the provided source text.

CLAIM:
"{node.claim}"

SOURCE TEXT:
"{node.text}"

Answer ONLY with one word:
YES or NO
"""
        response = llm(prompt).strip().upper()
        if response != "YES":
            return False

    return True

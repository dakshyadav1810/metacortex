# reasoning/extract_claims.py
import uuid
from typing import List

from src.reasoning.node import FactNode


def extract_claims_from_chunk(chunk: dict, llm):
    """
    chunk = {
        chunk_id, title, url, text
    }
    llm: callable(prompt) -> str
    """

    prompt = f"""
You are extracting factual claims from a wiki document.

RULES:
- Only extract claims explicitly stated in the text
- Do NOT infer or add new information
- Each claim must be independently verifiable from the text
- Return short, atomic statements

TEXT:
\"\"\"
{chunk['text']}
\"\"\"

Return claims as a bullet list.
"""

    response = llm(prompt)

    claims = []
    for line in response.split("\n"):
        line = line.strip("-• ").strip()
        if len(line) < 20:
            continue

        node = FactNode(
            node_id=str(uuid.uuid4()),
            claim=line,
            chunk_id=chunk["chunk_id"],
            title=chunk["title"],
            url=chunk["url"],
            text=chunk["text"]
        )
        claims.append(node)

    return claims

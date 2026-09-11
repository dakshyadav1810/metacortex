# reasoning/node.py
from dataclasses import dataclass


@dataclass
class FactNode:
    node_id: str
    claim: str
    chunk_id: str
    title: str
    url: str
    text: str

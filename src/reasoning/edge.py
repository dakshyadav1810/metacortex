# reasoning/edge.py
from dataclasses import dataclass


@dataclass
class Edge:
    source_id: str
    target_id: str
    relation: str

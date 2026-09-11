# reasoning/graph_builder.py
from collections import defaultdict
from typing import List

from src.reasoning.edge import Edge
from src.reasoning.node import FactNode


def build_graph(nodes: List[FactNode]):
    edges = []

    # Index nodes by title and chunk
    by_title = defaultdict(list)
    by_chunk = defaultdict(list)

    for node in nodes:
        by_title[node.title].append(node)
        by_chunk[node.chunk_id].append(node)

    # Rule 1: same page
    for title, group in by_title.items():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                edges.append(
                    Edge(
                        source_id=group[i].node_id,
                        target_id=group[j].node_id,
                        relation="same_page"
                    )
                )

    # Rule 2: same chunk
    for chunk, group in by_chunk.items():
        if len(group) > 1:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    edges.append(
                        Edge(
                            source_id=group[i].node_id,
                            target_id=group[j].node_id,
                            relation="same_chunk"
                        )
                    )

    # Rule 3: keyword overlap (VERY conservative)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a = nodes[i]
            b = nodes[j]

            words_a = set(a.claim.lower().split())
            words_b = set(b.claim.lower().split())

            overlap = words_a & words_b

            if len(overlap) >= 3:
                edges.append(
                    Edge(
                        source_id=a.node_id,
                        target_id=b.node_id,
                        relation="keyword_overlap"
                    )
                )

    return edges

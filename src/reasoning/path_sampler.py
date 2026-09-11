# reasoning/path_sampler.py
from collections import defaultdict
from typing import List

from src.reasoning.node import FactNode
from src.reasoning.edge import Edge


class ReasoningPath:
    def __init__(self, nodes: List[FactNode], relations: List[str]):
        self.nodes = nodes
        self.relations = relations

    def to_text(self):
        return " → ".join(n.claim for n in self.nodes)


def build_adjacency(edges: List[Edge]):
    graph = defaultdict(list)
    for e in edges:
        graph[e.source_id].append((e.target_id, e.relation))
        graph[e.target_id].append((e.source_id, e.relation))
    return graph


def sample_paths(nodes: List[FactNode],
                 edges: List[Edge],
                 max_depth: int = 3,
                 max_paths: int = 10):

    node_map = {n.node_id: n for n in nodes}
    graph = build_adjacency(edges)

    paths = []

    def dfs(current_id, visited, path_nodes, path_rels):
        if len(paths) >= max_paths:
            return

        if len(path_nodes) > 1:
            paths.append(
                ReasoningPath(
                    nodes=list(path_nodes),
                    relations=list(path_rels)
                )
            )

        if len(path_nodes) == max_depth:
            return

        for next_id, rel in graph.get(current_id, []):
            if next_id in visited:
                continue

            visited.add(next_id)
            dfs(
                next_id,
                visited,
                path_nodes + [node_map[next_id]],
                path_rels + [rel]
            )
            visited.remove(next_id)

    for node in nodes:
        dfs(
            node.node_id,
            visited={node.node_id},
            path_nodes=[node],
            path_rels=[]
        )

        if len(paths) >= max_paths:
            break

    return paths

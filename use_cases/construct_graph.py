import asyncio
import time
from typing import List, Tuple

from domain.graph import Graph
from domain.node import Node


async def sample_func(t):
    t = t or 1
    await asyncio.sleep(t * 0.1)

    return t


def create_graph_from_directional_edges(edges: List[Tuple[int, int]]):
    def _add_node(graph: Graph, node_id: int):
        if not graph.is_existed_node(node_id):
            graph.add_node(Node(id=node_id, func=sample_func))

    graph = Graph()

    for from_id, dest_id in edges:
        _add_node(graph, from_id)
        _add_node(graph, dest_id)

        graph.add_edge(from_id, dest_id)

    return graph

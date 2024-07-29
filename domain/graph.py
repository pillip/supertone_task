from dataclasses import dataclass, field
from typing import Dict

from .node import Node


@dataclass
class Graph:
    nodes: Dict[int, Node] = field(default_factory=dict)

    def is_existed_node(self, node_id: int) -> bool:
        return node_id in self.nodes

    def add_node(self, node: Node):
        if self.is_existed_node(node.id):
            raise Exception(f"Node {node.id} already exists")

        self.nodes[node.id] = node

    def add_edge(self, from_id: int, dest_id: int):
        if not self.is_existed_node(from_id):
            raise Exception(f"Node {from_id} does not exist")

        if not self.is_existed_node(dest_id):
            raise Exception(f"Node {dest_id} does not exist")

        self.nodes[from_id].add_edge(self.nodes[dest_id])

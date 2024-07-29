from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


class NodeStatus(Enum):
    PENDING = 0
    EXECUTING = 1
    EXECUTED = 2


@dataclass
class Node:
    id: int
    incoming_edge: Optional["Node"] = None
    outgoing_edges: list["Node"] = field(default_factory=list)
    func: Callable[[any], any] = None
    input: Optional[any] = None
    result: Optional[any] = None
    status: NodeStatus = NodeStatus.PENDING

    def add_edge(self, node: "Node"):
        self.outgoing_edges.append(node)
        node.incoming_edge = self

    def can_execute(self) -> bool:
        return (
            not self.incoming_edge
            or self.incoming_edge.status == NodeStatus.EXECUTED
        ) and self.status == NodeStatus.PENDING

    async def execute(self):
        try:
            if self.can_execute():
                self.status = NodeStatus.EXECUTING

                self.input = (
                    self.incoming_edge.result if self.incoming_edge else None
                )
                self.result = await self.func(self.input)

                self.status = NodeStatus.EXECUTED
            else:
                raise Exception("Cannot execute node")
        except Exception as e:
            raise Exception(f"Error executing node {self.id}: {e}")

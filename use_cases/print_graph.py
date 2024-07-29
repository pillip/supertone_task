import asyncio
from typing import List

from domain.graph import Graph
from domain.node import Node, NodeStatus


def print_graph(graph: Graph):
    def dfs(node: Node, visited: set, depth: int = 0):
        visited.add(node.id)
        print(f"{node.id:^4}", end="")

        first_child = True
        for dest_node in node.outgoing_edges:
            if dest_node.id not in visited:
                if first_child:
                    print(" --> ", end="")
                    first_child = False
                else:
                    print(
                        "\n" + "    " * (depth + 1) + "     " * depth, end=""
                    )

                    print(" \-> ", end="")

                dfs(dest_node, visited, depth + 1)

    visited = set()
    for node_id, node in graph.nodes.items():
        if node_id not in visited:
            dfs(node, visited)
            print("\n", end="")


async def print_execution_order(graph: Graph):
    async def _execute_node(
        queue: asyncio.Queue, order: List[str], tasks: List[asyncio.Task]
    ):
        while not queue.empty():
            current_node = await queue.get()

            order.append(str(current_node.id))

            task = asyncio.create_task(current_node.execute())
            tasks.append((current_node, task))

    async def _resolve_completed_tasks(
        tasks: List[asyncio.Task], queue: asyncio.Queue
    ):
        done, _ = await asyncio.wait(
            [task for _, task in tasks], return_when=asyncio.FIRST_COMPLETED
        )

        for done_task in done:
            for current_node, task in tasks:
                if task == done_task:
                    tasks.remove((current_node, task))

                    for neighbor in current_node.outgoing_edges:
                        if neighbor.can_execute():
                            await queue.put(neighbor)

                    break

    for node in graph.nodes.values():
        node.status = NodeStatus.PENDING

    queue = asyncio.Queue()
    tasks = []
    order = []

    for node in graph.nodes.values():
        if node.can_execute():
            await queue.put(node)

    while not queue.empty() or tasks:
        await _execute_node(queue, order, tasks)
        await _resolve_completed_tasks(tasks, queue)

    print("Execution order: ", " -> ".join(order))

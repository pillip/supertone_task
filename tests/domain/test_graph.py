import pytest

from domain.graph import Graph
from domain.node import Node, NodeStatus


def test_graph_initialization():
    graph = Graph()
    assert graph.nodes == {}


def test_add_node():
    async def sample_func(input):
        return input

    graph = Graph()
    node = Node(id=1, func=sample_func)

    graph.add_node(node)

    assert graph.is_existed_node(1) is True
    assert graph.nodes[1] == node


def test_add_existing_node():
    async def sample_func(input):
        return input

    graph = Graph()
    node = Node(id=1, func=sample_func)

    graph.add_node(node)

    with pytest.raises(Exception, match="Node 1 already exists"):
        graph.add_node(node)


def test_is_existed_node():
    async def sample_func(input):
        return input

    graph = Graph()
    node = Node(id=1, func=sample_func)

    graph.add_node(node)

    assert graph.is_existed_node(1) is True
    assert graph.is_existed_node(2) is False


def test_add_edge():
    async def sample_func(input):
        return input

    graph = Graph()
    node1 = Node(id=1, func=sample_func)
    node2 = Node(id=2, func=sample_func)

    graph.add_node(node1)
    graph.add_node(node2)

    graph.add_edge(1, 2)

    assert node2.incoming_edge == node1
    assert node1.outgoing_edges == [node2]


def test_add_edge_from_nonexistent_node():
    async def sample_func(input):
        return input

    graph = Graph()
    node2 = Node(id=2, func=sample_func)

    graph.add_node(node2)

    with pytest.raises(Exception, match="Node 1 does not exist"):
        graph.add_edge(1, 2)


def test_add_edge_to_nonexistent_node():
    async def sample_func(input):
        return input

    graph = Graph()
    node1 = Node(id=1, func=sample_func)

    graph.add_node(node1)

    with pytest.raises(Exception, match="Node 2 does not exist"):
        graph.add_edge(1, 2)


@pytest.mark.asyncio
async def test_execute_graph():
    async def sample_func(input):
        return input * 2 if input else 1

    graph = Graph()
    node1 = Node(id=1, func=sample_func)
    node2 = Node(id=2, func=sample_func)
    node3 = Node(id=3, func=sample_func)

    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)

    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    await node1.execute()
    assert node1.status == NodeStatus.EXECUTED
    assert node1.result == 1

    await node2.execute()
    assert node2.status == NodeStatus.EXECUTED
    assert node2.result == 2

    await node3.execute()
    assert node3.status == NodeStatus.EXECUTED
    assert node3.result == 4

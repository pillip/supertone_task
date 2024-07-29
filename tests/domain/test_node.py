import pytest

from domain.node import Node, NodeStatus


def test_node_init():
    async def sample_func(x):
        return x

    node = Node(id=1, func=sample_func)

    assert node.id == 1
    assert node.func == sample_func
    assert node.incoming_edge is None
    assert node.outgoing_edges == []
    assert node.input is None
    assert node.result is None
    assert node.status == NodeStatus.PENDING


@pytest.mark.asyncio
async def test_node_execution_without_incoming_edge():
    async def sample_func(input):
        return input * 2 if input else 1

    node = Node(id=1, func=sample_func)

    assert node.can_execute() is True

    await node.execute()

    assert node.status == NodeStatus.EXECUTED
    assert node.result == 1


def test_add_edge():
    async def sample_func(input):
        return input

    node1 = Node(id=1, func=sample_func)
    node2 = Node(id=2, func=sample_func)

    node1.add_edge(node2)

    assert node2.incoming_edge == node1
    assert node1.outgoing_edges == [node2]


@pytest.mark.asyncio
async def test_node_execution_with_incoming_edge():
    async def sample_func(input):
        return input * 2 if input else 1

    incoming_node = Node(id=0, func=sample_func)
    node = Node(id=1, func=sample_func)

    incoming_node.add_edge(node)

    assert node.can_execute() is False

    await incoming_node.execute()
    assert incoming_node.status == NodeStatus.EXECUTED
    assert incoming_node.result == 1

    assert node.can_execute() is True

    await node.execute()

    assert node.status == NodeStatus.EXECUTED
    assert node.result == 2


@pytest.mark.asyncio
async def test_node_execution_with_pending_incoming_edge():
    async def sample_func(input):
        return input * 2 if input else 1

    incoming_node = Node(id=0, func=sample_func)
    node = Node(id=1, func=sample_func)

    incoming_node.add_edge(node)

    with pytest.raises(Exception, match="Cannot execute node"):
        await node.execute()


@pytest.mark.asyncio
async def test_node_execution_with_error():
    async def faulty_func(input):
        raise RuntimeError("Function error")

    node = Node(id=1, func=faulty_func)

    with pytest.raises(
        Exception, match="Error executing node 1: Function error"
    ):
        await node.execute()

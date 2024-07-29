import asyncio

import pytest

from domain.graph import Graph
from domain.node import Node, NodeStatus
from use_cases.construct_graph import create_graph_from_directional_edges


def test_empty_edge_list():
    edges = []
    graph = create_graph_from_directional_edges(edges)
    assert len(graph.nodes) == 0


def test_single_edge():
    edges = [(1, 2)]
    graph = create_graph_from_directional_edges(edges)

    assert len(graph.nodes) == 2
    assert graph.is_existed_node(1)
    assert graph.is_existed_node(2)
    assert graph.nodes[1].outgoing_edges[0].id == 2
    assert graph.nodes[2].incoming_edge.id == 1


def test_multiple_edges():
    edges = [(1, 2), (2, 3), (3, 4)]
    graph = create_graph_from_directional_edges(edges)

    assert len(graph.nodes) == 4
    assert all(graph.is_existed_node(id) for id in range(1, 5))
    assert graph.nodes[2].outgoing_edges[0].id == 3
    assert graph.nodes[1].outgoing_edges[0].id == 2
    assert graph.nodes[3].outgoing_edges[0].id == 4


@pytest.fixture
def graph_with_edges():
    edges = [(1, 2), (2, 3), (3, 4)]
    return create_graph_from_directional_edges(edges)


@pytest.mark.asyncio
async def test_node_functionality(graph_with_edges):
    node = graph_with_edges.nodes[1]
    result = await node.func(1)
    assert result == 1

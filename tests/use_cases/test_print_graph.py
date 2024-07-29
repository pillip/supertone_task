import pytest

from domain.graph import Graph
from domain.node import Node
from use_cases.construct_graph import create_graph_from_directional_edges
from use_cases.print_graph import print_execution_order, print_graph


def test_print_simple_graph(capsys):
    graph = Graph()
    graph = create_graph_from_directional_edges([(1, 2), (1, 3), (2, 4)])

    print_graph(graph)

    captured = capsys.readouterr()
    expected_output = " 1   -->  2   -->  4  \n     \->  3  \n"
    assert captured.out == expected_output


@pytest.mark.asyncio
async def test_execute_order_simple_graph(capsys):
    graph = Graph()
    graph = create_graph_from_directional_edges([(1, 2), (1, 3), (2, 4)])

    await print_execution_order(graph)

    captured = capsys.readouterr()
    expected_outputs = [
        "Execution order:  1 -> 2 -> 3 -> 4\n",
        "Execution order:  1 -> 3 -> 2 -> 4\n",
    ]

    assert captured.out in expected_outputs

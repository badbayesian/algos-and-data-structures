import pytest
import graph

N = 10


def test_build_complete_graph():
    g = graph.Graph()
    for i in range(N):
        g.add_node({i: 0})

    for i in range(N):
        for j in range(N):
            if i != j:
                g.add_edge(i, j)

    h = graph.complete(N)
    assert g == h


def test_reverse_on_complete():
    g = graph.complete(N)
    h = g.reverse()
    assert g == h


def test_remove_all_nodes():
    g = graph.complete(N)
    h = graph.Graph()
    for i in range(N):
        g.remove_node(i)

    assert g == h


def test_remove_all_edges():
    g = graph.complete(N)
    for i in range(N):
        for j in range(N):
            g.remove_edge(i, j)

    h = graph.Graph()
    for i in range(N):
        h.add_node({i: 0})

    assert g == h


if __name__ == "__main__":
    test_remove_all_edges()

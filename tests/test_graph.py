import pytest
import graph

N = 10


def test_build_complete_graph():
    g = graph.Graph()
    for i in range(N):
        g.add_node({i: 0})

    print(g)
    for i in range(N):
        for j in range(N):
            if i != j:
                g.add_edge(i, j)

    h = graph.complete(N)
    assert g == h


def test_add():
    g = graph.Graph()
    h = graph.Graph()
    i = graph.Graph()

    g.add_node({0: 0})
    i.add_node({0: 0})

    h.add_node({1: 10})
    i.add_node({1: 10})

    print("g", g)
    print("h", h)
    print("i", i)
    print("sum", g + h)
    assert g + h == i


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
            if i != j:
                g.remove_edge(i, j)

    h = graph.Graph()
    for i in range(N):
        h.add_node({i: 0})

    assert g == h


if __name__ == "__main__":
    test_add()

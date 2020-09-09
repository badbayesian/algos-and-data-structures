import pytest
import graph


def test_wikipedia_dijkstra():
    g = graph.Graph("simple")
    g.add_edge(1, 2, 7)
    g.add_edge(1, 3, 9)
    g.add_edge(1, 6, 11)
    g.add_edge(2, 3, 10)
    g.add_edge(2, 4, 15)
    g.add_edge(3, 6, 2)
    g.add_edge(3, 4, 11)
    g.add_edge(6, 5, 9)
    g.add_edge(4, 5, 6)
    dist, prev = g.dijkstra(1)
    assert dist[5] == 20

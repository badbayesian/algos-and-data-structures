"""Graph"""
from __future__ import annotations
from typing import Dict, Any
from collections import defaultdict, Counter
from itertools import chain
from graph.search import SearchMixin


class Graph(SearchMixin):
    """Graph data structure with building methods.

    Potential graph types include simple and weighted.
    Nodes are stored in a dict.
    Edges are stored in nested dictionaries."""

    def __init__(self, graph_type: str = "weighted") -> None:
        possible_graphs = ["simple", "weighted"]
        if graph_type not in possible_graphs:
            raise TypeError(
                f"{graph_type} is not a valid graph type. Use {possible_graphs}."
            )

        self.nodes = {}
        self.edges = defaultdict(dict)
        self.graph_type = graph_type

    def __repr__(self) -> str:
        if self.graph_type == "simple":
            nodes = str([node for node in self.nodes.keys()]) + "\n"
            edges = "".join(
                [
                    f"{k}: {[e for e in v.keys()]}\n"
                    for (k, v) in self.edges.items()
                ]
            )
        elif self.graph_type == "weighted":
            nodes = "".join(
                [
                    f"{node}: {weight}\n"
                    for (node, weight) in self.nodes.items()
                ]
            )
            edges = "".join([f"{k}: {v}\n" for (k, v) in self.edges.items()])
        return f"Nodes:\n{nodes}\nEdges:\n{edges}"

    def __eq__(self, other: Graph) -> bool:
        if self.nodes != other.nodes:
            return False
        return self.edges == other.edges

    def __len__(self) -> int:
        return len(self.nodes)

    def __add__(self, other: Graph, verbose=True) -> Graph:
        """Combines graphs and adds weights of nodes and edges."""
        if verbose and (
            self.graph_type == "simple" or other.graph_type == "simple"
        ):
            raise TypeError("Use and for combining simple graphs.")

        new_graph = Graph(self.graph_type)
        new_graph.nodes = {
            k: self.nodes.get(k, 0) + other.nodes.get(k, 0)
            for k in set(self.nodes) | set(other.nodes)
        }

        for node, edge in chain(self.edges.items(), other.edges.items()):
            new_graph.edges[node] = {
                k: self.edges[node].get(k, 0) + other.edges[node].get(k, 0)
                for k in set(self.edges[node]) | set(other.edges[node])
            }
        return new_graph

    __radd__ = __add__

    def __and__(self, other: Graph) -> Graph:
        new_graph = Graph(self.graph_type)
        new_graph.nodes = {**self.nodes, **other.nodes}
        for node, edge in chain(other.edges.items(), self.edges.items()):
            new_graph.edges[node].update(edge)
        return new_graph

    __rand__ = __and__

    def __or__(self, other: Graph) -> Graph:
        raise NotImplementedError

    def __xor__(self, other: Graph) -> Graph:
        raise NotImplementedError

    def __sub__(self, other: Graph) -> Graph:
        """Subtract edges from self as defined by other."""
        ##TODO b inits all of a edges as a side effect
        new_graph = Graph(self.graph_type)
        new_graph.nodes = self.nodes
        for node_a, edge in self.edges.items():
            for node_b, weight in edge.items():
                if node_b not in other.edges[node_a]:
                    new_graph.edges[node_a][node_b] = weight
                else:
                    new_graph.edges[node_a] = {}

        return new_graph

    __rsub__ = __sub__

    def add_node(self, node: Dict) -> None:
        """Add node to graph."""
        self.nodes.update(node)
        _ = [self.edges[k].update() for k in node]

    def add_edge(
        self, node_a, node_b, weight=1, both_directions=False
    ) -> None:
        """Add edges to existing nodes in graph."""
        if node_a not in self.nodes:
            self.nodes[node_a] = 0
            self.edges[node_a] = {}
        if node_b not in self.nodes:
            self.nodes[node_b] = 0
            self.edges[node_b] = {}

        self.edges[node_a][node_b] = weight
        if self.graph_type == "weighted" and both_directions:
            self.edges[node_b][node_a] = weight

    def remove_node(self, node: Any) -> None:
        """Removes node from graph."""
        no_node = self.nodes.pop(node, True)
        if no_node:
            return

        self.edges.pop(node)

        for node_a, edge in self.edges.items():
            edge.pop(node)

    def remove_edge(
        self, node_a: Any, node_b: Any, both_directions: bool = False
    ) -> None:
        """Remove edge(s) from graph."""
        if not both_directions:
            self.edges[node_a].pop(node_b)

    def update_node_weight(self, node, new_weight) -> None:
        """Update node weight"""
        self.nodes[node] = new_weight

    def update_edge_weight(self, node_a, node_b, new_weight) -> None:
        """Updates edge weight."""
        self.edges[node_a][node_b] = new_weight

    def __reversed__(self) -> Graph:
        """Returns a copy that is the reverse graph."""
        r_graph = Graph(self.graph_type)
        for node_a, edge in self.edges.items():
            r_graph.add_node({node_a: self.nodes[node_a]})
            for node_b, weight in edge.items():
                r_graph.edges[node_b][node_a] = weight
        return r_graph

    def __contains__(self, query: Any) -> bool:
        raise NotImplementedError

    def complement(self) -> Graph:
        complete_graph = complete(len(self))
        return complete_graph - self

    __invert__ = complement


def complete(size: int, graph_type="weighted") -> Graph:
    """Creates complete graph."""
    graph = Graph(graph_type)
    if size == 1:
        graph.add_node({0: 0})
        return graph
    _ = [
        graph.add_edge(a, b)
        for a in range(size)
        for b in range(size)
        if a != b
    ]
    return graph

"""Graph"""
from __future__ import annotations
from typing import Dict
from collections import defaultdict
from graph.search import SearchMixin


class Graph(SearchMixin):
    """Graph data structure with building methods.

    With weighted nodes and edges (defaults 0 and 1 repectively).
    Edges stored in dictionaries."""

    def __init__(self, graph_type: str = "weighted") -> None:
        self.nodes = {}
        self.edges = defaultdict(dict)

        possible_graphs = ["simple", "weighted"]
        if graph_type not in possible_graphs:
            raise TypeError(
                f"{graph_type} is not a valid graph type. Use {possible_graphs}."
            )
        self.graph_type = graph_type

    def __repr__(self) -> str:
        nodes = "".join(
            [f"{node}: {weight}\n" for (node, weight) in self.nodes.items()]
        )
        output = f"Nodes:\n{nodes}\nEdges:\n"
        edges = "".join([f"{k}: {v}\n" for (k, v) in self.edges.items()])
        return output + edges

    def __eq__(self, other: Graph) -> bool:
        if self.nodes != other.nodes:
            return False
        return self.edges == other.edges

    def __len__(self) -> int:
        return len(self.nodes)

    def __and__(self, other: Graph, verbose: bool = False) -> Graph:
        """Adds."""
        new_graph = Graph(self.graph_type)
        new_graph.nodes = {**self.nodes, **other.nodes}
        for node, edge in self.edges.items():
            new_graph.edges[node] = edge

        for node, edge in other.edges.items():
            new_graph.edges[node] = edge

        return new_graph

    def __add__(self, other: Graph) -> Graph:
        return self.__and__(other)

    def __sub__(self, other: Graph) -> Graph:
        """Subtract edges from self as defined by other."""
        ##TODO b inits all of a edges as a side effect
        new_graph = Graph(self.graph_type)
        new_graph.nodes = self.nodes
        for node_a, edge in self.edges.items():
            for node_b, weight in edge.items():
                if node_b not in other.edges[node_a]:
                    new_graph.edges[node_a][node_b] = weight

        return new_graph

    def add_node(self, node: Dict) -> None:
        """Add node to graph."""
        self.nodes.update(node)
        _ = [self.edges[k].update() for k in node]

    def add_edge(self, node_a, node_b, weight_a=1) -> None:
        """Add edges to existing nodes in graph."""
        if node_a not in self.nodes:
            self.nodes[node_a] = 0
        if node_b not in self.nodes:
            self.nodes[node_b] = 0

        self.edges[node_a][node_b] = weight_a

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

    def reverse(self) -> Graph:
        """Returns a copy that is the reverse graph."""
        r_graph = Graph(self.graph_type)
        for node_a, edge in self.edges.items():
            r_graph.add_node({node_a: self.nodes[node_a]})
            for node_b, weight in edge.items():
                r_graph.edges[node_b][node_a] = weight
        return r_graph

    def complement(self) -> Graph:
        complete_graph = complete(len(self))
        return complete_graph - self


def complete(size: int, graph_type="weighted") -> Graph:
    """Creates complete graph."""
    graph = Graph(graph_type)
    _ = [
        graph.add_edge(a, b)
        for a in range(size)
        for b in range(size)
        if a != b
    ]
    return graph

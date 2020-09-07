"""Collection of search algorithms for Graphs. Built as Mixins."""
import heapq
from math import inf
from typing import Dict, Any


class SearchMixin:
    """Collection of search algorithms for Graph class."""

    def dijkstra(self, source):
        """Full dijkstra from a source.

        Assumes no negative cycles."""
        heap = []
        dist = {source: 0}
        prev = {}
        for node in self.nodes:
            if node != source:
                dist[node] = inf
                prev[node] = None
            heapq.heappush(heap, (dist[node], node))

        while heap:
            current_distance, node = heapq.heappop(heap)
            if current_distance > dist[node]:
                continue

            for neighbor, weight in self.edges[node].items():
                new_distance = current_distance + weight

                if new_distance < dist[neighbor]:
                    dist[neighbor] = new_distance
                    prev[neighbor] = node
                    heapq.heappush(heap, (new_distance, neighbor))

        return dist, prev

    def bellman_ford(self, source):
        dist = {source: 0}
        prev = {}
        for node in self.nodes:
            if node != source:
                dist[node] = inf
                prev[node] = None

        for node_a, edge in self.edges.items():
            for node_b, weight in edge:
                if dist[node_a] + weight < dist[node_b]:
                    dist[node_b] = dist[node_a] + weight
                    prev[node_b] = node_a

        for node_a, edge in self.edges.items():
            for node_b, weight in edge:
                if dist[node_a] + weight < dist[node_b]:
                    raise "Graph contains negative-weight cycle."

        return dist, prev

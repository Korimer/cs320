# pyright: basic

from collections import Counter
from copy import deepcopy
from typing import Optional

from edgegraph import *


class PalindromeTraversal:

    def __init__(self, graph: GraphEL) -> None:
        self.graph: GraphEL = graph
        self.verticies: list[VertexEL] = graph.vertices()
        vertexvalues = [edge.head().get_value() for edge in graph.edges()]
        self.vremaining: Counter = Counter(vertexvalues)
        self.visited: set[EdgeEL] = set()
        self.curroute: list[EdgeEL] = []
        self.palindromes: list[tuple[int, ...]] = []

    def getAllPalindromes(self) -> list[tuple[int, ...]]:
        for vert in self.verticies:
            self._visit(vert)
        return self.palindromes

    def _visit(self, vert: VertexEL) -> None:
        self.vremaining.subtract([vert])

        if self.isPalindrome():
            edgevals = [edge.get_value() for edge in self.curroute]
            self.palindromes.append(tuple(edgevals))

        unvisited_connections = [
            v_adjacent for v_adjacent in self.graph.incident(vert)
            if v_adjacent not in self.visited
        ]

        # valid_followups = self.canCreatePalindromeWith()
        for adjacent in unvisited_connections:
            adj1, adj2 = adjacent.ends()
            nextvert = adj1 if vert == adj2 else adj2
            # if valid_followups is None or adjacent.get_value() in valid_followups:
            self.visited.add(adjacent)
            self.curroute.append(adjacent)
            self._visit(nextvert)
            self.curroute.pop()
            self.visited.remove(adjacent)

        self.vremaining.update([vert])

    def isPalindrome(self) -> bool:
        if len(self.curroute) < 3:
            return False

        edgevals = [edge.get_value() for edge in self.curroute]

        return edgevals == edgevals[::-1]

    def canCreatePalindromeWith(self) -> Optional[set]:
        return set()

def pld_graph(graph: Optional[GraphEL]) -> list[tuple]:
    if graph is None:
        raise ValueError("Bad graph")
    return PalindromeTraversal(graph).getAllPalindromes()

# pyright: basic

from collections import Counter
from copy import deepcopy
from typing import Optional

from edgegraph import *


class PalindromeTraversal:

    def __init__(self, graph: GraphEL) -> None:
        self.graph: GraphEL = graph
        self.verticies: list[VertexEL] = graph.vertices()
        vertexvalues = [edge.tail().get_value() for edge in graph.edges()]
        self.vremaining: Counter = Counter(vertexvalues)
        self.visited: set[EdgeEL] = set()
        self.curroute: list[EdgeEL] = []
        self.palindromes: list[list] = []


    def _visit(self, vert: VertexEL) -> None:
        self.vremaining.subtract([vert])

        if self.isPalindrome():
            self.palindromes.append(self.curroute)

        unvisited_connections = [
            v_adjacent for v_adjacent in self.graph.outgoing(vert)
            if v_adjacent not in self.visited
        ]

        valid_followups = self.canCreatePalindromeWith()
        for adjacent in unvisited_connections:
            if valid_followups is None or adjacent.get_value() in valid_followups:
                self._visit(adjacent)

        self.vremaining.update([vert])

    def isPalindrome(self) -> bool:
        if len(self.curroute) < 3:
            return False

        for i in range(len(self.curroute) // 2):
            if self.curroute[i] != self.curroute[i * -1]:
                return False

        return True

    def canCreatePalindromeWith(self) -> Optional[set]:
        return set()




def pld_graph(graph: GraphEL) -> list[tuple[int,...]]:
    return []


# pyright: basic

from collections import deque
import edgegraph


def bfs(graph: edgegraph.GraphEL, start: edgegraph.VertexEL) -> list:

    if graph is None or start is None:
        raise ValueError("Invalid graph or vertex")

    if start.name not in graph._vertices:
        return []

    visited = set()
    tovisit = deque()
    searchresults = []

    tovisit.append(start)
    visited.add(start)

    while len(tovisit) != 0:
        searchresults.append(tuple(tovisit))

        connections = set()
        ordered_connections = deque()
        while len(tovisit) != 0:
            nextnode = tovisit.popleft()

            all_connections = graph.adjacent(nextnode)

            for connectednode in all_connections:
                if connectednode not in connections and connectednode not in visited:
                    visited.add(connectednode)
                    connections.add(connectednode)
                    ordered_connections.append(connectednode)
            
        tovisit = ordered_connections
                    
    return searchresults

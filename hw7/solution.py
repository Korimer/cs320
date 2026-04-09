# pyright: basic

from queue import Queue
import edgegraph


def bfs(graph: edgegraph.GraphEL, start: edgegraph.VertexEL) -> list:
    visited = set()
    tovisit = Queue()
    searchresults = []

    tovisit.put(start)

    while not tovisit.empty():
        connections = set()
        ordered_connections = Queue()
        while not tovisit.empty():
            nextnode = tovisit.get()
            if nextnode in visited:
                continue
            visited.add(nextnode)
            searchresults.append(nextnode)

            all_connections = graph.adjacent(nextnode)

            for connectednode in all_connections:
                if connectednode not in connections and connectednode not in visited:
                    connections.add(connectednode)
                    ordered_connections.put(connectednode)
        
        tovisit = ordered_connections

                    
    return searchresults

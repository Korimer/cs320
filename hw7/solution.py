# pyright: basic

import edgegraph

def bfs(graph: edgegraph.GraphEL, start: edgegraph.VertexEL) -> list:
    visited = set()
    tovisit = {start}
    next = set()

    while len(tovisit) != 0:
        for nodename in tovisit:
            pass
        tovisit = next
    return []

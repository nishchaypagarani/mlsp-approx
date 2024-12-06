# Implements a simplified LP from the flow-based model paper
import copy
import pulp
from Graph import Graph

# node i and its adjacent vertices (tau in paper notation)
def node_and_adj(graph: Graph, i: int):
    if not (0 <= i <= graph.numberOfEdges):
        raise Exception(f"{i} not a vertex of graph")
    out = [i]
    for (u, v) in graph.graphBiDirection:
        if   u == i:
            out.append(v)
    return out

# given root r, finds a solution that may represent an optimal directed spanning
# tree at that root
def rooted_LP(graph: Graph, r: int):
    if not (0 <= r < graph.numberOfNodes):
        raise Exception(f"{r} not a vertex of graph")
    # Construct graph
    G = copy.deepcopy(graph)
    t = G.add_node()
    for i in range(G.numberOfNodes):
        if i != r and i != t:
            G.add_edge((i, t))
    G.print_gv_bi(include_bi=True)
    # TODO: construct LP from graph


def test_rooted_LP():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    a.print_gv_bi(include_bi=True)
    rooted_LP(a, 0)


if __name__ == "__main__":
    test_rooted_LP()
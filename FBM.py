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
        if u == i:
            out.append(v)
    return out

# given root r, finds a solution that may represent an optimal directed spanning
# tree at that root
def Rooted_LP(graph: Graph, r: int):
    if not (0 <= r < graph.numberOfNodes):
        raise Exception(f"{r} not a vertex of graph")
    # Construct graph
    G = copy.deepcopy(graph)
    t = G.add_node()
    for i in range(G.numberOfNodes):
        if i != r and i != t:
            G.add_edge((i, t))
    
    # TODO: construct LP from graph

    

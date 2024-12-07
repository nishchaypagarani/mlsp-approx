# Implements a simplified LP from the flow-based model paper
import copy
import json
import pulp
from Graph import Graph

# node i and its adjacent vertices (gamma in paper notation)
def node_and_adj(graph: Graph, i: int):
    if not (0 <= i <= graph.numberOfNodes):
        raise Exception(f"{i} not a vertex of graph")
    # probably faster way to do this lol
    # out = [i]
    out = []
    for j in graph.graph[i]:
        out.append(j)
    return out

# given root r, finds a solution that may represent an optimal directed spanning
# tree at that root
def rooted_LP(graph: Graph, r: int):
    if not (0 <= r < graph.numberOfNodes):
        raise Exception(f"{r} not a vertex of graph")
    # Construct graph
    # G = copy.deepcopy(graph)
    n = graph.numberOfNodes
    G = Graph(n+1)
    # explicitly add bidirectional edges
    for u in range(n):
        for v in graph.graphBiDirection[u]:
            G.add_edge((u, v))
            # G.add_edge((v, u))
    t = n
    # t = G.add_node()
    # Add artificial arcs (edges to terminal)
    for i in range(G.numberOfNodes):
        if i != r and i != t:
            G.add_edge((i, t))
    G.print_gv(dir=True)
    # Define the LP Problem
    mlst_lp = pulp.LpProblem("MLST", pulp.LpMaximize)
    # Define the integer variables - one per each edge from non-root node to
    # sink 
    int_var_inds = []
    for i in range(graph.numberOfNodes):
        if i != r and i != t:
            int_var_inds.append((i, t))
    # Has Constraint Eq. 6 - vars in {0, 1}
    int_vars = pulp.LpVariable.dicts("ints", int_var_inds,
                                    lowBound=0, upBound=1,
                                    cat=pulp.LpInteger)
    # Can also try LpBinary to see if it makes a difference
    S = pulp.lpSum(int_vars)
    # Make S the objective function
    mlst_lp += S
    # Define the real variables - one for each edge not connecting to terminal
    real_var_inds = []
    for i in range(n):
        for j in G.graph[i]:
            real_var_inds.append((i, j))
    # Has Constraint Eq. 5 - flow must be > 0 and < 2n-2
    real_vars = pulp.LpVariable.dicts("reals", real_var_inds,
                                     lowBound=0, upBound=(2*n-2),
                                     cat=pulp.LpContinuous)
    # Constraint Eq. 2 - root's outgoing flow
    LHS = []
    for j in node_and_adj(G, r):
        LHS.append(real_vars[(r, j)])
    mlst_lp += (pulp.lpSum(LHS) - S == (n - 1))
    # Constraint Eq. 3 - each vertex (other than root and terminal) consuming 1
    # unit flow
    for i in range(graph.numberOfNodes):
        if i != r and i != t:
            LHS_1 = [real_vars[(j, i)] for j in node_and_adj(G, i) if j != t]
            # LHS_2 = []
            # for k in node_and_adj(G, i):
            #     if k != r:
            #         if k == t:
            #             LHS_2.append(int_vars[(i, k)])
            #         else:
            #             LHS_2.append(real_vars[(i, k)])
                
            LHS_2 = [real_vars[(i, k)] for k in node_and_adj(G, i) if k != r]
            mlst_lp += (pulp.lpSum(LHS_1) - pulp.lpSum(LHS_2) == 1)
    # Constraint Eq. 4 - sinks can only send flows to terminal
    for i in range(graph.numberOfNodes):
        if i != r and i != t:
            LHS_1 = [real_vars[(i, j)] for j in node_and_adj(G, i) if j != r and j != t]
            LHS = pulp.lpSum(LHS_1) + 2*(n-2)*real_vars[(i, t)]
            mlst_lp += (LHS <= 2*(n-2))
            # mlst_lp += (LHS >= 0)
    
    print(mlst_lp.variables())
    # print(json.dumps(mlst_lp.to_dict(), indent=2))
    mlst_lp.solve()

    # for i in range(n):
    #     if i != r:
    #         print(f"f_{i},t = {int_vars[(i, t)].value()}")
    for E in real_vars.keys():
        print(f"f_{E}: {real_vars[E].value()}")
    # TODO: add second args(?) of readable label for above constraints like in
    # TODO: start off at vertex in feasible region - a tree
    # wedding.py
     

    
    

def test_rooted_LP():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    m_a = Graph(17, [(1, 2), (2, 3), (1, 4), (4, 6), (6, 0), (0, 7), (7, 5), (5, 3),
                     (1, 8), (2, 9), (14, 0), (16, 7), (4, 11),
                     (8, 11), (9, 12), (10, 13), (8, 9), (9, 10), (12, 15), (14, 15), (15, 16)])
    print("Input graph")
    m_a.print_gv()
    print("Constructed graph for LP:")
    rooted_LP(m_a, 0)


if __name__ == "__main__":
    test_rooted_LP()
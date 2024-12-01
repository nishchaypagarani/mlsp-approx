from Graph import Graph
import copy

def calculate_number_of_leaves(tree: Graph):
    deg = [0]*tree.numberOfNodes
    for u,edges in tree.graph.items():
        for v in edges:
            deg[u]+=1
            deg[v]+=1
    cnt=0
    for i in deg:
        if i==1:
            cnt+=1
    return cnt

# TODO: brute force
def find_st_bf(graph: Graph, remainingGraph: Graph, fixedGraph: Graph):
    maxLeaves=-1
    bestGraph = None
    for u,edges in remainingGraph.graph.items():
        for v in edges:
            remainingGraph.remove_edge((u,v))
            fixedGraph.add_edge((u,v))
            if fixedGraph.numberOfEdges == (graph.numberOfNodes - 1):
                if graph.st_checker(fixedGraph):
                    leaves = calculate_number_of_leaves(fixedGraph)
                    if leaves>maxLeaves:
                        maxLeaves = leaves
                        bestGraph = copy.deepcopy(fixedGraph)
            elif fixedGraph.numberOfEdges < (graph.numberOfNodes - 1):
                (leaves, graphRes) = find_st_bf(graph, remainingGraph, fixedGraph)
                if leaves>maxLeaves:
                        maxLeaves = leaves
                        bestGraph = copy.deepcopy(graphRes)
            fixedGraph.remove_edge((u,v))
            remainingGraph.add_edge((u,v))
    return (maxLeaves, bestGraph)

# TODO: ensembler


def test_calculate_number_of_leaves():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    a.print_gv()
    a_tree=Graph(5, [(0,1), (1,2), (2,3), (2,4)])
    a_tree2=Graph(5, [(0,1), (1,2), (1,3), (2,4)])
    a_tree3=Graph(5, [(0,1), (1,2), (1,3)])
    a_tree.print_gv_bi()
    print(calculate_number_of_leaves(a_tree)) 
    a_tree2.print_gv_bi()
    print(calculate_number_of_leaves(a_tree2)) 
    a_tree3.print_gv_bi()
    print(calculate_number_of_leaves(a_tree3)) 
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    b.print_gv_bi()
    b_tree = Graph(6, [(0,1), (1,2),(1,3),(2,4),(4,5)])
    b_tree2 = Graph(6, [(0,1), (1,2),(1,3),(2,4),(3,5)])
    b_tree3 = Graph(6, [(0,1), (1,2),(2,3),(2,4),(3,5)])
    b_tree4 = Graph(6, [(0,1), (1,2),(2,3),(3,4),(4,5)])
    b_tree5 = Graph(6, [(0,1), (1,2),(2,3),(2,4),(3,5),(5,4)])
    b_tree.print_gv_bi()
    print(calculate_number_of_leaves(b_tree)) 
    b_tree2.print_gv_bi()
    print(calculate_number_of_leaves(b_tree2)) 
    b_tree3.print_gv_bi()
    print(calculate_number_of_leaves(b_tree3)) 
    b_tree4.print_gv_bi()
    print(calculate_number_of_leaves(b_tree4)) 
    b_tree5.print_gv_bi()
    print(calculate_number_of_leaves(b_tree5)) 
    c_tree = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5)])
    c_tree.print_gv_bi()
    print(calculate_number_of_leaves(c_tree)) 

def test_brute_force():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    c = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5)])
    d = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5),(1,2),(2,3),(3,4),(4,5),(2,4),(1,4),(1,5)])
    print("\n\n\n Test case A: ")
    a.print_gv_bi()
    (a_leaves, a_tree_opt) = find_st_bf(a,copy.deepcopy(a),Graph(a.numberOfNodes, []))
    print(a_leaves)
    a_tree_opt.print_gv_bi()
    print("\n\n\n Test case B: ")
    b.print_gv_bi()
    (b_leaves, b_tree_opt) = find_st_bf(b,copy.deepcopy(b),Graph(b.numberOfNodes, []))
    print(b_leaves)
    b_tree_opt.print_gv_bi()
    print("\n\n\n Test case C: ")
    c.print_gv_bi()
    (c_leaves, c_tree_opt) = find_st_bf(c,copy.deepcopy(c),Graph(c.numberOfNodes, []))
    print(c_leaves)
    c_tree_opt.print_gv_bi()
    print("\n\n\n Test case D: ")
    d.print_gv_bi()
    (d_leaves, d_tree_opt) = find_st_bf(d,copy.deepcopy(d),Graph(d.numberOfNodes, []))
    print(d_leaves)
    d_tree_opt.print_gv_bi()

if __name__ == "__main__":
    test_brute_force()
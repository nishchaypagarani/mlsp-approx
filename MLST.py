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

def find_st_greedy_ds(graph: Graph):
    stGraph = Graph(graph.numberOfNodes, [])
    ds = set()
    lvs = set()
    maxNeighbors = len(graph.graphBiDirection[0])
    maxNeighborNode = 0
    for v in graph.graphBiDirection[0]:
        if len(graph.graphBiDirection[v])>maxNeighbors:
            maxNeighbors = len(graph.graphBiDirection[v])
            maxNeighborNode = v
    ds.add(maxNeighborNode)
    for v in graph.graphBiDirection[maxNeighborNode]:
        lvs.add(v)
        stGraph.add_edge((maxNeighborNode,v))
    while ds.union(lvs)!=graph.nodes:
        maxNeighbors = -1
        maxNeighborNode = -1
        ss = ds.union(lvs)        
        for v in lvs:
            validNeighborCnt = 0
            for j in graph.graphBiDirection[v]:
                if j not in ss:
                    validNeighborCnt+=1
            if validNeighborCnt>maxNeighbors:
                maxNeighbors = validNeighborCnt
                maxNeighborNode = v
        lvs.remove(maxNeighborNode)
        ds.add(maxNeighborNode)
        for j in graph.graphBiDirection[maxNeighborNode]:
            if j not in ss:
                lvs.add(j)
                stGraph.add_edge((maxNeighborNode,j))
    leaves = calculate_number_of_leaves(stGraph)
    return (leaves,stGraph)
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
    e = Graph(2, [(0,1)])
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
    print("\n\n\n Test case E: ")
    e.print_gv_bi()
    (e_leaves, e_tree_opt) = find_st_bf(e,copy.deepcopy(e),Graph(e.numberOfNodes, []))
    print(e_leaves)
    e_tree_opt.print_gv_bi()

def test_st_greedy_ds():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    c = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5)])
    d = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5),(1,2),(2,3),(3,4),(4,5),(2,4),(1,4),(1,5)])
    e = Graph(2, [(0,1)])
    print("\n\n\n Test case A: ")
    a.print_gv_bi()
    (a_leaves, a_tree_opt) = find_st_greedy_ds(a)
    print(a_leaves)
    a_tree_opt.print_gv_bi()
    print("\n\n\n Test case B: ")
    b.print_gv_bi()
    (b_leaves, b_tree_opt) = find_st_greedy_ds(b)
    print(b_leaves)
    b_tree_opt.print_gv_bi()
    print("\n\n\n Test case C: ")
    c.print_gv_bi()
    (c_leaves, c_tree_opt) = find_st_greedy_ds(c)
    print(c_leaves)
    c_tree_opt.print_gv_bi()
    print("\n\n\n Test case D: ")
    d.print_gv_bi()
    (d_leaves, d_tree_opt) = find_st_greedy_ds(d)
    print(d_leaves)
    d_tree_opt.print_gv_bi()
    print("\n\n\n Test case E: ")
    e.print_gv_bi()
    find_st_greedy_ds(e)
    (e_leaves, e_tree_opt) = find_st_greedy_ds(e)
    print(e_leaves)
    e_tree_opt.print_gv_bi()
    # outputs = [(a_tree_opt, a_leaves),(b_tree_opt, b_leaves),(c_tree_opt, c_leaves),(d_tree_opt, d_leaves),(e_tree_opt, e_leaves)]
    # gen_output("hard.out", outputs)
    # outputs = [(a, 5),(b, 6),(c, 6),(d, 6),(e, 2)]
    # gen_output("hard.out", outputs)
def get_input(filename):
    graphs: list[Graph] = list()
    with open(filename) as my_file:
        n = int(my_file.readline())
        for i in range(n):
            current_graph = list(map(int, my_file.readline().split()))
            current_edges = []
            for j in range(current_graph[1]):
                new_edge = list(map(int, my_file.readline().split()))
                current_edges.append(new_edge)
            graphs.append(Graph(current_graph[0], current_edges))
        # for i in graphs:
        #     i.print_gv_bi()
    return graphs
def gen_output(filename, outputs: list[tuple[Graph, int]]):
    with open(filename, "w") as my_file:
        for o in outputs:
            graph: Graph = o[0]
            leaves = o[1]
            my_file.write(f"{leaves} {graph.numberOfEdges}\n")
            for v,edges in graph.graphBiDirection.items():
                for u in sorted(edges):
                    if u>v:
                        my_file.write(f"{v} {u}\n")
        
if __name__ == "__main__":
    # test_st_greedy_ds()
    get_input("hard.in")
import copy
import time
from Graph import Graph
from FBM import rooted_LP

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

def flow_leaves(int_flow_vals, eps=1e-5):
    # add 1 to account for root
    leaves = 1
    for arc in int_flow_vals.keys():
        if abs(int_flow_vals[arc] - 1.0) < eps:
            leaves += 1
    return leaves

# given original graph, construct a tree on it
def flow_to_tree(graph: Graph, real_flow_vals, threshold=1e-5):
    T = Graph(graph.numberOfNodes)
    for edge in real_flow_vals.keys():
        # make sure not adding duplicate edges
        if real_flow_vals[edge] - 0.0 > threshold:
            T.add_edge(edge, allow_duplicates=False)
    return T

# Runs a linear program  on a graph to find a MLST tree
# graph: Graph (assumed connected)
# time_limit: int (seconds)
# baseline: int (number of leaves - only returns tree if
# number of leaves greater than this)
def find_st_LP(graph: Graph, time_limit=60, baseline=0):
    # TODO: check FBM's leaves value matches calculate_number_of_leaves(tree)
    best_leaves = 0
    best_tree = {}
    start = time.perf_counter()
    with open('temp', 'w+') as fo:
        for r in range(graph.numberOfNodes):
            print(f"Running LP on root {r}/{graph.numberOfNodes}")
            int_flow_vals, real_flow_vals = rooted_LP(graph, r)
            # leaves = flow_leaves(int_flow_vals)
            tree = flow_to_tree(graph, real_flow_vals)
            leaves = calculate_number_of_leaves(tree)
            fo.write(str(int_flow_vals) + "\n")
            fo.write(str(real_flow_vals) + "\n")
            fo.write("Leaves: " + str(leaves) + "\n")
            if leaves > best_leaves:
                # best_tree = flow_to_tree(graph, real_flow_vals)
                best_tree = tree
                best_leaves = leaves
            now = time.perf_counter()
            if now - start >= time_limit:
                    break
    if best_leaves > baseline:
        print("Tree found better than baseline!")
        return (best_leaves, best_tree)
    else:
        print("No tree found better than baseline.")
        return None, None


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

def solve_and_compare(graphs: list[Graph]):
    for i in range(len(graphs)):
        print(f"Graph {i}: \n")
        if graphs[i].is_connected():
            graphs[i].print_gv_bi()
            (bf_leaves, bf_tree) = find_st_bf(graphs[i], copy.deepcopy(graphs[i]), Graph(graphs[i].numberOfNodes))
            (greedy_leaves, greedy_tree) = find_st_greedy_ds(graphs[i])
            print(f"Brute force solution leaves: {bf_leaves}")
            print(f"Greedy Solution Leaves: {greedy_leaves}")
            print("Brute force Tree: \n")
            bf_tree.print_gv_bi()
            print("Greedy Tree: \n")
            greedy_tree.print_gv_bi()
        else:
            print("Graph not connected")
        print("\n\n\n")


# Takes list of solvers - "LP", "bf", "greedy"
def solve_and_compare_LP(graphs: list[Graph], solvers):
    with open("log.txt", 'w') as fo, open("log2.txt", 'w') as fo2:
        for i in range(len(graphs)):
            fo.write(f"Graph {i}: \n")
            fo2.write(f"Graph {i}: \n")
            fo2.write(f"Input Graph: \n")
            fo2.write(graphs[i].ret_gv_bi())
            if graphs[i].is_connected():
                if "greedy" in solvers:
                    (greedy_leaves, greedy_tree) = find_st_greedy_ds(graphs[i])
                    fo.write(f"Greedy Solution Leaves: {greedy_leaves}\n")
                    fo2.write("Greedy Tree: \n")
                    fo2.write(greedy_tree.ret_gv_bi())
                if "bf" in solvers:
                    (bf_leaves, bf_tree) = find_st_bf(graphs[i], copy.deepcopy(graphs[i]), Graph(graphs[i].numberOfNodes))
                    fo.write(f"Brute force solution leaves: {bf_leaves}\n")
                    fo2.write("Brute force Tree: \n")
                    fo2.write(bf_tree.ret_gv_bi())
                if "lp" in solvers:
                    (lp_leaves, lp_tree) = find_st_LP(graphs[i])
                    fo.write(f"LP Solution leaves: {lp_leaves}\n")
                    fo2.write("LP Tree: \n")
                    fo2.write(lp_tree.ret_gv_bi())
            else:
                fo.write("Graph not connected")
                fo2.write("Graph not connected")
            print("\n\n\n")

def test_st_LP(fname_out = None):
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    c = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5)])
    d = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5),(1,2),(2,3),(3,4),(4,5),(2,4),(1,4),(1,5)])
    e = Graph(2, [(0,1)])
    graphs = {"a":a, "b":b, "c":c, "d":d, "e":e}
    if fname_out is not None:
        with open(fname_out, 'w') as fo:
            for name, graph in graphs.items():
                fo.write(f"Test case: {name} \n")
                fo.write(graph.ret_gv_bi())
                (leaves, tree_opt) = find_st_LP(graph)
                fo.write(f"Leaves: {leaves}\n")
                fo.write(tree_opt.ret_gv_bi())
                fo.write(f"Output is a tree: {graph.st_checker(tree_opt)}\n\n")
    # print("\n\n\n Test case B: ")
    # b.print_gv_bi()
    # (b_leaves, b_tree_opt) = find_st_LP(b)
    # print(b_leaves)
    # b_tree_opt.print_gv_bi()
    # print("\n\n\n Test case C: ")
    # c.print_gv_bi()
    # (c_leaves, c_tree_opt) = find_st_LP(c)
    # print(c_leaves)
    # c_tree_opt.print_gv_bi()
    # print("\n\n\n Test case D: ")
    # d.print_gv_bi()
    # (d_leaves, d_tree_opt) = find_st_LP(d)
    # print(d_leaves)
    # d_tree_opt.print_gv_bi()
    # print("\n\n\n Test case E: ")
    # e.print_gv_bi()
    # find_st_LP(e)
    # (e_leaves, e_tree_opt) = find_st_LP(e)
    # print(e_leaves)
    # e_tree_opt.print_gv_bi()
    # solve_and_compare_LP([a, b, c, d, e], ["bf", "greedy", "lp"])


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

def gen_hard_in(filename, additionalGraphs: list[Graph] = []):
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    c = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5)])
    d = Graph(6,[(0,1),(0,2),(0,3),(0,4),(0,5),(1,2),(2,3),(3,4),(4,5),(2,4),(1,4),(1,5)])
    e = Graph(2, [(0,1)])
    m_a = Graph(17, [(1, 2), (2, 3), (1, 4), (4, 6), (6, 0), (0, 7), (7, 5), (5, 3),
                     (1, 8), (2, 9), (14, 0), (16, 7), (4, 11),
                     (8, 11), (9, 12), (10, 13), (8, 9), (9, 10), (12, 15), (14, 15), (15, 16)])
    m_b = Graph(10, [(0, 1), (0, 4), (0, 3), (1, 4), (1, 2), (2, 4), (2, 5), (3, 6), (3, 7), (4, 7),
                     (5, 8), (6, 9), (7, 8), (7, 9)])
    # m_b.print_gv() 

    f = Graph(6,[(0,1), (0,2),(1,3),(2,3),(2,4),(4,5),(3,5)])
    g = Graph(8,[(0,1),(0,7),(0,5),(1,2),(2,3),(2,4),(2,5),(3,4),(4,5),(4,6),(5,6),(6,7),(1,7),(2,7)])
    testcases = [a,b,c,d,e,f,m_a,m_b,g]
    testcases.extend(additionalGraphs)
    with open(filename, "w") as my_file:
        my_file.write(f"{len(testcases)}\n")
        for o in testcases:
            graph: Graph = o
            my_file.write(f"{graph.numberOfNodes} {graph.numberOfEdges}\n")
            for v,edges in graph.graphBiDirection.items():
                for u in sorted(edges):
                    if u>v:
                        my_file.write(f"{v} {u}\n")
def solve_using_greedy(graphs: list[Graph]):
    sols = []
    for i in range(len(graphs)):
        # print(f"Graph {i}: \n")
        if graphs[i].is_connected():
            # graphs[i].print_gv_bi()
            (greedy_leaves, greedy_tree) = find_st_greedy_ds(graphs[i])
            # print(f"Greedy Solution Leaves: {greedy_leaves}")
            # print("Greedy Tree: \n")
            # greedy_tree.print_gv_bi()
            sols.append((greedy_tree,greedy_leaves))
        else:
            sols.append((Graph(0,[]),0))
        # print("\n\n\n")
    return sols

def ensembler(graphs: list[Graph], max_lp_nodes=250, log_short=None, log_long=None, progress_log=None):
    sols = []
    G_len = len(graphs)
    LP_better = 0
    greedy_better = 0
    fo1 = open(log_short, 'a+')
    fo2 = open(log_long, 'a+')
    for i in range(G_len):
        graph = graphs[i]
        fo1.write(f"{'-'*5} Graph {i+1} / {G_len} {'-'*5}\n")
        fo2.write(f"{'-'*5} Graph {i+1} / {G_len} {'-'*5}\n")
        with open(progress_log, 'w+') as pfo:
            pfo.write(f"{'-'*15} Graph {i+1} / {G_len} {'-'*15}\n")
        # try:
        if graph.is_connected():
            if graph.numberOfEdges < 50:
                fo2.write(graph.ret_gv_bi())
            else:
                fo2.write(f"Omitting input graph viz for size - {graph.numberOfEdges} > 50 edges\n")
            # If less than four nodes or six edges, use brute force
            if graph.numberOfNodes <= 4 or graph.numberOfEdges <= 6:
                fo1.write("Going with brute force\n")
                fo2.write("Going with brute force\n")
                (bf_leaves, bf_tree) = find_st_bf(graph, copy.deepcopy(graph), Graph(graph.numberOfNodes))
                if bf_tree != None:
                    fo1.write(f"Final Leaves: {bf_leaves}\n")
                    fo2.write(f"Final Leaves: {bf_leaves}\n")
                    fo2.write("Final Tree:\n")
                    fo2.write(bf_tree.ret_gv_bi())
                    sols.append((bf_tree, bf_leaves))
                else:
                    sols.append((Graph(0,[]),1))
                    fo1.write("Single node case")
                    fo2.write("Single node case")
            # otherwise, use other solution we have right now
            else:
                fo1.write("Too big for brute force\n")
                fo2.write("Too big for brute force\n")
                fo1.write("Trying greedy\n")
                fo2.write("Trying greedy\n")
                
                (greedy_leaves, greedy_tree) = find_st_greedy_ds(graph)
                (LP_leaves, LP_tree) = (None, None)
                if graph.numberOfNodes < max_lp_nodes:
                    (LP_leaves, LP_tree) = find_st_LP(graph, time_limit=(3*60+30),
                                                      baseline=greedy_leaves)
                if LP_leaves is not None and graph.st_checker(LP_tree):
                    sols.append((LP_tree, LP_leaves))
                    LP_better += 1
                    fo1.write("LP did best\n")
                    fo2.write("LP did best\n")
                    fo1.write(f"Final Leaves: {LP_leaves}\n")
                    fo2.write(f"Final Leaves: {LP_leaves}\n")
                    fo2.write("Final Tree:\n")
                    if LP_tree.numberOfEdges < 50:
                        fo2.write(LP_tree.ret_gv_bi())
                    else:
                        fo2.write(f"Omitting solution graph viz for size - {LP_tree.numberOfEdges} > 50 edges\n")
                else:
                    sols.append((greedy_tree,greedy_leaves))
                    greedy_better += 1
                    fo1.write("Greedy did best\n")
                    fo2.write("Greedy did best\n")
                    fo1.write(f"Final Leaves: {greedy_leaves}\n")
                    fo2.write(f"Final Leaves: {greedy_leaves}\n")
                    fo2.write("Final Tree:\n")
                    if greedy_tree.numberOfEdges < 50:
                        fo2.write(greedy_tree.ret_gv_bi())
                    else:
                        fo2.write(f"Omitting solution graph viz for size - {greedy_tree.numberOfEdges} > 50 edges\n")
        else:
            fo1.write(f"Graph is unconnected.\n")
            fo2.write(f"Graph is unconnected.\n")
            sols.append((Graph(0,[]),0))
    fo1.close()
    fo2.close()
    print(f"Number of solutions: {len(sols)}")
    return sols

def test_ensembler(inps):
    sols_ens = ensembler(inps)
    sols_greedy = solve_using_greedy(inps)
    # for sol in range(len())
    assert len(sols_ens) == len(sols_greedy)
    for i in range(len(sols_ens)):
        ens_tree, ens_leaves = sols_ens[i]
        greedy_tree, greedy_leaves = sols_greedy[i]
        print(f"Testing agreement on graph {i+1} / {len(inps)}")
        if ens_leaves != greedy_leaves:
            print(f"Difference on graph {i}")
            inps[i].print_gv_bi()
            print(f"Ensembler leaves {ens_leaves}, Greedy leaves {greedy_leaves}")
            if greedy_tree.numberOfNodes < 10:
                print("Ensembler tree:")
                ens_tree.print_gv_bi()
                print("Greedy tree:")
                greedy_tree.print_gv_bi()
            return
    print("All tests passed")
            # printf("Ensembler solution l")

def get_all_hard_in(filename):
    graphs: list[Graph] = list()
    with open(filename) as my_file:
        cnt = 1
        for line in my_file:
            current_graph = list(map(int, line.split()))
            current_edges = []
            print(f"Graph {cnt}, size: {current_graph}")
            for j in range(current_graph[1]):
                new_edge = list(map(int, my_file.readline().split()))
                current_edges.append(new_edge)
            graphs.append(Graph(current_graph[0], current_edges))
            cnt+=1
        # cnt should be 524 at end
    return graphs

# triple check our all hard outs are valid spanning trees of their respective
# graphs with correct leaf counts
def test_all_hard_out(all_hard_inps: list[Graph], all_hard_out_file):
    graphs: list[Graph] = list()
    wrong = []
    with open(all_hard_out_file) as fo:
        cnt = 0
        print("graph number | is a spanning tree | has right number of leaves")
        for inp_graph in all_hard_inps:
            print(f"{cnt+1}...", end=" ")
            num_nodes = inp_graph.numberOfNodes
            output_graph = Graph(num_nodes)
            leaves, num_out_edges = list(map(int, fo.readline().split()))
            # edges = []
            for i in range(num_out_edges):
                new_edge = list(map(int, fo.readline().split()))
                output_graph.add_edge(new_edge)
            # Check graph is a spanning tree
            if inp_graph.st_checker(output_graph):
                print("✅", end=" ")
            else:
                print("❌", end=" ")
                wrong.append(cnt)
            # Check the number of leaves correct
            if calculate_number_of_leaves(output_graph) == leaves:
                print("✅", end=" ")
            else:
                print("❌", end=" ")
                wrong.append(cnt+1)
            print("\n")
            cnt += 1
    print("\n")
    if cnt != 524:
        print("Wrong number of input and output instances")
    else:
        print("Right number of input and output instances")
    print(f"{len(wrong)} incorrect outputs:")
    print(wrong)

if __name__ == "__main__":
    # test_st_greedy_ds()
    inps = get_all_hard_in("all-hard.in")
    # print(inps[4].numberOfEdges)
    # sols_ensembler = ensembler(inps)
    # test_st_LP("test_lp.txt")
    # fi_cases = get_input("fi_hard.in")
    # gen_hard_in("hard.in", fi_cases)
    # inps = get_input("hard.in")
    # sols_ensembler = ensembler(inps,
    #                            max_lp_nodes=75,
    #                            log_short="log_short.txt",
    #                            log_long="log_long.txt",
    #                            progress_log="progress_log.txt")
    # test_ensembler(inps)
    # sols = solve_using_greedy(inps)
    # gen_output("all-hard.out", sols_ensembler)
    test_all_hard_out(inps, "all-hard.out")
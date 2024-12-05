class Graph:
    def __init__(self, n, edges=None):
        # adjacency list mapping vert -> incident edges
        self.numberOfNodes = n
        self.numberOfEdges = 0
        self.graph = {}
        self.graphBiDirection = {}
        self.nodes = set()
        for i in range(n):
            self.graph[i] = []
            self.graphBiDirection[i] = []
            self.nodes.add(i)
        if edges:
            for i in edges:
                self.numberOfEdges+=1
                self.graph[i[0]].append(i[1])
                # To make it undirected, could potentially remove, would require modifications in other parts of the code
                # but could be worthwhile if we have to constantly keep accounting for it
                self.graphBiDirection[i[0]].append(i[1])
                self.graphBiDirection[i[1]].append(i[0]) 
    def __str__(self):
        return "{}".format(self.graph)
    
    def add_edge(self, edge):
        self.graph[edge[0]].append(edge[1])
        self.graphBiDirection[edge[0]].append(edge[1])
        self.graphBiDirection[edge[1]].append(edge[0]) 
        self.numberOfEdges+=1
    def remove_edge(self, edge):
        if edge[0] in self.graph and edge[1] in self.graph[edge[0]]:
            self.graph[edge[0]].remove(edge[1])
            self.graphBiDirection[edge[0]].remove(edge[1])
            self.graphBiDirection[edge[1]].remove(edge[0])
            self.numberOfEdges-=1
        if edge[1] in self.graph and edge[0] in self.graph[edge[1]]:
            self.graph[edge[1]].remove(edge[0])
            self.graphBiDirection[edge[0]].remove(edge[1])
            self.graphBiDirection[edge[1]].remove(edge[0])
            self.numberOfEdges-=1

    def delete_node(self, node: int):
        if node in self.graphBiDirection:
            self.numberOfNodes-=1
            self.numberOfEdges-=len(self.graphBiDirection[node])
            for i in self.graphBiDirection[node]:
                self.graphBiDirection[i].remove(node)
                if i in self.graph and node in self.graph[i]:
                    self.graph[i].remove(node)
            self.graph.pop(node)
            self.graphBiDirection.pop(node)

    def print_gv(self):
        '''
        Prints the code for the current that can be copy-pasted into graphviz for visualization
        '''
        # for use with visualizer: https://dreampuf.github.io/GraphvizOnline/#digraph%20G
        print("digraph G {")
        print("edge [dir = none]")
        for u in self.graph:
            for v in self.graph[u]:
                print(u, "->", v)
        print("}")
    def print_gv_bi(self):
        '''
        Prints the code for the current that can be copy-pasted into graphviz for visualization
        '''
        # for use with visualizer: https://dreampuf.github.io/GraphvizOnline/#digraph%20G
        print("digraph G {")
        print("edge [dir = none]")
        for u in self.graph:
            for v in self.graphBiDirection[u]:
                if v>u:
                    print(u, "->", v)
        print("}")

    # TODO: if needed if recursion depth exceeded for large graphs, make iterative
    def explore_st_checker(self, tree, u, parent, visited):
        '''
        Returns True if no error (cycles/erroneous edges were found) in the spanning tree provided for the current graph
        '''
        visited.add(u)
        for v in tree.graph[u]:
            if v not in self.graph[u]: #To make sure the edges for the tree exist in the graph too
                return True
            if v not in visited:
                cycle = self.explore_st_checker(tree,v,u,visited)
                if cycle:
                    return True
            elif v!=parent: # To account for birectionality 
                return True
        return False
    
    def st_checker(self, tree):
        '''
        Checks if the given tree (instance of a graph) is a spanning tree for the current graph, returns True if it is, False otherwise.
        '''
        visited = set()
        error = self.explore_st_checker(tree,0,0,visited)
        if error or visited!=self.nodes:
            return False
        return True
    def explore_is_connected(self,u, visited):
        visited.add(u)
        for v in self.graph[u]:
            if v not in visited:
                self.explore_is_connected(v,visited)
    def is_connected(self):
        visited = set()
        self.explore_is_connected(0,visited)
        if visited!=self.nodes:
            return False
        return True

    

    
    
    
def test_checker():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    a_tree=Graph(5, [(0,1), (1,2), (2,3), (2,4)])
    a_tree2=Graph(5, [(0,1), (1,2), (1,3), (2,4)])
    a_tree3=Graph(5, [(0,1), (1,2), (1,3)])
    print(a.st_checker(a_tree)) #Expected: True
    print(a.st_checker(a_tree2)) #Expected: True
    print(a.st_checker(a)) #Expected: False
    print(a.st_checker(a_tree3)) #Expected: False
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    b.print_gv_bi()
    b_tree = Graph(6, [(0,1), (1,2),(1,3),(2,4),(4,5)])
    b_tree2 = Graph(6, [(0,1), (1,2),(1,3),(2,4),(3,5)])
    b_tree3 = Graph(6, [(0,1), (1,2),(2,3),(2,4),(3,5)])
    b_tree4 = Graph(6, [(0,1), (1,2),(2,3),(3,4),(4,5)])
    b_tree5 = Graph(6, [(0,1), (1,2),(2,3),(2,4),(3,5),(5,4)])
    print(b.st_checker(b_tree)) #Expected: True
    print(b.st_checker(b_tree2)) #Expected: True
    print(b.st_checker(b_tree3)) #Expected: True
    print(b.st_checker(b_tree4)) #Expected: False
    print(b.st_checker(b_tree5)) #Expected: False
    print(b.st_checker(a_tree)) #Expected: False
    b.print_gv_bi()
    b.remove_edge((1,3))
    b.print_gv_bi()
    b.add_edge((0,3))
    b.print_gv_bi()

def test_is_connected():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    a.print_gv()
    a_tree=Graph(5, [(0,1), (1,2), (2,3), (2,4)])
    a_tree2=Graph(5, [(0,1), (1,2), (1,3), (2,4)])
    a_tree3=Graph(5, [(0,1), (1,2), (1,3)])
    b = Graph(5, [(1,2),(1,3),(2,3),(2,4)])
    c = Graph(5, [(0,1), (1,2),(1,3),(2,3)])
    d = Graph(6, [(0,1),(1,3),(2,3),(2,4),(4,5),(5,3)])
    print(a.is_connected())
    print(a_tree.is_connected())
    print(a_tree2.is_connected())
    print(a_tree3.is_connected())
    print(b.is_connected())
    print(c.is_connected())
    print(d.is_connected())
def test_delete_node():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    a.print_gv_bi()
    a.delete_node(1)
    a.print_gv_bi()
    print(a.graph)
    print(a.graphBiDirection)
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    b.print_gv_bi()
    b.delete_node(2)
    b.print_gv_bi()
    print(b.graph)
    print(b.graphBiDirection)
    c = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    c.print_gv_bi()
    c.delete_node(0)
    c.delete_node(5)
    c.delete_node(4)
    c.print_gv_bi()
    print(c.graph)
    print(c.graphBiDirection)


if __name__ == "__main__":
    test_delete_node()

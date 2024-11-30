class Graph:
    def __init__(self, n, edges=None):
        # adjacency list mapping vert -> incident edges
        self.graph = {}
        self.nodes = set()
        for i in range(n):
            self.graph[i] = []
            self.nodes.add(i)
        if edges:
            for i in edges:
                self.graph[i[0]].append(i[1])
                # To make it undirected, could potentially remove, would require modifications in other parts of the code
                # but could be worthwhile if we have to constantly keep accounting for it
                self.graph[i[1]].append(i[0]) 
    def __str__(self):
        return "{}".format(self.graph)
    
    def print_gv(self):
        '''
        Prints the code for the current that can be copy-pasted into graphviz for visualization
        '''
        # for use with visualizer: https://dreampuf.github.io/GraphvizOnline/#digraph%20G
        print("digraph G {")
        print("edge [dir = none]")
        for u in self.graph:
            for v in self.graph[u]:
                if v>u: # To account for birectionality, since we do not need to add 2 edges in graphviz, we can ignore the repeated ones
                    print(u, "->", v)
        print("}")

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
    

    
    
    
def test_checker():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    a.print_gv()
    a_tree=Graph(5, [(0,1), (1,2), (2,3), (2,4)])
    a_tree2=Graph(5, [(0,1), (1,2), (1,3), (2,4)])
    a_tree3=Graph(5, [(0,1), (1,2), (1,3)])
    print(a.st_checker(a_tree)) #Expected: True
    print(a.st_checker(a_tree2)) #Expected: True
    print(a.st_checker(a)) #Expected: False
    print(a.st_checker(a_tree3)) #Expected: False
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    b.print_gv()
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

if __name__ == "__main__":
    test_checker()
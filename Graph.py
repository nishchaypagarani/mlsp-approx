class Graph:
    def __init__(self, n, edges=None):
        self.graph = {}
        self.nodes = set()
        for i in range(n):
            self.graph[i] = []
            self.nodes.add(i)
        if edges:
            for i in edges:
                self.graph[i[0]].append(i[1])
                self.graph[i[1]].append(i[0]) # To make it undirected, could potentially remove

    def __str__(self):
        return "{}".format(self.graph)
    
    def print_gv(self):
        # for use with visualizer: https://dreampuf.github.io/GraphvizOnline/#digraph%20G
        print("digraph G {")
        print("edge [dir = none]")
        for u in self.graph:
            for v in self.graph[u]:
                if v>u: # To account for birectionality 
                    print(u, "->", v)
        print("}")

    def explore_st_checker(self, tree, u, parent, visited):
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
        visited = set()
        cycle = self.explore_st_checker(tree,0,0,visited)
        if cycle or visited!=self.nodes:
            return False
        return True
    

    
    
    
def test_checker():
    a = Graph(5, [(0,1), (1,2),(1,3),(2,3),(2,4)])
    a.print_gv()
    a_tree=Graph(5, [(0,1), (1,2), (2,3), (2,4)])
    a_tree2=Graph(5, [(0,1), (1,2), (1,3), (2,4)])
    a_tree3=Graph(5, [(0,1), (1,2), (1,3)])
    print(a.st_checker(a_tree))
    print(a.st_checker(a_tree2))
    print(a.st_checker(a))
    print(a.st_checker(a_tree3))
    b = Graph(6, [(0,1), (1,2),(1,3),(2,3),(2,4),(4,5),(5,3)])
    b.print_gv()
    b_tree = Graph(6, [(0,1), (1,2),(1,3),(2,4),(4,5)])
    b_tree2 = Graph(6, [(0,1), (1,2),(1,3),(2,4),(3,5)])
    b_tree3 = Graph(6, [(0,1), (1,2),(2,3),(2,4),(3,5)])
    b_tree4 = Graph(6, [(0,1), (1,2),(2,3),(3,4),(4,5)])
    b_tree5 = Graph(6, [(0,1), (1,2),(2,3),(2,4),(3,5),(5,4)])
    print(b.st_checker(b_tree))
    print(b.st_checker(b_tree2))
    print(b.st_checker(b_tree3))
    print(b.st_checker(b_tree4))
    print(b.st_checker(b_tree5))
    print(b.st_checker(a_tree))

if __name__ == "__main__":
    test_checker()
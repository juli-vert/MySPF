class graph:
     
    def __init__(self):
        self.g = {}
    
    def addvertex(self, v):
        self.g.update({v.name:v.neighbors})
        
    def printgraph(self):
        print(self.g)
    
    def dijkstraAB(self, a, b):
        if a.name not in self.g.keys() or b.name not in self.g.keys():
            return -1
        else:
            pathcost = 0
            edges = self.g[a.name]
            if b.name in dict(edges).keys(): #direct path
                return dict(edges)[b.name]
            else: #there is no direct path
                return -2
                
class vertex:
    
    def __init__(self, n):
        self.neighbors = []
        self.name = n
        
    def addneighbor(self, n, cost):
        self.neighbors.append((n.name, cost))
    

if __name__ == '__main__':
    g1 = graph()
    v1 = vertex('a')
    g1.addvertex(v1)
    g1.printgraph()
    v2 = vertex('b')
    v1.addneighbor(v2, 100)
    g1.addvertex(v2)
    g1.printgraph()
    v3 = vertex('c')
    v1.addneighbor(v3, 50)
    g1.addvertex(v3)
    v4 = vertex('d')
    v3.addneighbor(v4, 140)
    g1.addvertex(v4)
    g1.printgraph()
    v2.addneighbor(v4, 80)
    g1.printgraph()
    v5 = vertex('e')
    e = g1.dijkstraAB(v1,v5)
    if e == -1:
        print('One of the vertex doesn\'t belong to this graph')
    elif e == -2:
        print('We need to run thru the graph')
    else:
        print('Cost of direct path is {0}'.format(e))

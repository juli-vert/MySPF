import json

def Test1():
    # Testing graph 1
    '''
    A ----100-----B
    |             |
    50           80
    |             |
    C-----140-----D
    '''
    g1 = graph()
    v1 = graph.vertex('a')
    g1.addvertex(v1)
    v2 = graph.vertex('b')
    v1.addneighbor(v2, 100)
    g1.addvertex(v2)
    v3 = graph.vertex('c')
    v1.addneighbor(v3, 50)
    g1.addvertex(v3)
    v4 = graph.vertex('d')
    v3.addneighbor(v4, 140)
    g1.addvertex(v4)
    v2.addneighbor(v4, 80)
    g1.printgraph()
    #v5 = vertex('e')
    e, nh = g1.dijkstraAB(v1.name,v4.name)
    if e == -1:
        print('One of the vertex doesn\'t belong to this graph')
    else:
        print('Cost of direct path is {0} via {1}'.format(e, nh))

def Test2():
    '''
    A-----100-----B-----50-----E
    |             |            |
    50           80           25
    |             |            |
    C-----140-----D-----30-----F
    '''
    g1 = graph()
    v1 = graph.vertex('a')
    v2 = graph.vertex('b')
    v3 = graph.vertex('c')
    v4 = graph.vertex('d')
    v5 = graph.vertex('e')
    v6 = graph.vertex('f')
    v1.addneighbor(v2, 100)
    v1.addneighbor(v3, 50)
    v2.addneighbor(v1, 100)
    v2.addneighbor(v4, 80)
    v2.addneighbor(v5, 50)
    v3.addneighbor(v1, 50)
    v3.addneighbor(v4, 140)
    v4.addneighbor(v2, 80)
    v4.addneighbor(v3, 140)
    v4.addneighbor(v6, 30)
    v5.addneighbor(v2, 50)
    v5.addneighbor(v6, 25)
    v6.addneighbor(v4, 30)
    v6.addneighbor(v5, 25)
    g1.addvertex(v1)
    g1.addvertex(v2)
    g1.addvertex(v3)
    g1.addvertex(v4)
    g1.addvertex(v5)
    g1.addvertex(v6)
    g1.printgraph()
    e, nh = g1.dijkstraAB(v1.name,v4.name)
    if e == -1:
        print('One of the vertex doesn\'t belong to this graph')
    else:
        print('Cost of direct path is {0} via {1}'.format(e, nh))

def Test3():
    '''
    A-----100-----B-----50-----E
    |             |            |
    10           80           25
    |             |            |
    C------10-----D-----30-----F
    '''
    g1 = graph()
    v1 = graph.vertex('a', 100)
    v2 = graph.vertex('b')
    v3 = graph.vertex('c')
    v4 = graph.vertex('d', 175)
    v5 = graph.vertex('e')
    v6 = graph.vertex('f', 50)
    v1.addneighbor(v2, 100)
    v1.addneighbor(v3, 10)
    v2.addneighbor(v1, 100)
    v2.addneighbor(v4, 80)
    v2.addneighbor(v5, 50)
    v3.addneighbor(v1, 10)
    v3.addneighbor(v4, 10)
    v4.addneighbor(v2, 80)
    v4.addneighbor(v3, 10)
    v4.addneighbor(v6, 30)
    v5.addneighbor(v2, 50)
    v5.addneighbor(v6, 25)
    v6.addneighbor(v4, 30)
    v6.addneighbor(v5, 25)
    g1.addvertex(v1)
    g1.addvertex(v2)
    g1.addvertex(v3)
    g1.addvertex(v4)
    g1.addvertex(v5)
    g1.addvertex(v6)
    g1.printgraph()
    e, nh = g1.dijkstraAB(v1.name,v6.name)
    if e == -1:
        print('One of the vertex doesn\'t belong to this graph')
    else:
        print('Cost of direct path is {0} via {1}'.format(e, nh))
    print (g1.fullDijkstra())
    return g1

class graph:

    def __init__(self):
        self.g = {}
        # !!self.priors = {}
        self.dr = None
        self.bdr = None
        self.fullroute = None

    def listofvertex(self):
        return self.g.keys()

    def vertexexists(self, vname):
        if vname in self.g.keys():
            return True
        else:
            return False
     
    def addvertex(self, v):
        if v.name not in self.g.keys():
            self.g.update({v.name:v})
            # !!self.priors.update({v.name:v.priority})
            if self.dr == None:
                self.dr = v.name
            else:
                if self.bdr == None:
                    self.bdr = v.name
                else:
                    if self.g[self.dr].priority > v.priority:
                        self.bdr = self.dr
                        self.dr = v.name
                    else:
                        if self.g[self.bdr].priority > v.priority:
                            self.bdr = v.name
            self.printgraph()
            print('!--- New vertex found: Updating routing tables ---!')
            self.fullroute = self.fullDijkstra()
            for v in self.g.keys(): #send the vertex routes to each
                self.g[v].updaterouting(self.fullroute[v])
        else:
            print("Vertex {0} is already in the graph".format(v.name))

    def delvertex(self, v):
        if v.name not in self.g.keys():
            print("Vertex {0} is not in the graph".format(v.name))
        else:
            if v.name == self.dr or v.name == self.bdr:
                print("Designated Routers changed: Convergency in progress")
            else:
                print("Recalculating routes: Convergency in progress")
                # self.fullroute = self.fullDijkstra()

    def addedge(self, vs, vd, cost):
        self.g[vs].addneighbor(self.g[vd], cost)
        self.g[vd].addneighbor(self.g[vs], cost)
        self.printgraph()
        print('!--- New adjacency found: Updating routing tables ---!')
        self.fullroute = self.fullDijkstra()
        for v in self.g.keys(): #send the vertex routes to each
            self.g[v].updaterouting(self.fullroute[v])

    def printgraph(self):
        print("The DR is {0} and the DBR is {1}".format(self.dr, self.bdr))
        for it in self.g:
            print('Node {0} with neighbors: '.format(it))
            print(self.g[it].neighbors)
            print('and priority {0}'.format(self.g[it].priority))

    # p: current vertex
    # i: initial vertex (to avoid loops)
    # s: source vertex (from where we have been called)
    # b: destination
    # currentcost: sum of the costs until this point
    def __partialDijkstra(self, p, i, s, b, currentcost):
        pathcost = 0
        if p != i: #avoid loops
            print('From {0} via {1}-{2} to {3}'.format(i, s, p, b))
            if p in self.g.keys():
                edges = self.g[p].neighbors
                if b in edges.keys(): #direct path
                    # print('Direct path found at {0} by {1}'.format(p, str(dict(edges)[b] + currentcost)))
                    return (edges[b] + currentcost), b
                else: #there is no direct path
                    nexthop = None
                    for edge in edges:
                        if s != edge : # split horizon
                            #print('Calculating cost via {0} with {1}'.format(edge[0], str(currentcost+edge[1])))
                            cost, nh = self.__partialDijkstra(edge, i, p, b, currentcost+edges[edge])
                            if pathcost == 0:
                                pathcost = cost
                                nexthop = edge
                            else:
                                if pathcost > cost:
                                    pathcost = cost
                                    nexthop = edge
                    return pathcost, nexthop
            else:
                return 0, None
        else:
            return 0, None

    def dijkstraAB(self, a, b):
        if a not in self.g.keys() or b not in self.g.keys():
            return -1, None
        else:
            if len(self.g[b].neighbors) > 0: # only if there is at least a path to the destination
                pathcost = 0
                edges = self.g[a].neighbors
                if b in edges.keys(): #direct path
                    # print('Direct path found at {0}'.format(a))
                    return edges[b], b
                else: #there is no direct path
                    nexthop = None
                    for edge in edges:
                        #print('Calculating cost via {0} with {1}'.format(edge[0], str(edge[1])))
                        cost, nh = self.__partialDijkstra(edge, a, a, b, edges[edge])
                        if pathcost == 0:
                            pathcost = cost
                            nexthop = edge
                        else:
                            if pathcost > cost:
                                pathcost = cost
                                nexthop = edge
                    return pathcost, nexthop
            else:
                return -1, None

    def fullDijkstra(self):
        tpath = {}
        for vxs in self.g.keys():
            ppath = {vxs:{}}
            for vxd in self.g.keys():
                lpath = {}
                if vxs != vxd:
                    c, nh = self.dijkstraAB(vxs, vxd)
                    lpath.update({vxd:(c, nh)})
                else:
                    lpath.update({vxd:(0, None)})
                ppath[vxs].update(lpath)
            tpath.update(ppath)
        return tpath

    class vertex:

        def __init__(self, n, p=255):
            self.neighbors = {}
            self.name = n
            self.priority = p
            self.rtable = None

        def addneighbor(self, n, cost):
            self.neighbors.update({n.name:cost})

        def delneighbor(self, n):
            if n.name in self.neighbors.keys():
                del self.neighbors[n]

        def updaterouting(self, routes):
            self.rtable = routes

        def printroutes(self):
            return self.rtable

if __name__ == '__main__':
    leave = False
    g1 = Test3()
    while not leave:
        opt = input('Pick an option:\n -(list) to check the list of vertex\n \
-(route+vertex_name) to check routing table of vertex_number\n \
-(add+vertex_name+priority) to add a new vertex to the network\n -(edge+vertex_source+vertex_dest+cost) to add a new edge\n \
-(remove+vertex_name) to delete the vertex from the network\n -(exit) to exit\n\
:')
        if opt == 'exit':
            leave = True
        elif 'route' in opt:
            if g1.vertexexists(opt.split('+')[1]):
                print(g1.g[opt.split('+')[1]].printroutes())
        elif opt == 'list':
            print(g1.listofvertex())
        elif 'add' in opt:
            if len(opt.split('+')) < 3:
                print('Wrong parameters\n')
            else:
                o, ver, prio = opt.split('+')
                v = graph.vertex(ver, int(prio))
                g1.addvertex(v)
        elif 'edge' in opt:
            if len(opt.split('+')) < 4:
                print('Wrong parameters\n')
            else:
                o, sv, dv, cost = opt.split('+')
                if g1.vertexexists(sv) and g1.vertexexists(dv):
                    g1.addedge(sv, dv, int(cost))
        elif 'remove' in opt:
            pass
        else:
            print('Wrong option\n')


    
    
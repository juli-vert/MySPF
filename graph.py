import json
class graph:

    def __init__(self):
        self.g = {}
        self.fullroute = None

    def listofvertex(self):
        return self.g.keys()

    def vertexexists(self, vname):
        return vname in self.g.keys()

    def addvertex(self, v):
        if v.name not in self.g.keys():
            self.g.update({v.name:v})
            self.printgraph()
            print('!--- New vertex found: Updating routing tables ---!')
            self.fullroute = self.fullDijkstra()
            for v in self.g.keys(): #send the vertex routes to each
                self.g[v].updaterouting(self.fullroute[v])
            return 1
        else:
            print("Vertex {0} is already in the graph".format(v.name))
            return 0

    def delvertex(self, v):
        if v not in self.g.keys():
            print("Vertex {0} is not in the graph".format(v.name))
        else:
            print("Recalculating routes: Convergency in progress")
            for ver in self.g.keys():
                self.g[ver].delneighbor(self.g[v])
            del self.g[v]
            self.fullroute = self.fullDijkstra()
            for v in self.g.keys(): #send the vertex routes to each
                self.g[v].updaterouting(self.fullroute[v])

    def addedge(self, vs, vd, cost):
        self.g[vs].addneighbor(self.g[vd], cost)
        self.g[vd].addneighbor(self.g[vs], cost)
        self.printgraph()
        print('!--- New adjacency found: Updating routing tables ---!')
        self.fullroute = self.fullDijkstra()
        for v in self.g.keys(): #send the vertex routes to each
            self.g[v].updaterouting(self.fullroute[v])

    def deledge(self, vs, vd):
        if self.g[vs].delneighbor(self.g[vd]) and self.g[vd].delneighbor(self.g[vs]):
            self.printgraph()
            print('!--- New adjacency found: Updating routing tables ---!')
            self.fullroute = self.fullDijkstra()
            for v in self.g.keys(): #send the vertex routes to each
                self.g[v].updaterouting(self.fullroute[v])

    def printgraph(self):
        res = {}
        for it in self.g:
            print('Node {0} with neighbors: '.format(it))
            print(self.g[it].neighbors)
            print('and priority {0}'.format(self.g[it].priority))
            res.update({'Node {0} with priority {1}'.format(it, self.g[it].priority): self.g[it].neighbors})
        return json.dumps(res)

    # p: current vertex
    # path: vertex that we already walked thru (avoiding loops and split horizon)
    # b: destination
    # currentcost: sum of the costs until this point
    def __partialDijkstra(self, p, path, b, currentcost):
        if p not in path: # avoid loops and split horizon
            if p in self.g.keys():
                edges = self.g[p].neighbors
                pathcost = -1
                nexthop = None
                p2 = list(path)
                p2.append(p)
                for edge in edges:
                    if b == edge: #direct path
                        if pathcost == -1 or (pathcost > edges[b] + currentcost and edges[b] !=-1):
                            pathcost = edges[b] + currentcost
                            nexthop = b
                    else: #no direct path: we need to jump to the next
                        cost, nh = self.__partialDijkstra(edge, p2, b, currentcost+edges[edge])
                        if (pathcost == -1 and cost != -1) or (pathcost > cost and cost !=-1):
                            pathcost = cost
                            nexthop = edge
                return pathcost, nexthop
            else:
                return -1, None
        else:
            return -1, None

    def dijkstraAB(self, a, b):
        if a not in self.g.keys() or b not in self.g.keys():
            return -1, None
        else:
            if len(self.g[b].neighbors) > 0: # only if there is at least a path to the destination
                pathcost = -1
                edges = self.g[a].neighbors
                nexthop = None
                for edge in edges:
                    if b == edge: #direct path
                        if pathcost == -1 or (pathcost > edges[b] and edges[b] !=-1):
                            pathcost = edges[b]
                            nexthop = b
                    else: #no direct path: we need to jump to the next neighbor
                        path = [a]
                        cost, nh = self.__partialDijkstra(edge, path, b, edges[edge])
                        if pathcost == -1 or (pathcost > cost and cost !=-1):
                            pathcost = cost
                            nexthop = edge
                return pathcost, nexthop
            else:
                return -1, None

    # there is room for improvement. Once we get the best path from A to B, we can ensure
    # that path is the best from any vertex in within A and B
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
                del self.neighbors[n.name]
                return True
            else:
                print('{0} is not connected to {1}'.format(self.name, n.name))
                return False

        def updaterouting(self, routes):
            self.rtable = routes

        def printroutes(self):
            return self.rtable

if __name__ == '__main__':
    g1 = Test3()
    opt = input('Pick an option:\n -(list) to check the list of vertex\n \
-(route+vertex_name) to check routing table of vertex_number\n \
-(add+vertex_name+priority) to add a new vertex to the network\n \
-(edge+vertex_source+vertex_dest+cost) to add a new edge\n \
-(remove+vertex_name) to delete the vertex from the network\n \
-(del+vertex_source+vertex_dest) to delete an edge\n \
-(check+vertex_source+vertex_dest) to check the paths from source to dest\n \
-(exit) to exit\n\
:')
    while 1:
        if opt == 'exit':
            break
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
            if len(opt.split('+')) < 2:
                print('Wrong parameters\n')
            else:
                o, ver = opt.split('+')
                if g1.vertexexists(ver):
                    g1.delvertex(ver)
        elif 'check' in opt:
            if len(opt.split('+')) < 3:
                print('Wrong parameters\n')
            else:
                o, s, d = opt.split('+')
                print(g1.dijkstraAB(s,d))
        elif 'del' in opt:
            if len(opt.split('+')) < 3:
                print('Wrong parameters\n')
            else:
                o, sv, dv = opt.split('+')
                v = g1.deledge(sv,dv)
        else:
            print('Wrong option\n')
        opt = input(':')




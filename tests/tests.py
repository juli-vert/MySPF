from graph import graph

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
    '''e, nh = g1.dijkstraAB(v1.name,v6.name)
    if e == -1:
        print('One of the vertex doesn\'t belong to this graph')
    else:
        print('Cost of direct path is {0} via {1}'.format(e, nh))'''
    print (g1.fullDijkstra())
    return g1
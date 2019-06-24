from graph import graph
from ipaddress import ip_address, ip_network, ip_interface
from flask import json, Flask, make_response, Response
import time
import sys
import json

class controller(graph):

    def __init__(self, ip='192.168.1.132/24', p=8088):
        print('Setting up the controller')
        self.ipmgmt = ip_interface(ip)
        self.port = p
        self.managed_routers = {"nodes": []}
        # format: '{"nodes": [{"name" : "A", "ip" : "10.0.0.1", "port" : 8088, "interfaces": [1, 2, 3]}, {"name" : "B", "ip" : "10.0.0.15", "port" : 8088, "interfaces": [1, 4, 6]}]}'
        graph.__init__(self)

    def getIP(self):
        print(str(self.ipmgmt.ip))
        return str(self.ipmgmt.ip)

    def getNetwork(self):
        return self.printgraph()

    def registerRouter(self, name, ip, port, prior):
        v = graph.vertex(name, prior)
        self.managed_routers["nodes"].append({"name": name, "ip": ip, "port": port, "interfaces": []})
        return self.addvertex(v)

    def registerIface(self, name, ip, cost):
        res = []
        exists = False
        idx = 0
        for node in self.managed_routers['nodes']:
            if name == node['name']:
                exists = True
                break
            idx += 1
        if not exists:
            return 0, res
        else:
            iface = ip_interface(ip)
            # First we register the new interface into the managed_routers dictionary
            self.managed_routers['nodes'][idx]['interfaces'].append(iface)
            # Second we check if this new interface generates any new adjacency
            neighbors = []
            out = []
            for node in self.managed_routers['nodes']:
                for mriface in node['interfaces']:
                    if ip_interface(mriface).network == iface.network:
                        neighbors.append(node['name'])
            for neig in neighbors:
                out.append(self.addedge(name, neig, cost))
            for a, b in zip(neighbors, out):
                if b == 1:
                    res.append(a)
            return 1, res




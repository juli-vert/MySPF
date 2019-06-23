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
        graph.__init__(self)

    def getIP(self):
        print(str(self.ipmgmt.ip))
        return str(self.ipmgmt.ip)

    def getNetwork(self):
        return self.printgraph()

    def registerRouter(self, name, ip, prior):
        v = graph.vertex(name, prior)
        return self.addvertex(v)


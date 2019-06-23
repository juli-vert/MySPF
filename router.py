from graph import graph
from ipaddress import ip_address, ip_network, ip_interface
import requests as rq
import sys

class router():

    def __init__(self, name, mgmtIP, port, controllerIP, prio=255):
        if ip_address(controllerIP) not in ip_interface(mgmtIP).network.hosts():
            print('Controller IP {0} not in range {1}'.format(str(ip_address(controllerIP)), str(ip_interface(mgmtIP).network)))
        else:
            self.vertex = graph.vertex(name, prio)
            self.ip = ip_interface(mgmtIP)
            self.controller = ip_address(controllerIP)
            self.interfaces = {}
            params = {'name':name, 'ip': mgmtIP, 'port': port, 'priority': prio}
            r = rq.get('http://{0}:8088/router'.format(controllerIP), params=params)
            print(r)
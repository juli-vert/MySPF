from graph import graph
from flask import json, Flask, make_response, Response, request
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
            self.port = port
            self.controller = ip_address(controllerIP)
            self.interfaces = {}
            self.localroutes = {}
            params = {'name':name, 'ip': mgmtIP, 'port': port, 'priority': prio}
            r = rq.get('http://{0}:8089/router'.format(controllerIP), params=params)
            print(r)


if __name__ == '__main__':
    app = Flask(__name__)

    print (sys.argv)
    try:
        if len(sys.argv) == 6:
            for arg in sys.argv:
                if arg.startswith('name'):
                    name = arg.split("=")[1]
                elif arg.startswith('mgmtip'):
                    mgmtip = arg.split("=")[1]
                    if "/" not in mgmtip:
                        print("wrong management ip format")
                        raise Exception("wrong management ip format")
                elif arg.startswith('port'):
                    port = int(arg.split("=")[1])
                elif arg.startswith('controller'):
                    conip = arg.split("=")[1]
                elif arg.startswith('prio'):
                    prio = arg.split("=")[1]
                elif arg.startswith('router.py'):
                    pass
                else:
                    print('Unknow parameter')
                    raise Exception('unknow parameter')
            r = router(name, mgmtip, port, conip, prio)
            app.run(host=str(ip_interface(mgmtip).ip), port=port, debug=False)
        else:
            print('Wrong parameters')
            raise Exception('wrong parameters')
    except Exception as e:
        print(e)


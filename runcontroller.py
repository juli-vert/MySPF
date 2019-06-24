from flask import json, Flask, make_response, Response, request
import json
from controller import controller
import sys

app = Flask(__name__)

@app.route('/')
def getNetwork():
    global __g
    out = __g.getNetwork()
    resp = Response(out, status=200, mimetype='application/json')
    return resp

@app.route('/routetable')
def getRouting():
    global __g
    out = __g.fullroute
    resp = Response(json.dumps(out, indent=4), status=200, mimetype='application/json')
    return resp

# callable method to register a new router
@app.route('/router', methods=['GET'])
def registerRouter():
    global __g
    rname = request.args.get('name')
    rip = request.args.get('ip')
    rport = request.args.get('port')
    rpriority = request.args.get('priority')
    out = __g.registerRouter(rname, rip, rport, rpriority)
    if out:
        resp = Response('New router added', status=200, mimetype='text/plain')
    else:
        resp = Response('Failed to add router', status=200, mimetype='text/plain')
    return resp

# method 'PUT' using json to be define
@app.route('/jrouter', methods=['GET'])
def registerjRouter():
    pass

@app.route('/link', methods=['GET'])
def registerIface():
    rname = request.args.get('name')
    ip = request.args.get('ip')
    mask = request.args.get('mask')
    cost = request.args.get('cost')
    out, neighbors = __g.registerIface(rname, '{0}/{1}'.format(ip, mask), int(cost))
    if out:
        out = '{{ "Node" : "{0}", "Interface" : "{1}", "Neighbors" : ["{2}"] }}'.format(rname, '{0}/{1}'.format(ip, mask), '","'.join(neighbors))
        resp = Response(json.dumps(json.loads(out), indent=4), status=200, mimetype='application/json')
    else:
        resp = Response('Failed to add new interface', status=200, mimetype='text/plain')
    return resp

if __name__ == '__main__':
    n = p = h = False
    for arg in sys.argv:
        if arg.startswith('-h'):
            h = arg.split('h')[1]
        elif arg.startswith('-n'):
            n = arg.split('n')[1]
        elif arg.startswith('-p'):
            p = arg.split('p')[1]
    if h and n and p:
        __g = controller(ip=h, net=n, p=int(p))
    else:
        print("Not all parameters have been met, running with defaults")
        __g = controller()

    print(__g)
    app.run(host=__g.getIP(), port=__g.port, debug=False)
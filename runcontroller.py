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
def registerLink():
    pass

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
    __g = controller()

print(__g)
app.run(host=__g.getIP(), port=__g.port, debug=False)
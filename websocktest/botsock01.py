from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from bottle import route, run, template, get, post, request

@get('/websocket', apply=[websocket])
def echo(ws):
	while True:
		msg = ws.receive()
		if msg is not None:
			ws.send(msg)
		else: break
			
run(host='0.0.0.0', port=5000, server=GeventWebSocketServer)
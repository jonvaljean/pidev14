from bottle import request, Bottle, abort

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
#from gevent import monkey; monkey.patch_all()


app = Bottle()

@app.route('/start')
def start():
	HTML = """
		<!DOCTYPE html>
		<html>
			<head>
  			<script type="text/javascript">
    			var ws = new WebSocket("ws://0.0.0.0:8080/websocket");
    			ws.onopen = function() {
        	ws.send("Hello, happy world");
    	};
    	ws.onmessage = function (evt) {
        alert(evt.data);
    	};
  	</script>
		</head>
		</html>
		"""
	return HTML



@app.route('/websocket')
def handle_websocket():
	wsock = request.environ.get('wsgi.websocket')
	print("in handle_websocket")		
	if not wsock:
		abort(400, 'Expected WebSocket request.')
		timecounter = 0
		while True:
			timecounter +=1
			try:
				message = wsock.receive()
				print('in try, message is ', message)
				wsock.send("Your message was: %r" % message)
				wsock.send("timecounter is: %6s" % timecounter)
			except WebSocketError:
				print('in WebSocketError')
				break

print("before start server")
server = WSGIServer(("0.0.0.0", 8080), app,
                    handler_class=WebSocketHandler)
#server.start()
print("after server.start")
server.serve_forever()
print("after serve_forever")
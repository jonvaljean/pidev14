from bottle import request, Bottle, abort
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

    while True:
        try:
            message = wsock.receive()
            print('in try, message is ', message)
            wsock.send("Your message was: %r" % message)
        except WebSocketError:
            print('in WebSocketError')					
            break

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("127.0.0.1", 5000), app,
                    handler_class=WebSocketHandler)
server.serve_forever()
#example websocket code from yoker on https://pythonexample.com/code/bottle%20websocket%20server/
#coding: utf-8
 
import sys, time, json
reload(sys)
sys.setdefaultencoding('utf-8')
 
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from bottle import get, run
 
 
@get('/chat', apply=[websocket])
def chat(ws):
    while True:
        msg = ws.receive()
        if msg is not None:
            print 'received: ' + msg
            j = json.loads(msg)
            ws.send('[{}]>{}: {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()), j[0], j[1]))
 
@get('/')
def home():
    return """<html>
<script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
<body>
<div>
<input id="user" type="text" value="Yoker" />
<input id="msg" type="text" value="how old are you?" />
<input id="send" type="button" value="submit" />
</div>
<div id="messages"></div>
</body>
<script>
    $(document).ready(function() {
        if (!window.WebSocket) {
            if (window.MozWebSocket) {
                window.WebSocket = window.MozWebSocket;
            } else {
                $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
            }
        }
        ws = new WebSocket('ws://localhost:8080/chat');
        ws.onopen = function(evt) {
            console.log(evt);
            console.log(ws);
            $('#messages').append('<li>Connected to '+ evt.target.url +'.</li>');
        }
        ws.onmessage = function(evt) {
            console.log(evt);
            $('#messages').append('<li>' + evt.data + '</li>');
        }
        ws.onclose = function(evt) {
            console.log(evt);
            $('#messages').append('<li>closed.</li>');
        }
        $('#send').click(function() {
            var msg = $('#msg').val();
            var user = $('#user').val();
            ws.send(JSON.stringify([user, msg]));
        });
    });
</script>
</html>
    """

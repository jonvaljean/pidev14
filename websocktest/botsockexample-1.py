# example bottle websocket code from sk364 on https://pythonexample.com/code/bottle%20websocket%20server/

from bottle import get, run
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
 
 
@get('/', apply=[websocket])
def echo(ws):
    urls = ['https://media.starwars.ea.com/content/starwars-ea-com/en_US/starwars/battlefront/news-articles/collect-iconic-heroes-and-dominate-the-universe-in-star-wars-gal/_jcr_content/featuredImage/renditions/rendition1.img.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/1200px-Star_Wars_Logo.svg.png', 'http://www.planwallpaper.com/static/images/starwarsinfive-1449855236991_large.jpg']
    while True:
        if not urls: break
 
        txt = ws.receive()
        msg = 'document.getElementsByTagName("body")[0].innerHTML = "<img src=\'{}\'>"'.format(urls[0])
        ws.send(msg)
 
        del urls[0]
 
 
run(host='127.0.0.1', port=8000, server=GeventWebSocketServer)

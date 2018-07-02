from flask import Flask, request, Response
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask_cors import CORS
import json
from handler import *
import nfc_read

app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/")
def index():
    return "Hello World!"


@app.route('/socket/readCard')
# @content_type('application/json')
# @cross_origin()
def socket():
    if request.environ.get('wsgi.websocket'):
        print("Connected")
        ws = request.environ['wsgi.websocket']
        while True:
            cardid = nfc_read.nfc_read()
            if cardid is not "":
                msg = json.dumps({
                    "IsCard": True,
                    "CardID": cardid,
                    "IsNew": isNewCard(cardid),
                    "timestamp": int(time.time())
                })
                ws.send(msg)
                break
    return


@app.route("/api/createuser", methods=['POST'])
# @content_type('application/json')
# @cross_origin()
def createUserHandler():
    req_json = json.loads(request.data.decode('utf-8'))
    res = Response(
        response=createUser(req_json),
        content_type='application/json',
        status=200)
    res.headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
    res.headers[
        'Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    res.headers['Access-Control-Allow-Credentials'] = True

    return res


@app.route("/api/readuser", methods=['POST'])
# @content_type('application/json')
# @cross_origin()
def readUserHandler():
    req_json = json.loads(request.data.decode('utf-8'))
    res = Response(
        response=getUser(req_json),
        content_type='application/json',
        status=200)
    res.headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
    res.headers[
        'Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    res.headers['Access-Control-Allow-Credentials'] = True
    return res


@app.route("/api/updateuser", methods=['UPDATE'])
# @content_type('application/json')
# @cross_origin()
def updateUserHandler():
    return


@app.route("/api/log", methods=["POST"])
# @content_type('application/json')
# @cross_origin()
def logHandler():
    req_json = json.loads(request.data.decode('utf-8'))
    res = Response(addLog(req_json))
    res.headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
    res.headers[
        'Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    res.headers['Access-Control-Allow-Credentials'] = True
    return res


class WebSocket():
    def open_websocket(self):
        app.debug = True
        self.server = pywsgi.WSGIServer(
            ("", 3000), app, handler_class=WebSocketHandler)
        print("server runnning at port:3000")
        self.server.serve_forever()

    def close_websocket(self):
        self.server.close()


if __name__ == "__main__":
    ws = WebSocket()
    ws.open_websocket()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_api import status
from flask import jsonify

import threading
import json
from multiprocessing import Process, Value
import subprocess
import requests
import thread_model
import http.server
from utils.bigram import get_tokenized_words

model = thread_model.ThreadModel()
model.start()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qvm'
socketio = SocketIO(app)


#@app.route('/')
#def index():
#    return render_template('index.html')

#@app.route('/topic')
#def topic():
#    return render_template('topic.html')

#@app.route('/wordtree')
#def wordtree():
#    return render_template('wordtree.html')

#@app.route('/to-client/', methods=['POST'])
#def to_client():
#    data = request.get_json()
#    socketio.emit('server_response', {'id': 'to_client', 'data': data})
#    return "to_client message is sent"

# curl -i -H "Content-Type: application/json" -X POST -d '{"user_name": "test", "message": "hello"}' http://localhost:5252/json-check
#@app.route('/json-check', methods=['POST'])
#def connection_check():
#    print("json_check")
#    data = request.get_json()
#    print(data)
#    return data

# curl -i -H "Content-Type: application/json" -X POST -d '{"data": "전류를 더 많이 흘려 보낸다."}' http://localhost:5252/get-tokenized
@app.route('/get-tokenized', methods=['POST'])
def get_tokenized():
    print("get-tokenized")
    data = request.get_json()
    print(data)
    result, most_common_word = get_tokenized_words(data['data'])
    context = {
        'tokenized': result,
        'most_common': most_common_word,
    }
    return context

#@socketio.on('connection-check', namespace='/')
#def connection_check(message):
#    print("connection-check")
#    model.onPriorThread(model.connection_check, message['data'])
    
#@socketio.on('topic-modeling-file', namespace='/')
#def topic_modeling_file(message):
#    print("topic-modeling-file")
#    
#    """print(message)"""
#    """print('INPUT FILE : ', message['name'])"""
#    
#    model.onPriorThread(model.get_topic_modeling, message['data']['file'], message['data']['k'])


###############################################


#def transmitter_from_http_2_io(parameter):
#  socketio.emit('my response', parameter)

#@app.route('/terminal_post', methods=['POST'])
#def terminal_post():
#  data = request.get_json() 
#  for foobar in data:
#    print("-> ", foobar)
#  print( 'recived terminal_post : ' + str( data ) )
#  #socketio.emit( 'my response', data) # nothing happen
#  transmitter_from_http_2_io(data)
#  print(data)
#  return "ok"

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.use_reloader = True
    socketio.run(app, host="0.0.0.0", port=5252, debug=True)

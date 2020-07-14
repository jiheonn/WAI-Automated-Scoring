from flask import Flask, request
from flask_socketio import SocketIO
from utils import bigram

import argparse
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qvm'
socketio = SocketIO(app)

sa_logger = logging.getLogger("sentence-analysis")
sa_logger.setLevel(logging.INFO)
logger_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logger_format)
sa_logger.addHandler(stream_handler)


@app.route('/get-tokenized', methods=['POST'])
def get_tokenized():
    sa_logger.info("get-tokenized")
    requested_data = request.get_json()
    raw_sentence = requested_data['raw_sentence']
    print(f'[INPUT] raw_sentence : {raw_sentence}')
    result, most_common_word = bigram.get_tokenized_words(raw_sentence)
    context = {
        'tokenized': result,
        'most_common': most_common_word,
    }
    return context


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments for Sentence-Analysis Server.')
    parser.add_argument('--port', type=int, default=5252, help='port number for sentence-analysis server.')
    args = parser.parse_args()
    sa_logger.info("Start Sentence-Analysis Server.")
    socketio.run(app, host="0.0.0.0", port=args.port, debug=True)

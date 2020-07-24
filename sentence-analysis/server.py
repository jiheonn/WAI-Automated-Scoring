from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import bigram

import argparse
import logging

app = Flask(__name__)
app.config["SECRET_KEY"] = "qvm"
CORS(app, resources={r"/*": {"origins": "*"}})

sa_logger = logging.getLogger("sentence-analysis")
sa_logger.setLevel(logging.INFO)
logger_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logger_format)
sa_logger.addHandler(stream_handler)


@app.route("/get-tokenized/", methods=["GET"])
@cross_origin()
def get_tokenized():
    sa_logger.info("get-tokenized")
    raw_sentence = request.args.get('raw_sentence')
    print(f"[INPUT] raw_sentence : {raw_sentence}")
    result, most_common_word, frequency = bigram.get_tokenized_words(raw_sentence)
    context = {
        "tokenized": result,
        "most_common": most_common_word,
        "frequency": frequency,
    }
    return context

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Arguments for Sentence-Analysis Server."
    )

    args = parser.parse_args()
    sa_logger.info("Start Sentence-Analysis Server.")
    app.run(host="0.0.0.0", debug=True)
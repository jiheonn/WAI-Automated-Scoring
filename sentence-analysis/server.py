from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import bigram, topic_modeling

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


@app.route("/get-tokenized/", methods=["POST"])
@cross_origin()
def get_tokenized():
    sa_logger.info("get-tokenized")
    raw_sentence = request.form['raw_sentence']
    print(f"[INPUT] raw_sentence : {raw_sentence}")
    result, most_common_word, frequency = bigram.get_tokenized_words(raw_sentence)
    context = {
        "id": "get-tokenized",
        "data": {
            "tokenized": result,
            "most_common": most_common_word,
            "frequency": frequency,
        },
    }
    return context


@app.route("/get-topic-modeling/", methods=["POST"])
@cross_origin()
def analyze_response():
    sa_logger.info("get-topic-modeling")
    file_storage = request.files['file']
    print("topic_number : ", request.form['num_topic'])
    res = topic_modeling.analyze_csv(file_storage)
    context = {
        "id": "analyze-response",
        "data": {
            "df": res.to_string(),
        },
    }
    return context

@app.errorhandler(Exception)
@cross_origin()
def handling_exception(e):
    sa_logger.error('Exception: %s', (e))
    context = {
        "id": "error",
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

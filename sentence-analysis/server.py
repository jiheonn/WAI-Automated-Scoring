from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import bigram, topic_modeling
from utils.score import ScoreModel

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

file_path = './res/reference_data.csv'
sm = ScoreModel(file_path)

# Bigram Tree 분석
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


# 주제분석
@app.route("/get-topic-analysis/", methods=["POST"])
@cross_origin()
def get_topic_analysis():
    sa_logger.info("get-topic-analysis")
    file_storage = request.files['file']
    extension = request.form['extension']
    num_topic = int(request.form['num_topic'])
    version = request.form['version']

    # 토픽 모델링 분석
    topic_modeling_result, factorized_matrix_meta = topic_modeling.get_topic_modeling(file=file_storage, extension=extension, num_topic=num_topic)
    if topic_modeling_result is None:
        return "Wrong CSV format", 400

    # T-SNE 분석
    tsne_result = topic_modeling.get_tsne(factorized_matrix_meta, version=version)
    
    context = {
        "id": "topic-analysis",
        "data": {
            "topics": topic_modeling_result,
            "tsne": tsne_result,
        },
    }
    file_storage.close()
    return context


# 스코어 분석
@app.route("/get-sentence-score/", methods=["POST"])
@cross_origin()
def get_sentence_score():
    sa_logger.info("get-sentence-score")
    sentence = request.form['sentence']
    score = sm.get_score(sentence, option='normalized')
    context = {
        "id": "get-sentence-score",
        "data": {
            "score": score,
        },
    }
    return context


@app.errorhandler(Exception)
@cross_origin()
def handling_exception(e):
    print(e)
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

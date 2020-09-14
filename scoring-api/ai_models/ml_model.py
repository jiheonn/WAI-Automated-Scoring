import os
import re
import string

import dill as pickle
from konlpy.tag import Kkma

from flask import abort

kkma = Kkma()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
MODEL_DIR = os.path.join(APP_ROOT, 'model')


def load_model_dict(filepath):
    with open(filepath, 'rb') as file:
        model_dict = pickle.load(file)
    return model_dict


def clean_sentence(sentence, analyzer=';'):
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    sentence = str(sentence)
    sentence = re_punc.sub('', sentence).strip()

    if sentence:
        return analyzer.join([word for word, _ in kkma.pos(sentence)])
    else:
        return sentence


def predict(sentence, model):
    if model.predict_proba([sentence])[0][1] < 0.5:
        score = 0
    else:
        score = 1
    return score


def get_ml_score(question_id, sentence, model_dir=MODEL_DIR):
    filename = question_id + ".pkl"
    model_path = os.path.join(model_dir, filename)
    if not os.path.exists(model_path):
        abort(404, description="ML model ID '{}' is not exists.".format(question_id))
    model_dict = load_model_dict(model_path)
    sentence = clean_sentence(sentence)

    results = []
    for measure, model in model_dict.items():
        score = predict(sentence, model)
        results.append(score)

    return min(sum(results), 1)

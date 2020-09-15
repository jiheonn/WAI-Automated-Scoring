from konlpy.tag import Kkma
from db_models import MainpageQuestion
from flask import abort

kkma = Kkma()


def split_sentence(sentence):
    k = []
    for word, tag in sentence:
        if tag in ['NNG', 'VV', 'VA', 'NNP']:
            k.append(word)
    return k


def get_SAI_keywords(question_id):
    result = MainpageQuestion.query.filter(MainpageQuestion.question_id == question_id,
                                           MainpageQuestion.ml_model_check == 0).first()
    if not result:
        abort(404, description="SA model '{}' is not exist.".format(question_id))
    keywords = result.scoring_keyword.split()
    return keywords


def get_sa_score(question_id, answer):
    answer_set = set(split_sentence(kkma.pos(answer)))
    keyword_list = get_SAI_keywords(question_id)
    score = 0
    for i in keyword_list:
        k = kkma.pos(i)
        if answer.find(i) != -1:
            score += 1
        elif answer_set.issuperset(split_sentence(k)):
            score += 1

    return min(score, 1)

# coding: utf-8
from sqlalchemy import BigInteger, Column, Table, Text
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class MainpageQuestion(db.Model):
    __tablename__ = 'mainpage_question'

    question_id = db.Column(db.Integer, primary_key=True)
    question_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    hint = db.Column(db.Text, nullable=False)
    made_date = db.Column(db.Date, nullable=False)
    ques_concept = db.Column(db.Text, nullable=False)
    scoring_keyword = db.Column(db.Text)
    ml_model_check = db.Column(db.Integer)
    upload_check = db.Column(db.Integer)
    category_id = db.Column(db.Integer, nullable=False, index=True)


#
# t_mainpage_question = db.Table(
#     'mainpage_question',
#     db.Column('id', db.BigInteger, index=True),
#     db.Column('question_id', db.BigInteger),
#     db.Column('question_name', db.Text),
#     db.Column('discription', db.Text),
#     db.Column('answer', db.Text),
#     db.Column('image', db.Text),
#     db.Column('hint', db.Text),
#     db.Column('made_date', db.Text),
#     db.Column('ques_concept', db.Text),
#     db.Column('scoring_keyword', db.Text),
#     db.Column('category_id', db.BigInteger)
# )

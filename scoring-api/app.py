import os

from flask import Flask, request, abort
from flask_restplus import Api, Resource
from gevent.pywsgi import WSGIServer

from db_models import db
from ai_models import ml_model, sa_model

PORT = os.environ.get("FLASK_RUN_PORT", '5000')

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PW = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_URL = os.environ.get("POSTGRES_URL")
POSTGRES_DB = os.environ.get("POSTGRES_DB")



DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                               pw=POSTGRES_PW,
                                                               url=POSTGRES_URL,
                                                               db=POSTGRES_DB)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(app, version='1.0',
          title='WAI-Automated-Scoring API',
          description='WAI-Automated-Scoring')

api = api.namespace('', description='Scoring API')


@api.route('/<model_type>')
class Prediction(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Model is Not Exists'},
             params={'model_type': {'description': 'model type (ML/SA)',
                                    'in': 'path',
                                    'default': 'ML'},
                     'question_id': {'description': 'question ID',
                                     'in': 'query',
                                     'default': '1',
                                     'required': True},
                     'answer': {'description': 'student answer',
                                'in': 'query',
                                'default': None,
                                'required': True}
                     })
    def get(self, model_type):
        question_id = request.args.get('question_id')
        answer = request.args.get('answer')
        if not question_id:
            abort(400, description="Enter the question ID")
        if not answer:
            abort(400, description="Enter the answer")

        if model_type == 'ML':
            score = ml_model.get_ml_score(question_id, answer)
        elif model_type == 'SA':
            score = sa_model.get_sa_score(question_id, answer)
        else:
            abort(400, description="Choose between ML and SA")

        return {'model_type': model_type,
                'question_id': question_id,
                'answer': answer,
                'score': score}


if __name__ == '__main__':
    # app.run('0.0.0.0', debug=True)
    http_server = WSGIServer(('', PORT), app)
    http_server.serve_forever()

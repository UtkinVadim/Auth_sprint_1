from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app.config.from_object("config")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

from app import views, models

api.add_resource(views.HelloWorld, '/')
#api.add_resource(views.user.UserSignIn, '/api/v1/user/sign_in')
#api.add_resource(views.user.UserSignUp, '/api/v1/user/sign_up')

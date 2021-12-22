from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app.config.from_object("config")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api_app = Api(app)

from app import models
from app.api.v1 import user, hello_world, role

api_app.add_resource(hello_world.HelloWorld, '/')
api_app.add_resource(user.UserSignIn, '/api/v1/user/sign_in')
api_app.add_resource(user.UserSignUp, '/api/v1/user/sign_up')
api_app.add_resource(role.Role, '/api/v1/access/role')

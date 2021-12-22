from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES

app.config.from_object("config")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = JWT_REFRESH_TOKEN_EXPIRES

db = SQLAlchemy(app)
jwt = JWTManager(app)
api_app = Api(app)

from app import models
from app.api.v1 import user, hello_world, role

api_app.add_resource(hello_world.HelloWorld, '/')
api_app.add_resource(user.UserSignIn, '/api/v1/user/sign_in')
api_app.add_resource(user.UserSignUp, '/api/v1/user/sign_up')
api_app.add_resource(role.Role, '/api/v1/access/role')

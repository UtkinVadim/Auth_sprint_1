from flask import Flask
from flask_alembic import Alembic
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

redis_client = FlaskRedis(decode_responses=True)
alembic = Alembic()
jwt = JWTManager()


def create_app(test_config: dict = None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        app.config.from_object('config')
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    # TODO: Что тут неладно...
    jwt.init_app(app)

    redis_client.init_app(app)

    api = Api(app)

    from app.api.v1 import user, role

    api.add_resource(user.UserSignIn, '/api/v1/user/sign_in')
    api.add_resource(user.UserSignUp, '/api/v1/user/sign_up')
    api.add_resource(user.RefreshToken, '/api/v1/user/refresh')
    api.add_resource(user.Logout, '/api/v1/user/sign_out')
    api.add_resource(user.ChangeUserParams, '/api/v1/user/change')
    api.add_resource(user.UserHistory, '/api/v1/user/history')
    api.add_resource(user.RoleManipulation, '/api/v1/user/role')
    api.add_resource(role.Role, '/api/v1/access/role')

    return app

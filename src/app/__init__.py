from flask import Flask
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
redis_client = FlaskRedis(decode_responses=True)
jwt = JWTManager()


def create_app(test_config: dict = None) -> Flask:
    """
    Функция, создающая приложение на основе переданных конфигов, либо если конфиги не переданы - приложение
    создается используя конфиги из файла config.py.
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(SECRET_KEY="dev", SQLALCHEMY_TRACK_MODIFICATIONS=False)

    if test_config is None:
        app.config.from_object("config")
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    redis_client.init_app(app)

    api = Api(app)
    from app.api.v1.urls import urls

    for api_url in urls:
        api.add_resource(api_url[0], api_url[1])

    return app

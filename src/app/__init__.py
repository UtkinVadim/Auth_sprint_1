from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import redis
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES, REDIS_HOST, REDIS_PORT

app.config.from_object("config")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # гуглани

db = SQLAlchemy(app)
jwt = JWTManager(app)


from app import models
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) -> bool:
    """
    Проверяет наличие токена в редисе, если нет - значит токен истёк

    :param jwt_header:
    :param jwt_payload:
    :return:
    """
    if jwt_payload["type"] != 'refresh':
        return False
    jti = jwt_payload["jti"]
    token_in_redis = jwt_whitelist.get(jti)
    return token_in_redis is None


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = models.User.query.filter_by(login=identity).one_or_none()
    return user


api_app = Api(app)
jwt_whitelist = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

from app.api.v1 import user, hello_world, role

api_app.add_resource(hello_world.HelloWorld, '/')
api_app.add_resource(user.UserSignIn, '/api/v1/user/sign_in')
api_app.add_resource(user.UserSignUp, '/api/v1/user/sign_up')
api_app.add_resource(user.RefreshToken, '/api/v1/user/refresh')
api_app.add_resource(user.Logout, '/api/v1/user/sign_out')
api_app.add_resource(user.ChangeUserParams, '/api/v1/user/change')

api_app.add_resource(role.Role, '/api/v1/access/role')

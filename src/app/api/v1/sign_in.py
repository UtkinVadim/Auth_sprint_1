from http import HTTPStatus

from flask import jsonify
from flask import make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

from app import models
from app.redis import Redis


sign_in_parser = reqparse.RequestParser()
sign_in_parser.add_argument('login', dest='login', location='json', required=True, type=str, help='The user\'s login')
sign_in_parser.add_argument('password', dest='password', type=str, location='json', required=True,
                    help='The user\'s password')
sign_in_parser.add_argument('User-Agent', dest='fingerprint', location='headers')


class SignIn(Resource):
    redis_instance = Redis()
    """
    Класс для ручки логина пользователя.
    - параметры пользователя (логин, пароль...) находятся в args
    - с помощью args делается идентификация и аутентификация пользователя
    - если успешно, то логируется логин пользователя
    - из базы берутся роли пользователя
    - создаются access и refresh токены. В access токен кладутся роли пользователя
    - refresh токен кладётся в in-memory базу
    """
    def post(self):
        args = sign_in_parser.parse_args()
        user = models.User.check_user_by_login(args)
        if user:
            models.LoginHistory.log_sign_in(user, args['fingerprint'])
        else:
            return {'message': 'invalid credentials'}, HTTPStatus.UNAUTHORIZED
        user_roles_dict = models.User.get_user_roles(user_id=user.id)
        access_token = create_access_token(identity=user.id, additional_claims=user_roles_dict)
        refresh_token = create_refresh_token(identity=user.id)
        self.redis_instance.set_user_access_token(user_id=str(user.id), access_token=access_token)
        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK)
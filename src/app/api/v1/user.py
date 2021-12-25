import logging
from http import HTTPStatus

from flask import jsonify
from flask import make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt, get_jti, get_current_user
from flask_restful import fields, reqparse, Resource

from app import models, jwt_whitelist, jwt_with_role_required
from config import JWT_REFRESH_TOKEN_EXPIRES

logger = logging.getLogger(__name__)

login_pass_parser = reqparse.RequestParser()
login_pass_parser.add_argument('login', dest='login', location='json', required=True, type=str,
                               help='The user\'s login')
login_pass_parser.add_argument('password', dest='password', type=str, location='json', required=True,
                               help='The user\'s password')

user_info_parser = login_pass_parser.copy()
user_info_parser.add_argument('last_name', dest='last_name', location='json', required=False, type=str,
                              help='The user\'s last_name')
user_info_parser.add_argument('first_name', dest='first_name', location='json', required=False, type=str,
                              help='The user\'s first_name')
user_info_parser.add_argument('email', dest='email', type=str, location='json', required=True, help='The user\'s email')

login_pass_parser.add_argument('User-Agent', dest='fingerprint', location='headers')

user_signin_fields = {'login': fields.String, 'password': fields.String, 'fingerprint': fields.String}

user_params_parser = reqparse.RequestParser()
user_params_parser.add_argument('new_login', dest='new_login', location='json', required=True, type=str,
                                help='The user\'s login')
user_params_parser.add_argument('new_password', dest='new_password', type=str, location='json', required=True,
                                help='The user\'s password')

role_parser = reqparse.RequestParser()
role_parser.add_argument('user_id', dest='user_id', location='json', required=True, type=str, help='user_id')
role_parser.add_argument('role_id', dest='role_id', location='json', required=True, type=str, help='role_id')

user_signup_fields = {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'login': fields.String,
    'email': fields.String,
    'password': fields.String,
}


class UserSignUp(Resource):
    def post(self):
        args = user_info_parser.parse_args()
        user = models.User.is_login_exist(args)
        if user:
            return {'message': 'choose another login'}, HTTPStatus.CONFLICT
        models.User.create(args)
        return make_response(jsonify(message='user created successfully'), HTTPStatus.OK)


class UserSignIn(Resource):
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
        args = login_pass_parser.parse_args()
        user = models.User.check_user_by_login(args)
        if user:
            models.LoginHistory.log_sign_in(user, args['fingerprint'])
        else:
            return {'message': 'invalid credentials'}, HTTPStatus.UNAUTHORIZED
        user_roles_dict = models.User.get_user_roles(user_id=user.id)
        access_token = create_access_token(identity=user.id, additional_claims=user_roles_dict)
        refresh_token = create_refresh_token(identity=user.id)
        jti = get_jti(refresh_token)
        jwt_whitelist.set(jti, jti, ex=JWT_REFRESH_TOKEN_EXPIRES)
        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK)


class UserHistory(Resource):
    """
    Класс для ручки со списком логонов (успешных сеансов аутентификации) пользователя.

    """
    @jwt_required()
    def get(self):
        user = get_current_user()
        events = models.LoginHistory.get_user_events(user_id=user.id)
        return make_response(jsonify(events=events), HTTPStatus.OK)


class RefreshToken(Resource):
    """
    Класс для ручки обновления refresh токена
    - из токена берутся identity (id пользователя) и old_jti (id текущего refresh токена)
    - из in-memory базы удаляется из белого списка refresh токен
    - по identity собираются актуальные роли пользователя
    - формируется access токен, куда также кладутся роли пользователя и refresh токен
    - refresh токен кладётся в in-momory базу
    - пользователю возвращается пара access и refresh токенов
    """
    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt_identity()
        old_jti = get_jwt()['jti']
        jwt_whitelist.delete(old_jti)
        user_roles_dict = models.User.get_user_roles(user_id=identity)
        access_token = create_access_token(identity=identity, additional_claims=user_roles_dict)
        refresh_token = create_refresh_token(identity=identity)
        jti = get_jti(refresh_token)
        jwt_whitelist.set(jti, jti, ex=JWT_REFRESH_TOKEN_EXPIRES)
        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK)


class Logout(Resource):
    """
    Ручка для логаута пользователя.
    - из refresh токена берётся его id
    - и удаляется из белого списка хранящегося в in-memoru базе
    """
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()["jti"]
        jwt_whitelist.delete(jti)
        return jsonify(message="Refresh token revoked")


class ChangeUserParams(Resource):
    """
    Класс ручки для изменения параметров пользователя (логин+пароль)
    """
    @jwt_required()
    def post(self):
        args = user_params_parser.parse_args()
        user = get_current_user()
        if models.User.is_login_exist(args):
            return {'message': 'choose another login'}, HTTPStatus.CONFLICT
        models.User.change_user(user.id, args)
        return {'message': 'login&password successfully changed'}, HTTPStatus.OK


class RoleManipulation(Resource):
    """
    Класс ручки для добавления или удаления роли пользователю

    """
    @jwt_with_role_required('admin')
    def post(self):
        args = role_parser.parse_args()
        models.UserRole.add(args['user_id'], args['role_id'])
        return {'message': 'role added'}, HTTPStatus.OK

    @jwt_with_role_required('admin')
    def delete(self):
        args = role_parser.parse_args()
        models.UserRole.delete(args['user_id'], args['role_id'])
        return {'message': 'role deleted'}, HTTPStatus.OK

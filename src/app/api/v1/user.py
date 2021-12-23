import logging
from http import HTTPStatus

from flask import jsonify
from flask import make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt, get_jti, get_current_user
from flask_restful import fields, reqparse, Resource

from app import models, jwt_whitelist
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
        user = models.User.is_user_exist(args)
        if user:
            return {'message': 'choose another login'}, HTTPStatus.CONFLICT
        models.User.create(args)
        return make_response(jsonify(message='user created successfully'), HTTPStatus.OK)


class UserSignIn(Resource):
    def post(self):
        args = login_pass_parser.parse_args()
        user = models.User.check_user(args)
        if user:
            models.LoginHistory.log_sign_in(user, args['fingerprint'])
        else:
            return {'message': 'invalid credentials'}, HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=user.login)
        refresh_token = create_refresh_token(identity=user.login)
        jti = get_jti(refresh_token)
        jwt_whitelist.set(jti, jti, ex=JWT_REFRESH_TOKEN_EXPIRES)
        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK)


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        jti = get_jti(refresh_token)
        jwt_whitelist.set(jti, jti, ex=JWT_REFRESH_TOKEN_EXPIRES)
        return jsonify(access_token=access_token, refresh_token=refresh_token)


class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        jwt_whitelist.delete(jti)
        return jsonify(msg="Refresh token revoked")


class ChangeUserParams(Resource):
    @jwt_required()
    def post(self):
        args = user_params_parser.parse_args()
        user = get_current_user()
        models.User.change_user(user.id, args)
        return {'message': 'login&password successfully changed'}, HTTPStatus.OK

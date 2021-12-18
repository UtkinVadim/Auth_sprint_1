from flask_restful import fields, marshal_with, reqparse, Resource

from src.app.models import create_user, check_user, log_sign_in
import logging
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

user_signup_fields = {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'login': fields.String,
    'email': fields.String,
    'password': fields.String,
}


class UserInfo(Resource):
    def get(self):
        return {'message': 'user info'}


class UserRegistration(Resource):
    def post(self):
        return {'message': 'User registration'}


class UserSignUp(Resource):
    @marshal_with(user_signup_fields)
    def post(self):
        args = user_info_parser.parse_args()
        user = create_user(args)
        return user


class UserSignIn(Resource):
    @marshal_with(user_signin_fields)
    def post(self):
        args = login_pass_parser.parse_args()
        user = check_user(args)
        if user:
            log_sign_in(user, args['fingerprint'])
        return user

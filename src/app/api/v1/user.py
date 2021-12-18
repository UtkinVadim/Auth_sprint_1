from flask_restful import fields, marshal_with, reqparse, Resource

from src.app.models import create_user, check_user

post_parser = reqparse.RequestParser()
post_parser.add_argument('last_name', dest='last_name', location='json', required=False, type=str,
                         help='The user\'s last_name')
post_parser.add_argument('first_name', dest='first_name', location='json', required=False, type=str,
                         help='The user\'s first_name')
post_parser.add_argument('login', dest='login', location='json', required=True, type=str,
                         help='The user\'s login')
post_parser.add_argument('email', dest='email', type=str, location='json', required=True, help='The user\'s email')
post_parser.add_argument('password', dest='password', type=str, location='json', required=True,
                         help='The user\'s password')

user_signin_fields = {'login': fields.String, 'password': fields.String}

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
        args = post_parser.parse_args()
        user = create_user(args)
        return user


class UserSignIn(Resource):
    @marshal_with(user_signin_fields)
    def post(self):
        args = post_parser.parse_args()
        user = check_user(args)
        return user

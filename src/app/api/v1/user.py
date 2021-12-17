# from flask_restful import Resource, reqparse
# parser = reqparse.RequestParser()
# parser.add_argument('username', help='This field cannot be blank', required=True)
# parser.add_argument('password', help='This field cannot be blank', required=True)


from flask_restful import Resource

class UserInfo(Resource):
    def get(self):
        return {'message': 'user info'}


class UserRegistration(Resource):
    def post(self):
        return {'message': 'User registration'}


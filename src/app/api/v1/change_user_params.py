from http import HTTPStatus

from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource, reqparse

from app import models

user_params_parser = reqparse.RequestParser()
user_params_parser.add_argument(
    "new_login", dest="new_login", location="json", required=True, type=str, help="The user's login"
)
user_params_parser.add_argument(
    "new_password", dest="new_password", type=str, location="json", required=True, help="The user's password"
)


class ChangeUserParams(Resource):
    """
    Класс ручки для изменения параметров пользователя (логин+пароль)
    """

    @jwt_required()
    def post(self):
        args = user_params_parser.parse_args()
        user = get_current_user()
        if models.User.is_login_exist(args):
            return {"message": "choose another login"}, HTTPStatus.CONFLICT
        models.User.change_user(user.id, args)
        return {"message": "login&password successfully changed"}, HTTPStatus.OK

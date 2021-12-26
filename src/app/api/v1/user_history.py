from http import HTTPStatus

from flask import jsonify
from flask import make_response
from flask_jwt_extended import jwt_required, get_current_user
from flask_restful import Resource

from app import models


class UserHistory(Resource):
    """
    Класс для ручки со списком логонов (успешных сеансов аутентификации) пользователя.

    """

    @jwt_required()
    def get(self):
        user = get_current_user()
        events = models.LoginHistory.get_user_events(user_id=user.id)
        return make_response(jsonify(events=events), HTTPStatus.OK)

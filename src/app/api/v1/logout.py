from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource

from app.redis import Redis


class Logout(Resource):
    redis_instance = Redis()
    """
    Ручка для логаута пользователя.
    - из refresh токена берётся его id
    - и удаляется из белого списка хранящегося в in-memory базе
    """
    @jwt_required(refresh=True)
    def post(self):
        token = get_jwt()
        self.redis_instance.remove_user_token(token)
        return jsonify(message="Refresh token revoked")

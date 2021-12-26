from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource

from app import redis_client
from app.redis import Redis


class Logout(Resource):
    redis_instance = Redis()
    """
    Ручка для логаута пользователя.
    - из refresh токена берётся его id
    - и удаляется из белого списка хранящегося в in-memoru базе
    """
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()["jti"]
        redis_client.delete(jti)
        return jsonify(message="Refresh token revoked")

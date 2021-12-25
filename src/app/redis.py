from flask_jwt_extended import get_jti, get_jwt_identity
from flask_redis import FlaskRedis

from app import redis_client
from config import JWT_REFRESH_TOKEN_EXPIRES


class Redis:
    def __init__(self):
        self.redis_client: FlaskRedis = redis_client

    def set_user_access_token(self, user_id: str, access_token: str) -> None:
        key = self.generate_key(user_id, access_token)
        self.redis_client.set(key, access_token, ex=JWT_REFRESH_TOKEN_EXPIRES)

    def refresh_user_token(self, user_id: str, old_jwt: str, new_jwt: str):
        key = self.generate_key(user_id, old_jwt)
        self.redis_client.delete(key)
        self.set_user_access_token(user_id, new_jwt)

    @staticmethod
    def generate_key(user_id: str, access_token: str) -> str:
        jti = get_jti(access_token)
        return "::".join([user_id, jti])

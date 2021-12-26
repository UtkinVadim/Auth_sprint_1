from typing import Union

from flask_jwt_extended import get_jti, get_jwt_identity
from flask_redis import FlaskRedis

from app import redis_client
from config import JWT_REFRESH_TOKEN_EXPIRES


class Redis:
    def __init__(self):
        self.redis_client: FlaskRedis = redis_client

    def set_user_refresh_token(self, user_id: str, refresh_token: str) -> None:
        key = self.generate_key(user_id, refresh_token)
        self.redis_client.set(key, refresh_token, ex=JWT_REFRESH_TOKEN_EXPIRES)

    def refresh_user_token(self, user_id: str, old_jwt: dict, new_jwt: str):
        key = "::".join([old_jwt["sub"], old_jwt["jti"]])
        self.redis_client.delete(key)
        self.set_user_refresh_token(user_id, new_jwt)

    def remove_user_token(self, refresh_token: dict) -> None:
        jti = refresh_token["jti"]
        user_id = refresh_token["sub"]
        key = "::".join([user_id, jti])
        self.redis_client.delete(key)

    def token_is_revoked(self, user_id: str, jti: str) -> bool:
        key = "::".join([user_id, jti])
        result = self.redis_client.get(key)
        if not result:
            return True
        return False

    @staticmethod
    def generate_key(user_id: str, refresh_token: Union[str, dict]) -> str:
        jti = get_jti(refresh_token)
        return "::".join([user_id, jti])

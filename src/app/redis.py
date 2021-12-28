from flask_jwt_extended import get_jti
from flask_redis import FlaskRedis

from app import redis_client
from config import JWT_REFRESH_TOKEN_EXPIRES


class Redis:
    def __init__(self):
        self.redis_client: FlaskRedis = redis_client

    def set_user_refresh_token(self, user_id: str, refresh_token: str) -> None:
        """
        Метод, для записи токена пользователя.
        """
        jti = get_jti(refresh_token)
        key = self.generate_redis_key(user_id, jti)
        self.redis_client.set(key, refresh_token, ex=JWT_REFRESH_TOKEN_EXPIRES)

    def refresh_user_token(self, user_id: str, old_jwt: dict, new_jwt: str):
        """
        Метод для обновления токена пользователя.
        """
        self.remove_user_token(old_jwt)
        self.set_user_refresh_token(user_id, new_jwt)

    def remove_user_token(self, refresh_token: dict) -> None:
        """
        Метод для удаления токена пользователя.
        """
        jti = refresh_token["jti"]
        user_id = refresh_token["sub"]
        key = self.generate_redis_key(user_id, jti)
        self.redis_client.delete(key)

    def remove_all_user_tokens(self, refresh_token: dict) -> None:
        """
        Метод для удаления всех токенов принадлежащих пользователю.
        """
        user_id = refresh_token["sub"]
        for key in self.redis_client.scan_iter(f"{user_id}::*"):
            self.redis_client.delete(key)

    def token_is_revoked(self, user_id: str, jti: str) -> bool:
        """
        Метод для проверки токена пользователя на наличие в redis.
        """
        key = self.generate_redis_key(user_id, jti)
        result = self.redis_client.get(key)
        if not result:
            return True
        return False

    @staticmethod
    def generate_redis_key(user_id: str, jti: str) -> str:
        """
        Метод для генерации ключа для redis.
        """
        return "::".join([user_id, jti])

from http import HTTPStatus

from flask_jwt_extended import get_jti

from app.models import User
from app.tests.testing_data import USER_DATA
from app.tests.base_auth_test_case import BaseAuthTestCase


class SignInTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        self.client.post("/api/v1/user/sign_up", json=USER_DATA)

    def test_user_sign_in(self):
        response = self.client.post(self.sign_in_url, json=USER_DATA)
        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.json
        assert "refresh_token" in response.json

    def test_wrong_sign_in_data(self):
        data = {"login": "fake_login", "password": "fake_password"}
        response = self.client.post(self.sign_in_url, json=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        expected_details = {'message': 'invalid credentials'}
        assert response.json == expected_details

    def test_check_token_in_redis(self):
        self.clear_redis_cache()
        response = self.client.post(self.sign_in_url, json=USER_DATA)
        assert response.status_code == HTTPStatus.OK
        user = User.query.filter_by(login=USER_DATA.get("login")).first()
        access_token = response.json["access_token"]
        jti = get_jti(access_token)
        redis_key = f"{user.id}::{jti}"
        result = self.redis_client.get(redis_key)
        assert result == access_token

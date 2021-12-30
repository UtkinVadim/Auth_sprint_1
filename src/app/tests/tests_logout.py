from http import HTTPStatus

from app.tests.base_auth_test_case import BaseAuthTestCase


class LogOutTestCase(BaseAuthTestCase):
    url = "/api/v1/user/sign_out"

    def setUp(self):
        super().setUp()
        self.authorize_client()

    def test_logout(self):
        token_in_redis = self.get_token_from_redis()
        assert token_in_redis
        response = self.client.post(self.url, headers=self.headers_refresh)
        assert response.status_code == HTTPStatus.OK
        expected_response = {"message": "Refresh token revoked"}
        assert response.json == expected_response
        token_in_redis = self.get_token_from_redis()
        assert not token_in_redis

    def test_logout_from_all_places(self):
        token_in_redis = self.get_token_from_redis()
        assert token_in_redis
        data = {"form_all_places": True}
        response = self.client.post(self.url, headers=self.headers_refresh, json=data)
        assert response.status_code == HTTPStatus.OK
        expected_response = {"message": "All user tokens revoked"}
        assert response.json == expected_response
        token_in_redis = self.get_token_from_redis()
        assert not token_in_redis

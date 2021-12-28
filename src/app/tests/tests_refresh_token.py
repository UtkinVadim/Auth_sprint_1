from http import HTTPStatus

from app.tests.base_auth_test_case import BaseAuthTestCase


class RefreshTokenTestCase(BaseAuthTestCase):
    url = "/api/v1/user/refresh"

    def setUp(self):
        super().setUp()
        self.authorize_client()

    def test_refresh_access_token(self):
        old_access_token = self.access_token
        old_refresh_token = self.refresh_token
        response = self.client.get(self.url, headers=self.headers_refresh)
        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.json
        assert "refresh_token" in response.json
        assert response.json["access_token"] != old_access_token
        assert response.json["refresh_token"] != old_refresh_token

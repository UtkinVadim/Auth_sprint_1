from http import HTTPStatus

from app.tests.base_auth_test_case import BaseAuthTestCase
from app.tests.testing_data import USER_DATA, USER_NEW_LOGIN, USER_NEW_PASSWORD


class SignInTestCase(BaseAuthTestCase):
    url = "/api/v1/user/change"

    def setUp(self):
        super().setUp()
        self.client.post(self.sign_up_url, json=USER_DATA)
        response = self.client.post(self.sign_in_url, json=USER_DATA)
        self.refresh_token = response.json["refresh_token"]
        self.access_token = response.json["access_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.headers_refresh = {"Authorization": f"Bearer {self.refresh_token}"}

    def test_change_login(self):
        response = self.client.post(self.url, headers=self.headers, json=USER_NEW_LOGIN)
        assert response.json == {"message": "successfully changed"}
        response = self.client.post(self.sign_out_url, headers=self.headers_refresh)
        assert response.json == {"message": "Refresh token revoked"}
        response = self.client.post(self.sign_in_url, json=USER_DATA | USER_NEW_LOGIN)
        assert response.status_code == HTTPStatus.OK

    def test_change_password(self):
        response = self.client.post(self.url, headers=self.headers, json=USER_NEW_PASSWORD)
        assert response.json == {"message": "successfully changed"}
        response = self.client.post(self.sign_out_url, headers=self.headers_refresh)
        assert response.json == {"message": "Refresh token revoked"}
        response = self.client.post(self.sign_in_url, json=USER_DATA | USER_NEW_PASSWORD)
        assert response.status_code == HTTPStatus.OK

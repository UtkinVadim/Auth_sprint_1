from http import HTTPStatus

from app.tests.base_auth_test_case import BaseAuthTestCase


class LogOutTestCase(BaseAuthTestCase):
    logout_url = "/api/v1/user/sign_out"

    def setUp(self):
        super().setUp()
        self.authorize_client()

    def test_logout(self):
        response = self.client.post(self.logout_url, headers=self.headers)
        print(response.json)

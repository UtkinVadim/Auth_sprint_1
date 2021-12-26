from app.tests.base_auth_test_case import BaseAuthTestCase


class RefreshTokenTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        self.authorize_client()

    def test_refresh_access_token(self):
        headers = {"Authorization": f"Bearer {self.refresh_token}"}
        response = self.client.get(self.refresh_token_url, headers=headers)
        # TODO: {'message': 'The token has been revoked.'}

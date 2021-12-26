from http import HTTPStatus

from app.tests.base_auth_test_case import BaseAuthTestCase


class HistoryTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        self.authorize_client()

    def test_get_history(self):
        response = self.client.get(self.history_url, headers=self.headers)
        assert response.status_code == HTTPStatus.OK
        events = response.json["events"]
        assert len(events) == 1
        assert events[0].get("user_id") == str(self.user.id)
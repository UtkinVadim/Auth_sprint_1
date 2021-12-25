from http import HTTPStatus

from app.tests.base_auth_test_case import BaseAuthTestCase
from app.tests.testing_data import USER_DATA, ROLE_DATA


class RoleTestCase(BaseAuthTestCase):
    sign_in = "/api/v1/access/role"

    def setUp(self):
        super().setUp()
        self.client.post("/api/v1/user/sign_up", json=USER_DATA)

    def test_create_role(self):
        pass

    def test_role_already_exists(self):
        pass

    def test_get_all_roles(self):
        pass

    def test_update_role(self):
        pass

    def test_delete_role(self):
        pass

    def test_check_roles_api_permission(self):
        pass

    def test_add_role_to_user(self):
        pass

    def test_remove_user_role(self):
        pass

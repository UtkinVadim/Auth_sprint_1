from http import HTTPStatus

from app.models import Role
from app.tests.base_auth_test_case import BaseAuthTestCase
from app.tests.testing_data import ROLE_DATA


class RoleTestCase(BaseAuthTestCase):
    url = "/api/v1/access/role"

    def setUp(self):
        super().setUp()
        self.authorize_client()

    def test_create_role(self):
        response = self.client.post(self.url, headers=self.headers, json=ROLE_DATA)
        assert response.status_code == HTTPStatus.CREATED
        expected_response = {"message": "role created"}
        assert response.json == expected_response
        created_role: Role = Role.query.filter_by(title=ROLE_DATA.get("title")).first()
        assert created_role
        assert created_role.title == ROLE_DATA.get("title")

    def test_role_already_exists(self):
        Role.create(title=ROLE_DATA.get("title"))
        response = self.client.post(self.url, headers=self.headers, json=ROLE_DATA)
        assert response.status_code == HTTPStatus.CONFLICT
        expected_response = {"message": "role already exists"}
        assert response.json == expected_response

    def test_get_all_roles(self):
        role_1 = Role.create(title="role 1")
        role_2 = Role.create(title="role 2")
        response = self.client.get(self.url, headers=self.headers)
        assert response.status_code == HTTPStatus.OK
        expected_response = {
            "roles": [
                {"id": str(self.role.id), "title": "admin"},
                {"id": str(role_1.id), "title": "role 1"},
                {"id": str(role_2.id), "title": "role 2"},
            ]
        }
        assert response.json == expected_response

    def test_update_role(self):
        old_title = "old_title"
        new_title = "new_title"
        role = Role.create(title=old_title)
        data = {"title": old_title, "new_title": new_title}
        response = self.client.patch(self.url, headers=self.headers, json=data)
        assert response.status_code == HTTPStatus.OK
        expected_response = {"message": "role updated"}
        assert response.json == expected_response
        assert role.title == new_title

    def test_updating_role_does_not_exists(self):
        data = {"title": "fake_role", "new_title": "new_title"}
        response = self.client.patch(self.url, headers=self.headers, json=data)
        assert response.status_code == HTTPStatus.CONFLICT
        expected_response = {"message": "role does not exist"}
        assert response.json == expected_response

    def test_delete_role(self):
        title = "unused_role"
        Role.create(title=title)
        data = {"title": title}
        response = self.client.delete(self.url, headers=self.headers, json=data)
        assert response.status_code == HTTPStatus.OK
        expected_response = {"message": "role deleted"}
        assert response.json == expected_response
        role: Role = Role.query.filter_by(title=title).first()
        assert not role

    def test_deleting_role_does_not_exists(self):
        data = {"title": "fake_role"}
        response = self.client.delete(self.url, headers=self.headers, json=data)
        assert response.status_code == HTTPStatus.CONFLICT
        expected_response = {"message": "role does not exist"}
        assert response.json == expected_response

    def test_check_roles_api_permission(self):
        sign_up_data = {"login": "Nikola", "password": "Nikola123", "email": "nikola@nikola.com"}
        self.client.post(self.sign_up_url, json=sign_up_data)
        access_token = self.client.post(self.sign_in_url, json=sign_up_data).json["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.get(self.url, headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN
        expected_response = {"message": "you shall not pass"}
        assert response.json == expected_response

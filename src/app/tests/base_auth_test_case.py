from flask_testing import TestCase

from app import create_app, db, redis_client
from app.models import User
from app.tests.testing_data import USER_DATA
from config import (
    TEST_DB_USER,
    TEST_DB_PASSWORD,
    TEST_DB_HOST,
    TEST_DB_PORT,
    TEST_DB,
    TEST_REDIS_HOST,
    TEST_REDIS_PORT
)


class BaseAuthTestCase(TestCase):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB}"
    REDIS_URL = f"redis://{TEST_REDIS_HOST}:{TEST_REDIS_PORT}/0"
    TESTING = True

    sign_up_url = "/api/v1/user/sign_up"
    sign_in_url = "/api/v1/user/sign_in"
    history_url = "/api/v1/user/history"
    refresh_token_url = "/api/v1/user/refresh"

    def create_app(self):
        test_config = {"SQLALCHEMY_DATABASE_URI": self.SQLALCHEMY_DATABASE_URI,
                       "TESTING": True,
                       "REDIS_URL": self.REDIS_URL}
        return create_app(test_config)

    def setUp(self):
        self.db = db
        self.redis_client = redis_client
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.clear_redis_cache()

    def clear_redis_cache(self):
        for key in self.redis_client.scan_iter("*"):
            self.redis_client.delete(key)

    def authorize_client(self):
        self.client.post(self.sign_up_url, json=USER_DATA)
        self.user = User.query.filter_by(login=USER_DATA.get("login")).first()
        response = self.client.post(self.sign_in_url, json=USER_DATA)
        self.access_token = response.json["access_token"]
        self.refresh_token = response.json["refresh_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

import pytest
from flask import url_for

from app import app as app_instance


@pytest.fixture
def app():
    return app_instance


def test_app(client):
    assert client.get(url_for('hello_world')).status_code == 200

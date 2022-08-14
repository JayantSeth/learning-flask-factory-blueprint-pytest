from application import create_app
import pytest
from models.user import User
from models.author import Author
import json


@pytest.fixture
def app():
    app = create_app("TESTING")
    return app


@pytest.fixture
def new_user(app):
    with app.app_context():
        user = User(username="test", password="test", email="test@example.com")
        user.save_to_db()
        yield user


@pytest.fixture
def new_author(new_user):
    author = Author(name="test", age=30)
    author.save_to_db()
    return author


@pytest.fixture(scope="module")
def headers():
    return {"Content-Type": "application/json"}


@pytest.fixture
def login_request(client, new_user, headers):
    response = client.post("/auth/signin", data=json.dumps({"username": new_user.username, "password": "test"}), headers=headers)
    return response.json


@pytest.fixture
def auth_headers(headers, login_request):
    headers["Authorization"] = f"Bearer {login_request['access_token']}"
    return headers

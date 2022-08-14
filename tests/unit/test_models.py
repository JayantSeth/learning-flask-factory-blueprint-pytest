from models.user import User
import bcrypt
from application import create_app


def test_new_user(new_user):
    """
    Given a user model
    When a new user is created
    Then username and email field should be correctly defined
    :return:
    """
    username = "test"
    password = "test"
    email = "test@example.com"
    assert new_user.username == username
    assert new_user.email == email
    assert bcrypt.checkpw(password.encode("utf-8"), new_user.password_hash)


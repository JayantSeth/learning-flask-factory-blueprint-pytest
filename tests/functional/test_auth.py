import json


def test_signup(client, headers):
    """
    Given the flask application configured for testing
    When post request is sent to /signup with correct params
    Then user should be registered
    :return:
    """
    response = client.post('/auth/signup', data=json.dumps({"username": "test123", "password": "test123",
                                                            "email": "test123@example.com"}),
                           headers=headers)
    with open("output.txt", "w+") as f:
        f.write(json.dumps(response.json))
    assert response.status_code == 200
    assert "message" in response.json


def test_signin(client, new_user, headers):
    assert new_user.username == "test"
    response = client.post('/auth/signin', data=json.dumps({"username": "test", "password": "test"}), headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_refresh_token(client, login_request, headers):
    headers["Authorization"] = f"Bearer {login_request['refresh_token']}"
    response = client.post('/auth/refresh_token', data=json.dumps({}), headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json

import json


def test_get_authors(client, auth_headers):
    response = client.get("/api/authors", headers=auth_headers)
    assert response.status_code == 200


def test_post_author(client, auth_headers):
    author = {"name": "test", "age": 28}
    response = client.post("/api/author/test", data=json.dumps(author), headers=auth_headers)
    assert response.status_code == 200


def test_get_author(client, new_author, auth_headers):
    response = client.get("/api/author/test", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["author"]["name"] == new_author.name
    assert response.json["author"]["age"] == new_author.age


def test_put_author(client, new_author, auth_headers):
    new_author_data = {"name": "new_test", "age": 35}
    response = client.put(f"/api/author/{new_author.name}", data=json.dumps(new_author_data), headers=auth_headers)
    assert response.status_code == 200
    response = client.get("/api/author/new_test", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["author"]["age"] == 35


def test_delete_author(client, new_author, new_user, login_request, headers):
    fresh_headers = headers.copy()
    refresh_token = login_request["refresh_token"]
    headers["Authorization"] = f"Bearer {refresh_token}"
    login_resp = client.post(f"/auth/refresh_token", data=json.dumps({}), headers=headers)
    assert "access_token" in login_resp.json
    access_token = login_resp.json["access_token"]
    headers["Authorization"] = f"Bearer {access_token}"
    response = client.delete(f"/api/author/{new_author.name}", headers=headers)
    assert response.status_code == 500
    login_resp = client.post(f"/auth/signin", data=json.dumps({"username": new_user.username,
                                                               "password": "test"}), headers=fresh_headers)
    assert login_resp.status_code == 200
    headers["Authorization"] = f"Bearer {login_resp.json['access_token']}"
    response = client.delete(f"/api/author/{new_author.name}", headers=headers)
    assert response.status_code == 200
    response = client.get(f"/api/author/{new_author.name}", headers=headers)
    assert response.status_code == 404


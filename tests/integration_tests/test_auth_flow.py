class TestAuthFlow:
    def test_sign_up(self, client):
        request_body = {
            "username": "user1",
            "email": "example@gmail.com",
            "password": "password",
        }

        resp = client.post("/auth/sign-up", json=request_body)
        assert resp.status_code == 200
        assert resp.json()['token_type'] == "bearer"
        assert resp.json()['access_token'] is not None

    def test_sign_up_when_user_already_exists_with_email(self, client):
        request_body = {
            "username": "user1",
            "email": "example@gmail.com",
            "password": "password",
        }
        client.post("/auth/sign-up", json=request_body)

        request_body = {
            "username": "user2",
            "email": "example@gmail.com",
            "password": "new-password",
        }
        response = client.post("/auth/sign-up", json=request_body)
        assert response.status_code == 400
        assert response.json()['detail'] == "User already exists with same email"

    def test_login(self, client):
        request_body = {
            "username": "user1",
            "email": "example@gmail.com",
            "password": "password",
        }
        client.post("/auth/sign-up", json=request_body)

        request_body = {
            "username": "example@gmail.com",
            "password": "password"
        }
        response = client.post("/auth/login", data=request_body)
        assert response.status_code == 200
        assert response.json()['token_type'] == "bearer"
        assert response.json()['access_token'] is not None

    def test_login_when_user_not_found(self, client):
        request_body = {
            "username": "dummy@gmail.com",
            "password": "password"
        }
        response = client.post("/auth/login", data=request_body)
        assert response.status_code == 404
        assert response.json()['detail'] == "User not found"

    def test_login_when_password_mismatch(self, client):
        request_body = {
            "username": "user1",
            "email": "example@gmail.com",
            "password": "password",
        }
        client.post("/auth/sign-up", json=request_body)

        request_body = {
            "username": "example@gmail.com",
            "password": "dummy_password"
        }
        response = client.post("/auth/login", data=request_body)
        assert response.status_code == 404
        assert response.json()['detail'] == "password mismatch"

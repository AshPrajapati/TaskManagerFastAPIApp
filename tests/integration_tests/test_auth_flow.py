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

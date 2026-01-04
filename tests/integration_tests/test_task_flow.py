from starlette.testclient import TestClient


class TestTaskFlow:
    def test_create_task(self, authenticated_client: TestClient):
        request_body = {
            "title": "task1",
            "description": "task1 description",
            "status": "pending",
            "priority": "low"
        }
        response = authenticated_client.post("/tasks", json=request_body)
        assert response.status_code == 200
        assert response.json()["title"] == "task1"
        assert response.json()["description"] == "task1 description"
        assert response.json()["status"] == "pending"
        assert response.json()["priority"] == "low"

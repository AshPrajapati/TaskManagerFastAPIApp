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

    def test_get_all_tasks(self, authenticated_client: TestClient, seeded_tasks):
        response = authenticated_client.get("/tasks")
        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) == 2

    def test_get_task_by_id(self, authenticated_client: TestClient, seeded_tasks):
        response = authenticated_client.get("/tasks/1")

        assert response.status_code == 200
        body = response.json()
        assert body["task_id"] == 1
        assert body["title"] == "task1"

    def test_get_task_by_id_not_found(self, authenticated_client: TestClient, seeded_tasks):
        response = authenticated_client.get("/tasks/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

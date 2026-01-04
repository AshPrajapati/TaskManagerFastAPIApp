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
        task_id = seeded_tasks[0]
        response = authenticated_client.get(f"/tasks/{task_id}")

        assert response.status_code == 200
        body = response.json()
        assert body["task_id"] == task_id
        assert body["title"] == "task1"

    def test_get_task_by_id_not_found(self, authenticated_client: TestClient, seeded_tasks):
        response = authenticated_client.get("/tasks/9999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_update_task(self, authenticated_client: TestClient, seeded_tasks):
        request_body = {
            "title": "updated_task",
            "priority": "high",
            "status": "in_progress",
        }
        task_id = seeded_tasks[0]
        response = authenticated_client.put(f"/tasks/{task_id}", json=request_body)
        assert response.status_code == 200
        assert response.json()["title"] == "updated_task"
        assert response.json()["priority"] == "high"
        assert response.json()["status"] == "in_progress"

    def test_update_task_not_found(self, authenticated_client: TestClient, seeded_tasks):
        request_body = {
            "title": "updated_task",
            "priority": "high",
            "status": "in_progress",
        }
        response = authenticated_client.put("/tasks/9999", json=request_body)
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_delete_task(self, authenticated_client: TestClient, seeded_tasks):
        task_id = seeded_tasks[0]
        response = authenticated_client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

        task_response = authenticated_client.get(f"/tasks/{task_id}")
        assert task_response.status_code == 404
        assert task_response.json()["detail"] == "Task not found"

    def test_delete_task_not_found(self, authenticated_client: TestClient, seeded_tasks):
        response = authenticated_client.delete("/tasks/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found to delete"

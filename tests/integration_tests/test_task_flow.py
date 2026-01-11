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

    def test_get_tasks_with_filters_sort_and_pagination(self, authenticated_client: TestClient, seeded_tasks_get_all_tasks):
        response = authenticated_client.get(
            "/tasks?page=1&size=1&status=pending&priority=low&search=buy&sort_by=title&order=asc"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["size"] == 1
        assert data["total"] == 2
        assert data["total_pages"] == 2
        assert data["tasks"][0]["title"] == "Buy groceries"

    def test_get_tasks_second_page(self, authenticated_client, seeded_tasks_get_all_tasks):
        response = authenticated_client.get(
            "/tasks?page=2&size=1&status=pending&priority=low&search=buy&sort_by=title&order=asc"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["size"] == 1
        assert data["total"] == 2
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Buy milk"

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

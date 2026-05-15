from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_root_returns_metadata(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["data"]["docs"] == "/api/v1/docs"
    assert "x-request-id" in response.headers


def test_health_returns_healthy(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["data"]["status"] == "healthy"


def test_list_users_initially_empty(client: TestClient) -> None:
    response = client.get("/api/v1/users")

    assert response.status_code == 200
    assert response.json()["data"] == []


def test_create_and_get_user(client: TestClient) -> None:
    email = f"ada-{uuid4().hex}@example.com"

    create_response = client.post(
        "/api/v1/users",
        json={"name": "Ada Lovelace", "email": email},
    )

    assert create_response.status_code == 201
    created = create_response.json()["data"]
    assert created["name"] == "Ada Lovelace"
    assert created["email"] == email

    get_response = client.get(f"/api/v1/users/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["data"]["id"] == created["id"]


def test_update_user(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/users",
        json={"name": "Alan Turing", "email": f"alan-{uuid4().hex}@example.com"},
    )
    user_id = create_response.json()["data"]["id"]

    update_response = client.patch(f"/api/v1/users/{user_id}", json={"name": "A. Turing"})

    assert update_response.status_code == 200
    assert update_response.json()["data"]["name"] == "A. Turing"


def test_delete_user(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/users",
        json={"name": "Grace Hopper", "email": f"grace-{uuid4().hex}@example.com"},
    )
    user_id = create_response.json()["data"]["id"]

    delete_response = client.delete(f"/api/v1/users/{user_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["data"] == {"deleted": True}

    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


def test_duplicate_email_returns_409(client: TestClient) -> None:
    email = f"duplicate-{uuid4().hex}@example.com"

    first_response = client.post("/api/v1/users", json={"name": "One", "email": email})
    second_response = client.post("/api/v1/users", json={"name": "Two", "email": email})

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["error"]["code"] == "CONFLICT"


def test_invalid_json_returns_400(client: TestClient) -> None:
    response = client.post(
        "/api/v1/users",
        content='{ "name": "Broken", ',
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_JSON"


def test_validation_error_returns_422(client: TestClient) -> None:
    response = client.post("/api/v1/users", json={"name": "", "email": "bad-email"})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_unknown_route_returns_404(client: TestClient) -> None:
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_unsupported_method_returns_405(client: TestClient) -> None:
    response = client.put("/health")

    assert response.status_code == 405
    assert response.json()["error"]["code"] == "METHOD_NOT_ALLOWED"

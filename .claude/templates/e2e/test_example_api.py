"""Example API contract E2E tests using httpx and factories.

These tests demonstrate the pattern for writing API E2E tests.
They require a running application server at BASE_URL.

Run:
    BASE_URL=http://localhost:8000 pytest tests/e2e/test_example_api.py -m e2e
"""

from __future__ import annotations

import httpx
import pytest
from tests.e2e.factories.user_factory import UserDataFactory


@pytest.mark.e2e
class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_200(self, api_client: httpx.Client) -> None:
        """Health endpoint should return HTTP 200."""
        response = api_client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self, api_client: httpx.Client) -> None:
        """Health endpoint should return a JSON body with status field."""
        response = api_client.get("/health")
        body = response.json()
        assert "status" in body
        assert body["status"] == "ok"

    def test_health_content_type(self, api_client: httpx.Client) -> None:
        """Health endpoint should return application/json content type."""
        response = api_client.get("/health")
        assert "application/json" in response.headers.get("content-type", "")


@pytest.mark.e2e
class TestExampleCrudFlow:
    """Tests for a hypothetical CRUD API flow."""

    def test_create_and_read_item(self, api_client: httpx.Client) -> None:
        """Creating an item via POST should allow reading it via GET."""
        user_data = UserDataFactory()

        create_response = api_client.post("/api/users", json=user_data)
        assert create_response.status_code == 201

        created = create_response.json()
        user_id = created["id"]

        get_response = api_client.get(f"/api/users/{user_id}")
        assert get_response.status_code == 200

        fetched = get_response.json()
        assert fetched["name"] == user_data["name"]
        assert fetched["email"] == user_data["email"]

    def test_invalid_payload_returns_422(self, api_client: httpx.Client) -> None:
        """Sending an invalid payload should return 422 Unprocessable Entity."""
        response = api_client.post("/api/users", json={})
        assert response.status_code == 422

import hashlib
import hmac
import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app  # Assuming your FastAPI app instance is named 'app'


@pytest.fixture
def client():
    return TestClient(app)


WEBHOOK_SECRET = "test_secret"
WEBHOOK_URL = "/api/v1/notion/webhooks/"


def generate_signature(payload: bytes, secret: str) -> str:
    return hmac.new(key=secret.encode(), msg=payload, digestmod=hashlib.sha256).hexdigest()


@patch("app.core.integrations.notion.webhooks.tasks.process_webhook_event.delay")
@patch("app.core.config.settings.NOTION_WEBHOOK_SECRET", WEBHOOK_SECRET)
def test_handle_webhook_success(mock_process_webhook, client: TestClient):
    """Test successful webhook handling with a valid signature."""
    payload = {"event_type": "page.updated", "data": {"page_id": "1234"}}
    payload_bytes = json.dumps(payload).encode()
    signature = generate_signature(payload_bytes, WEBHOOK_SECRET)

    response = client.post(
        WEBHOOK_URL,
        content=payload_bytes,
        headers={"X-Notion-Signature": signature, "Content-Type": "application/json"},
    )

    assert response.status_code == 202
    assert response.json() == {"status": "received"}
    mock_process_webhook.assert_called_once_with(payload)


@patch("app.core.config.settings.NOTION_WEBHOOK_SECRET", WEBHOOK_SECRET)
def test_handle_webhook_invalid_signature(client: TestClient):
    """Test webhook handling with an invalid signature."""
    payload = {"event_type": "page.created", "data": {}}
    payload_bytes = json.dumps(payload).encode()

    response = client.post(
        WEBHOOK_URL,
        content=payload_bytes,
        headers={
            "X-Notion-Signature": "invalid_signature",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400
    assert "Invalid webhook signature" in response.text


@patch("app.core.config.settings.NOTION_WEBHOOK_SECRET", None)
def test_handle_webhook_no_secret_configured(client: TestClient):
    """Test webhook handling when the secret is not configured on the server."""
    payload = {"event_type": "page.deleted", "data": {}}
    payload_bytes = json.dumps(payload).encode()

    response = client.post(
        WEBHOOK_URL,
        content=payload_bytes,
        headers={
            "X-Notion-Signature": "any_signature",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 500
    assert "Webhook secret is not configured" in response.text

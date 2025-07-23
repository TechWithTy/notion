from unittest.mock import AsyncMock, patch

import pytest

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.exceptions import NotionAPIError


@pytest.mark.asyncio
@patch("app.core.integrations.notion.client.httpx.AsyncClient")
async def test_list_users_success(mock_async_client):
    """Test successful listing of users."""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "object": "list",
        "results": [{"object": "user", "id": "some-user-id", "name": "Test User"}],
        "next_cursor": None,
        "has_more": False,
    }
    mock_async_client.return_value.__aenter__.return_value.request.return_value = (
        mock_response
    )

    client = AsyncNotionClient(token="test-token")
    users_response = await client.list_users()

    assert users_response.object == "list"
    assert len(users_response.results) == 1
    assert users_response.results[0].name == "Test User"


@pytest.mark.asyncio
@patch("app.core.integrations.notion.client.httpx.AsyncClient")
async def test_get_user_success(mock_async_client):
    """Test successful retrieval of a single user."""
    user_id = "some-user-id"
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "object": "user",
        "id": user_id,
        "name": "Specific User",
    }
    mock_async_client.return_value.__aenter__.return_value.request.return_value = (
        mock_response
    )

    client = AsyncNotionClient(token="test-token")
    user = await client.get_user(user_id)

    assert user.id == user_id
    assert user.name == "Specific User"


@pytest.mark.asyncio
@patch("app.core.integrations.notion.client.httpx.AsyncClient")
async def test_get_me_success(mock_async_client):
    """Test successful retrieval of the bot user."""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "object": "user",
        "id": "bot-id",
        "name": "My Bot",
        "type": "bot",
    }
    mock_async_client.return_value.__aenter__.return_value.request.return_value = (
        mock_response
    )

    client = AsyncNotionClient(token="test-token")
    bot_user = await client.get_me()

    assert bot_user.id == "bot-id"
    assert bot_user.type == "bot"


@pytest.mark.asyncio
@patch("app.core.integrations.notion.client.httpx.AsyncClient")
async def test_user_endpoints_api_error(mock_async_client):
    """Test Notion API error handling for user endpoints."""
    mock_response = AsyncMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"code": "invalid_request", "message": "Error"}
    mock_async_client.return_value.__aenter__.return_value.request.return_value = (
        mock_response
    )

    client = AsyncNotionClient(token="test-token")

    with pytest.raises(NotionAPIError):
        await client.list_users()

    with pytest.raises(NotionAPIError):
        await client.get_user("some-id")

    with pytest.raises(NotionAPIError):
        await client.get_me()

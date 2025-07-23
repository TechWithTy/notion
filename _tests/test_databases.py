"""Tests for Notion Client database operations."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import Response

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.exceptions import (
    NotionBadRequestError,
    NotionNotFoundError,
)
from app.core.integrations.notion.schemas import Database


@pytest.mark.asyncio
async def test_get_database_success(async_notion_client: AsyncNotionClient):
    """Test successful retrieval of a database."""
    database_id = "d9824bdc-8445-4327-be8b-5b47500af6ce"
    mock_response = {
        "object": "database",
        "id": database_id,
        "title": [{"type": "text", "text": {"content": "Test DB"}}],
    }

    with patch.object(
        async_notion_client.client, "get", 
        new_callable=AsyncMock,
        return_value=Response(200, json=mock_response)
    ) as mock_get:
        database = await async_notion_client.get_database(database_id)
        mock_get.assert_called_once_with(f"databases/{database_id}")

    assert isinstance(database, Database)
    assert database.id == database_id
    assert database.title[0].text.content == "Test DB"


@pytest.mark.asyncio
async def test_get_database_not_found(async_notion_client: AsyncNotionClient):
    """Test that NotionNotFoundError is raised for a 404 response."""
    database_id = "d9824bdc-8445-4327-be8b-5b47500af6ce"
    mock_error = {"object": "error", "code": "object_not_found"}

    with patch.object(
        async_notion_client.client, "get",
        new_callable=AsyncMock,
        return_value=Response(404, json=mock_error)
    ) as mock_get:
        with pytest.raises(NotionNotFoundError):
            await async_notion_client.get_database(database_id)
        mock_get.assert_called_once_with(f"databases/{database_id}")


@pytest.mark.asyncio
async def test_query_database_success(async_notion_client: AsyncNotionClient):
    """Test successful query of a database."""
    database_id = "d9824bdc-8445-4327-be8b-5b47500af6ce"
    mock_response = {
        "object": "list",
        "results": [{
            "object": "page",
            "id": "c2f9e9e8-5e5c-4b3c-8a9d-1b3e8a9b3c1e"
        }],
        "next_cursor": None,
        "has_more": False,
    }

    with patch.object(
        async_notion_client.client, "post",
        new_callable=AsyncMock,
        return_value=Response(200, json=mock_response)
    ) as mock_post:
        response = await async_notion_client.query_database(database_id, {})
        mock_post.assert_called_once_with(
            f"databases/{database_id}/query",
            json={}
        )

    assert response.results
    assert len(response.results) == 1
    assert response.results[0].id == "c2f9e9e8-5e5c-4b3c-8a9d-1b3e8a9b3c1e"


@pytest.mark.asyncio
async def test_query_database_bad_request(async_notion_client: AsyncNotionClient):
    """Test that NotionBadRequestError is raised for a 400 response during query."""
    database_id = "d9824bdc-8445-4327-be8b-5b47500af6ce"
    mock_error = {"object": "error", "code": "validation_error"}

    with patch.object(
        async_notion_client.client, "post",
        new_callable=AsyncMock,
        return_value=Response(400, json=mock_error)
    ) as mock_post:
        with pytest.raises(NotionBadRequestError):
            await async_notion_client.query_database(
                database_id, 
                {"filter": {"property": "invalid"}}
            )
        mock_post.assert_called_once_with(
            f"databases/{database_id}/query",
            json={"filter": {"property": "invalid"}}
        )
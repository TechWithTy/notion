"""Tests for Notion Client page operations."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import Response

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.exceptions import NotionNotFoundError
from app.core.integrations.notion.schemas import Page


@pytest.mark.asyncio
async def test_get_page_success(async_notion_client: AsyncNotionClient):
    """Test successful retrieval of a page."""
    page_id = "c2f9e9e8-5e5c-4b3c-8a9d-1b3e8a9b3c1e"
    mock_response = {"object": "page", "id": page_id}
    
    with patch.object(
        async_notion_client.client, "get",
        new_callable=AsyncMock,
        return_value=Response(200, json=mock_response)
    ) as mock_get:
        page = await async_notion_client.get_page(page_id)
        mock_get.assert_called_once_with(f"pages/{page_id}")

    assert isinstance(page, Page)
    assert page.id == page_id


@pytest.mark.asyncio
async def test_get_page_not_found(async_notion_client: AsyncNotionClient):
    """Test NotionNotFoundError is raised on 404."""
    page_id = "nonexistent-page"
    
    with patch.object(
        async_notion_client.client, "get",
        new_callable=AsyncMock,
        return_value=Response(404, json={"object": "error", "message": "Not found"})
    ) as mock_get:
        with pytest.raises(NotionNotFoundError):
            await async_notion_client.get_page(page_id)
        mock_get.assert_called_once_with(f"pages/{page_id}")


@pytest.mark.asyncio
async def test_create_page_success(async_notion_client: AsyncNotionClient):
    """Test successful creation of a page."""
    page_data = {"parent": {"database_id": "test-db"}, "properties": {"title": "Test"}}
    mock_response = {"object": "page", "id": "new-page-id"}
    
    with patch.object(
        async_notion_client.client, "post",
        new_callable=AsyncMock,
        return_value=Response(200, json=mock_response)
    ) as mock_post:
        page = await async_notion_client.create_page(page_data)
        mock_post.assert_called_once_with("pages", json=page_data)

    assert isinstance(page, Page)
    assert page.id == "new-page-id"


@pytest.mark.asyncio
async def test_update_page_success(async_notion_client: AsyncNotionClient):
    """Test successful update of a page."""
    page_id = "c2f9e9e8-5e5c-4b3c-8a9d-1b3e8a9b3c1e"
    update_data = {"properties": {"title": "Updated Title"}}
    mock_response = {"object": "page", "id": page_id}
    
    with patch.object(
        async_notion_client.client, "patch",
        new_callable=AsyncMock,
        return_value=Response(200, json=mock_response)
    ) as mock_patch:
        page = await async_notion_client.update_page(page_id, update_data)
        mock_patch.assert_called_once_with(f"pages/{page_id}", json=update_data)

    assert isinstance(page, Page)
    assert page.id == page_id
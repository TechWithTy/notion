from unittest.mock import AsyncMock, patch

import pytest

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.exceptions import NotionNotFoundError
from app.core.integrations.notion.schemas import CreateCommentPayload, RichText


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_list_comments_success(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests successful retrieval of comments for a block."""
    block_id = "test_block_id"
    mock_response_data = {
        "object": "list",
        "results": [
            {
                "object": "comment",
                "id": "comment_id_1",
                "rich_text": [{"type": "text", "text": {"content": "This is a comment."}}],
            }
        ],
        "next_cursor": None,
        "has_more": False,
    }
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = mock_response_data

    response = await async_notion_client.list_comments(block_id)

    assert len(response.results) == 1
    assert response.results[0].id == "comment_id_1"
    mock_request.assert_called_once_with(
        "GET", f"https://api.notion.com/v1/comments?block_id={block_id}", headers=async_notion_client.headers, json=None, params=None
    )


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_list_comments_not_found(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests that NotionNotFoundError is raised when the block is not found."""
    block_id = "non_existent_block_id"
    mock_request.return_value.status_code = 404
    mock_request.return_value.json.return_value = {
        "object": "error",
        "code": "object_not_found",
        "message": "Could not find block.",
    }

    with pytest.raises(NotionNotFoundError):
        await async_notion_client.list_comments(block_id)


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_create_comment_success(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests successful creation of a comment."""
    payload = CreateCommentPayload(
        parent={"page_id": "page_id_1"},
        rich_text=[RichText(text={"content": "A new comment"})],
    )
    mock_response_data = {
        "object": "comment",
        "id": "new_comment_id",
        "rich_text": [{"type": "text", "text": {"content": "A new comment"}}],
    }
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = mock_response_data

    response = await async_notion_client.create_comment(payload)

    assert response.id == "new_comment_id"
    assert response.rich_text[0].text.content == "A new comment"
    mock_request.assert_called_once()

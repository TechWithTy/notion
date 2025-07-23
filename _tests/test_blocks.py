import pytest
from unittest.mock import AsyncMock, patch

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.exceptions import (
    NotionBadRequestError,
    NotionNotFoundError,
)
from app.core.integrations.notion.schemas import (
    AppendBlockChildrenPayload,
    Block,
    RichText,
)


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_get_block_children_success(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests successful retrieval of block children."""
    block_id = "test_block_id"
    mock_response_data = {
        "object": "list",
        "results": [
            {
                "object": "block",
                "id": "child_block_id",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Hello world", "link": None},
                        }
                    ]
                },
            }
        ],
        "next_cursor": None,
        "has_more": False,
    }
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = mock_response_data

    response = await async_notion_client.get_block_children(block_id)

    assert response.results[0].id == "child_block_id"
    assert isinstance(response.results[0], Block)
    mock_request.assert_called_once()


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_get_block_children_not_found(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests that NotionNotFoundError is raised for a 404 response."""
    block_id = "non_existent_block_id"
    mock_request.return_value.status_code = 404
    mock_request.return_value.json.return_value = {
        "object": "error",
        "code": "object_not_found",
        "message": "Could not find block with ID: ...",
    }

    with pytest.raises(NotionNotFoundError):
        await async_notion_client.get_block_children(block_id)


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_append_block_children_success(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests successfully appending block children."""
    block_id = "parent_block_id"
    payload = AppendBlockChildrenPayload(
        children=[
            Block(
                object="block",
                type="paragraph",
                paragraph={"rich_text": [RichText(text={"content": "New block"})]}
            )
        ]
    )

    mock_response_data = {
        "object": "list",
        "results": [{"object": "block", "id": "new_block_id"}],
    }
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = mock_response_data

    response = await async_notion_client.append_block_children(block_id, payload)

    assert response.results[0].id == "new_block_id"
    mock_request.assert_called_once()


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_append_block_children_bad_request(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests that NotionBadRequestError is raised for a 400 response."""
    block_id = "parent_block_id"
    payload = AppendBlockChildrenPayload(children=[])  # Invalid payload

    mock_request.return_value.status_code = 400
    mock_request.return_value.json.return_value = {
        "object": "error",
        "code": "validation_error",
        "message": "Invalid payload.",
    }

    with pytest.raises(NotionBadRequestError):
        await async_notion_client.append_block_children(block_id, payload)

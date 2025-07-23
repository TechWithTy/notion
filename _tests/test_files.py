from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.schemas import Block, File, FilesProperty


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_retrieve_file_block_success(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests successful retrieval of a block containing a file."""
    block_id = "test_block_id_with_file"
    file_url = "https://example.com/file.pdf"
    mock_response_data = {
        "object": "list",
        "results": [
            {
                "object": "block",
                "id": "file_block_id_1",
                "type": "file",
                "file": {
                    "type": "external",
                    "external": {"url": file_url},
                    "caption": [],
                    "name": "file.pdf",
                },
            }
        ],
        "next_cursor": None,
        "has_more": False,
    }
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = mock_response_data

    response = await async_notion_client.get_block_children(block_id)

    assert len(response.results) == 1
    file_block = response.results[0]
    assert isinstance(file_block, Block)
    assert file_block.type == "file"
    assert isinstance(file_block.file, File)
    assert file_block.file.external.url == file_url
    assert file_block.file.name == "file.pdf"

    mock_request.assert_called_once()


@pytest.mark.asyncio
@patch("httpx.AsyncClient.request", new_callable=AsyncMock)
async def test_get_page_property_file_success(
    mock_request: AsyncMock, async_notion_client: AsyncNotionClient
):
    """Tests successful retrieval of a file property from a page."""
    page_id = "test_page_id"
    property_id = "test_property_id"
    file_url = "https://example.com/document.docx"
    mock_response_data = {
        "object": "property_item",
        "id": property_id,
        "type": "files",
        "files": [
            {
                "name": "document.docx",
                "type": "external",
                "external": {"url": file_url},
            }
        ],
    }
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = mock_response_data

    response = await async_notion_client.get_page_property(page_id, property_id)

    assert response.type == "files"
    assert len(response.files) == 1
    file = response.files[0]
    assert isinstance(file, File)
    assert file.name == "document.docx"
    assert file.external["url"] == file_url

    mock_request.assert_called_once_with(
        "GET",
        f"https://api.notion.com/v1/pages/{page_id}/properties/{property_id}",
        headers=async_notion_client.headers,
        json=None,
        params=None,
    )


def test_get_file_property_route_success(client: TestClient):
    """Tests the file property retrieval route for a successful response."""
    page_id = "test_page_id"
    property_id = "test_property_id"
    file_url = "https://example.com/document.docx"
    mock_response_data = {
        "object": "property_item",
        "id": property_id,
        "type": "files",
        "files": [
            {
                "name": "document.docx",
                "type": "external",
                "external": {"url": file_url},
            }
        ],
    }

    with patch(
        "app.core.integrations.notion.client.AsyncNotionClient.get_page_property",
        new_callable=AsyncMock,
    ) as mock_get_property:
        mock_get_property.return_value = FilesProperty(**mock_response_data)

        response = client.get(
            f"/api/v1/integrations/notion/files/{page_id}/properties/{property_id}"
        )

        assert response.status_code == 200
        json_response = response.json()
        assert json_response["type"] == "files"
        assert len(json_response["files"]) == 1
        assert json_response["files"][0]["name"] == "document.docx"

        mock_get_property.assert_called_once_with(page_id, property_id)

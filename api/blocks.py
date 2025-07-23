from fastapi import APIRouter, Depends, HTTPException

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.dependencies import get_notion_client
from app.core.integrations.notion.exceptions import NotionAPIError
from app.core.integrations.notion.schemas import (
    AppendBlockChildrenPayload,
    AppendBlockChildrenResponse,
    PaginatedBlockResponse,
)

router = APIRouter()


@router.get(
    "/{block_id}/children",
    response_model=PaginatedBlockResponse,
    summary="Get Block Children",
)
async def get_block_children(
    block_id: str,
    page_size: int | None = None,
    client: AsyncNotionClient = Depends(get_notion_client),
):
    """Retrieve a list of child blocks for a given block ID."""
    try:
        return await client.get_block_children(block_id, page_size=page_size)
    except NotionAPIError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{block_id}/children",
    response_model=AppendBlockChildrenResponse,
    summary="Append Block Children",
)
async def append_block_children(
    block_id: str,
    payload: AppendBlockChildrenPayload,
    client: AsyncNotionClient = Depends(get_notion_client),
):
    """Append new child blocks to a specific block."""
    try:
        return await client.append_block_children(block_id, payload)
    except NotionAPIError as e:
        raise HTTPException(status_code=400, detail=str(e))

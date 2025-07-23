from fastapi import APIRouter, Depends, HTTPException

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.dependencies import get_notion_client
from app.core.integrations.notion.exceptions import NotionAPIError
from app.core.integrations.notion.schemas import (
    Comment,
    CreateCommentPayload,
    PaginatedCommentResponse,
)

router = APIRouter()


@router.get(
    "/", response_model=PaginatedCommentResponse, summary="List Comments"
)
async def list_comments(
    block_id: str,
    client: AsyncNotionClient = Depends(get_notion_client),
):
    """Retrieve a list of comments for a given block ID."""
    try:
        return await client.list_comments(block_id)
    except NotionAPIError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=Comment, summary="Create Comment")
async def create_comment(
    payload: CreateCommentPayload,
    client: AsyncNotionClient = Depends(get_notion_client),
):
    """Create a new comment."""
    try:
        return await client.create_comment(payload)
    except NotionAPIError as e:
        raise HTTPException(status_code=400, detail=str(e))

"""API router for Notion page endpoints."""

from fastapi import APIRouter, Depends, status

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.dependencies import get_notion_client
from app.core.integrations.notion.schemas import (
    CreatePagePayload,
    Page,
    UpdatePagePayload,
)

router = APIRouter()


@router.post("/", response_model=Page, status_code=status.HTTP_201_CREATED)
async def create_page(
    payload: CreatePagePayload, client: AsyncNotionClient = Depends(get_notion_client)
) -> Page:
    """Create a new page in Notion."""
    return await client.create_page(payload.dict(exclude_unset=True))


@router.get("/{page_id}", response_model=Page)
async def get_page(
    page_id: str, client: AsyncNotionClient = Depends(get_notion_client)
) -> Page:
    """Retrieve a Notion page by its ID."""
    return await client.get_page(page_id)


@router.patch("/{page_id}", response_model=Page)
async def update_page(
    page_id: str,
    payload: UpdatePagePayload,
    client: AsyncNotionClient = Depends(get_notion_client),
) -> Page:
    """Update a Notion page."""
    return await client.update_page(page_id, payload.dict(exclude_unset=True))

"""API router for Notion database endpoints."""

from fastapi import APIRouter, Depends

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.dependencies import get_notion_client
from app.core.integrations.notion.schemas import (
    Database,
    PaginatedPageResponse,
    QueryDatabasePayload,
)

router = APIRouter()


@router.get("/{database_id}", response_model=Database)
async def get_database(
    database_id: str,
    client: AsyncNotionClient = Depends(get_notion_client),
) -> Database:
    """Retrieve a Notion database by its ID."""
    return await client.get_database(database_id)


@router.post("/{database_id}/query", response_model=PaginatedPageResponse)
async def query_database(
    database_id: str,
    payload: QueryDatabasePayload,
    client: AsyncNotionClient = Depends(get_notion_client),
) -> PaginatedPageResponse:
    """Query a Notion database."""
    return await client.query_database(database_id, payload.dict(exclude_unset=True))

"""FastAPI dependencies for the Notion integration."""

import os
from collections.abc import AsyncGenerator

import httpx
from fastapi import Depends, HTTPException, status

from app.core.integrations.notion.client import AsyncNotionClient

# * Global httpx client for connection pooling
_httpx_client = httpx.AsyncClient()


async def get_notion_token() -> str:
    """Retrieves the Notion API token from environment variables."""
    token = os.getenv("NOTION_API_TOKEN")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="NOTION_API_TOKEN is not set in environment variables.",
        )
    return token


async def get_notion_client(
    token: str = Depends(get_notion_token),
) -> AsyncGenerator[AsyncNotionClient, None]:
    """
    FastAPI dependency to get an instance of the AsyncNotionClient.

    Yields:
        An instance of the AsyncNotionClient.
    """
    yield AsyncNotionClient(token=token, client=_httpx_client)

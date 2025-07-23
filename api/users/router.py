from fastapi import APIRouter, Depends, HTTPException

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.dependencies import get_notion_client
from app.core.integrations.notion.exceptions import NotionAPIError
from app.core.integrations.notion.schemas import PaginatedUserResponse, User

router = APIRouter()


@router.get("/", response_model=PaginatedUserResponse, summary="List All Users")
async def list_users(client: AsyncNotionClient = Depends(get_notion_client)):
    """Retrieve a list of all users in the workspace."""
    try:
        return await client.list_users()
    except NotionAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/me", response_model=User, summary="Get Bot User")
async def get_me(client: AsyncNotionClient = Depends(get_notion_client)):
    """Retrieve the bot user associated with the integration token."""
    try:
        return await client.get_me()
    except NotionAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/{user_id}", response_model=User, summary="Get User by ID")
async def get_user(user_id: str, client: AsyncNotionClient = Depends(get_notion_client)):
    """Retrieve a specific user by their ID."""
    try:
        return await client.get_user(user_id)
    except NotionAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

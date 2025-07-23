from fastapi import APIRouter, Depends, HTTPException

from app.core.integrations.notion.client import AsyncNotionClient
from app.core.integrations.notion.dependencies import get_notion_client
from app.core.integrations.notion.exceptions import NotionAPIError
from app.core.integrations.notion.schemas import FilesProperty

router = APIRouter()


@router.get(
    "/pages/{page_id}/properties/{property_id}",
    response_model=FilesProperty,
    summary="Get Page Property",
)
async def get_page_property(
    page_id: str,
    property_id: str,
    client: AsyncNotionClient = Depends(get_notion_client),
):
    """
    Retrieves a specific property from a Notion page, intended for file properties.
    """
    try:
        return await client.get_page_property(page_id, property_id)
    except NotionAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

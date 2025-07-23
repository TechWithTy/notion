"""Main API router for Notion integration, combining all resource-specific routers."""

from fastapi import APIRouter

from app.api.v1.integrations.notion.databases import databases
from app.api.v1.integrations.notion.pages import pages

router = APIRouter()

# Include resource-specific routers
router.include_router(databases.router, prefix="/databases", tags=["Notion Databases"])
router.include_router(pages.router, prefix="/pages", tags=["Notion Pages"])

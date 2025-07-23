"""Main API router for the Notion integration."""

from fastapi import APIRouter

from app.core.integrations.notion.api import (
    blocks,
    comments,
    databases,
    pages,
    webhooks,
)
from app.core.integrations.notion.api.files import router as files_router
from app.core.integrations.notion.api.users import router as users_router

router = APIRouter()

router.include_router(databases.router, prefix="/databases", tags=["Notion Databases"])
router.include_router(pages.router, prefix="/pages", tags=["Notion Pages"])
router.include_router(blocks.router, prefix="/blocks", tags=["Notion Blocks"])
router.include_router(comments.router, prefix="/comments", tags=["Notion Comments"])
router.include_router(users_router, prefix="/users", tags=["Notion Users"])
router.include_router(
    webhooks.router, prefix="/webhooks", tags=["Notion Webhooks"]
)
router.include_router(files_router, prefix="/files", tags=["Notion Files"])


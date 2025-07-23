from fastapi import APIRouter, Depends, status

from app.core.integrations.notion.webhooks.schemas import WebhookPayload
from app.core.integrations.notion.webhooks.security import verify_notion_signature
from app.core.integrations.notion.webhooks.tasks import process_webhook_event

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(verify_notion_signature)],
    summary="Handle Incoming Notion Webhook",
)
async def handle_notion_webhook(payload: WebhookPayload):
    """
    Receives, validates, and processes incoming webhooks from Notion.

    - **Signature Verification**: Ensures the request is from Notion.
    - **Asynchronous Processing**: Offloads the event to a Celery worker.
    """
    process_webhook_event.delay(payload.model_dump())
    return {"status": "received"}

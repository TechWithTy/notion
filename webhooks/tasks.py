import logging

from app.core.celery_app import celery_app
from app.core.integrations.notion.webhooks.schemas import WebhookPayload

logger = logging.getLogger(__name__)


@celery_app.task(name="notion.process_webhook")
def process_webhook_event(payload: dict):
    """
    Asynchronously processes a Notion webhook event.
    For now, it just logs the event.
    """
    try:
        validated_payload = WebhookPayload.model_validate(payload)
        logger.info(f"Processing Notion webhook event: {validated_payload.event_type}")
        # TODO: Add actual processing logic here based on event_type
        logger.info(f"Payload data: {validated_payload.data}")
    except Exception as e:
        logger.error(f"Error processing Notion webhook payload: {e}", exc_info=True)

from typing import Any, Dict

from pydantic import BaseModel, Field


class WebhookPayload(BaseModel):
    """
    Represents the incoming payload from a Notion webhook.

    *Note*: This is a generic structure, as Notion does not have official webhooks.
    This can be adapted based on the actual payload received.
    """

    event_type: str = Field(..., description="The type of event, e.g., 'page.updated'.")
    data: Dict[str, Any] = Field(
        ..., description="The payload data associated with the event."
    )

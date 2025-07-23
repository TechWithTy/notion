import hashlib
import hmac

from fastapi import Header, HTTPException, Request, status

from app.core.config import settings


async def verify_notion_signature(
    request: Request, x_notion_signature: str = Header(...)
):
    """
    Verifies the HMAC-SHA256 signature of an incoming Notion webhook request.

    The signature is expected in the 'X-Notion-Signature' header.
    The secret is read from the NOTION_WEBHOOK_SECRET environment variable.
    """
    secret = settings.NOTION_WEBHOOK_SECRET
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret is not configured on the server.",
        )

    body = await request.body()
    expected_signature = hmac.new(
        key=secret.encode(), msg=body, digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, x_notion_signature):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature.",
        )

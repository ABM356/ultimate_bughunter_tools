"""Notification service for email/Slack/webhook dispatch."""

from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage
from typing import Any, Dict, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    async def send_slack(self, text: str, webhook_url: Optional[str] = None) -> bool:
        url = webhook_url or settings.SLACK_WEBHOOK_URL
        if not url:
            logger.info("Slack webhook not configured; skipping")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json={"text": text})
        return resp.is_success

    async def send_webhook(self, url: str, payload: Dict[str, Any]) -> bool:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
        return resp.is_success

    def send_email(self, to_addr: str, subject: str, body_html: str) -> bool:
        if not settings.SMTP_HOST:
            logger.info("SMTP not configured; skipping email to %s", to_addr)
            return False
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_USER or "noreply@hopeup.security"
        msg["To"] = to_addr
        msg.set_content("This message requires HTML rendering.")
        msg.add_alternative(body_html, subtype="html")
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            smtp.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(msg)
        return True


_service: NotificationService | None = None


def get_notification_service() -> NotificationService:
    global _service
    if _service is None:
        _service = NotificationService()
    return _service

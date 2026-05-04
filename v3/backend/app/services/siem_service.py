"""SIEM service: log ingestion, correlation, search."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from app.core.elasticsearch_client import get_es

logger = logging.getLogger(__name__)

LOG_INDEX_PREFIX = "hopeup-logs"
ALERT_INDEX_PREFIX = "hopeup-alerts"


def _index_for(tenant_id: Optional[UUID]) -> str:
    return f"{LOG_INDEX_PREFIX}-{tenant_id}" if tenant_id else f"{LOG_INDEX_PREFIX}-global"


class SIEMService:
    async def ingest_log(self, tenant_id: Optional[UUID], event: Dict[str, Any]) -> str:
        es = get_es()
        doc = dict(event)
        doc.setdefault("@timestamp", datetime.now(timezone.utc).isoformat())
        doc["tenant_id"] = str(tenant_id) if tenant_id else None
        resp = await es.index(index=_index_for(tenant_id), document=doc)
        return resp["_id"]

    async def search_logs(
        self,
        tenant_id: Optional[UUID],
        query: Optional[str] = None,
        size: int = 100,
    ) -> List[Dict[str, Any]]:
        es = get_es()
        body: Dict[str, Any] = {"size": size, "sort": [{"@timestamp": "desc"}]}
        if query:
            body["query"] = {
                "query_string": {
                    "query": query,
                    "default_field": "message",
                }
            }
        else:
            body["query"] = {"match_all": {}}
        try:
            resp = await es.search(index=_index_for(tenant_id), body=body)
        except Exception as exc:  # pragma: no cover
            logger.warning("ES search failed: %s", exc)
            return []
        return [hit["_source"] for hit in resp.get("hits", {}).get("hits", [])]

    def correlate(self, events: List[Dict[str, Any]]) -> Optional[UUID]:
        """Naive correlation: return a shared correlation_id if pattern found."""
        if not events:
            return None
        ips = {e.get("ip") for e in events if e.get("ip")}
        if len(ips) == 1 and len(events) >= 3:
            return uuid4()
        return None


_service: SIEMService | None = None


def get_siem_service() -> SIEMService:
    global _service
    if _service is None:
        _service = SIEMService()
    return _service

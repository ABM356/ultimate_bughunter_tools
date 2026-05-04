"""Scanner orchestration service."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scan import Scan

logger = logging.getLogger(__name__)


SCAN_PROFILES: Dict[str, List[str]] = {
    "fast": ["nmap-quick", "httpx", "nuclei-basic"],
    "medium": ["nmap-quick", "httpx", "nuclei-full", "dirsearch", "sqlmap-light"],
    "deep": [
        "nmap-full",
        "httpx",
        "nuclei-full",
        "dirsearch",
        "sqlmap-full",
        "zap-active",
        "wpscan",
        "nikto",
    ],
}


class ScannerService:
    """Coordinates scan execution by handing work off to Celery workers."""

    async def queue_scan(self, db: AsyncSession, scan: Scan) -> str:
        """Push a scan onto the Celery queue. Returns the Celery task id."""
        from app.workers.scan_worker import run_scan

        task = run_scan.delay(str(scan.id))
        scan.status = "queued"
        await db.commit()
        return task.id

    def tools_for_level(self, scan_level: str) -> List[str]:
        return SCAN_PROFILES.get(scan_level, SCAN_PROFILES["fast"])

    async def execute(self, scan_id: UUID, scan_type: str, scan_level: str, target: str) -> Dict[str, Any]:
        """Synchronous orchestration entry point used by the worker."""
        from app.integrations import nmap as nmap_int
        from app.integrations import nuclei as nuclei_int
        from app.integrations import zap as zap_int

        tools = self.tools_for_level(scan_level)
        results: Dict[str, Any] = {"target": target, "tools": tools, "results": {}}

        if "nmap-quick" in tools or "nmap-full" in tools:
            results["results"]["nmap"] = nmap_int.scan(
                target, full="nmap-full" in tools
            )
        if any(t.startswith("nuclei") for t in tools):
            results["results"]["nuclei"] = nuclei_int.scan(target)
        if "zap-active" in tools:
            results["results"]["zap"] = zap_int.active_scan(target)
        return results


_service: ScannerService | None = None


def get_scanner_service() -> ScannerService:
    global _service
    if _service is None:
        _service = ScannerService()
    return _service

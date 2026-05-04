"""python-nmap wrapper."""

from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def scan(target: str, full: bool = False, ports: str = "1-1000") -> Dict[str, Any]:
    """Run an nmap scan against ``target``.

    Falls back to a stubbed result if python-nmap or the nmap binary is
    unavailable so that the skeleton remains importable.
    """
    try:
        import nmap  # type: ignore[import-not-found]
    except ImportError:
        logger.warning("python-nmap not installed; returning stub")
        return {"target": target, "stub": True, "ports": []}

    scanner = nmap.PortScanner()
    args = "-sV -T4" + (" -p-" if full else f" -p{ports}")
    try:
        scanner.scan(hosts=target, arguments=args)
    except Exception as exc:  # pragma: no cover
        logger.warning("nmap scan failed: %s", exc)
        return {"target": target, "error": str(exc), "ports": []}

    out: Dict[str, Any] = {"target": target, "hosts": []}
    for host in scanner.all_hosts():
        host_data: Dict[str, Any] = {"host": host, "state": scanner[host].state(), "ports": []}
        for proto in scanner[host].all_protocols():
            for port, info in scanner[host][proto].items():
                host_data["ports"].append(
                    {
                        "port": port,
                        "proto": proto,
                        "state": info.get("state"),
                        "service": info.get("name"),
                        "version": info.get("version"),
                    }
                )
        out["hosts"].append(host_data)
    return out

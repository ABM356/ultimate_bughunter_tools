"""Nuclei CLI wrapper."""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def scan(
    target: str,
    severity: Optional[List[str]] = None,
    templates: Optional[List[str]] = None,
    timeout: int = 600,
) -> Dict[str, Any]:
    """Invoke nuclei against ``target``. Returns parsed findings."""
    if shutil.which("nuclei") is None:
        logger.warning("nuclei binary not found; returning stub")
        return {"target": target, "stub": True, "findings": []}

    cmd: List[str] = ["nuclei", "-u", target, "-jsonl", "-silent"]
    if severity:
        cmd += ["-severity", ",".join(severity)]
    if templates:
        for t in templates:
            cmd += ["-t", t]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
    except Exception as exc:  # pragma: no cover
        logger.warning("nuclei subprocess failed: %s", exc)
        return {"target": target, "error": str(exc), "findings": []}

    findings: List[Dict[str, Any]] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            findings.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return {
        "target": target,
        "exit_code": result.returncode,
        "findings": findings,
    }

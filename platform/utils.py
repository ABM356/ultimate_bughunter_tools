"""
Shared utilities for the platform.
"""

import os
import json
import subprocess
import shutil
from datetime import datetime, timezone


def check_binary(name):
    return shutil.which(name) is not None


def check_python_module(name):
    try:
        subprocess.run(
            ["python3", "-c", f"import {name}"],
            capture_output=True, timeout=5, check=True,
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False


def run_with_timeout(cmd, timeout=120, cwd=None):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "timeout", "returncode": -1}
    except FileNotFoundError:
        return {"success": False, "stdout": "", "stderr": "not found", "returncode": -2}


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

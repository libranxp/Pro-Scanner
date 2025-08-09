# utils/locks.py

import os
import time
from utils.logger import log

LOCK_DIR = "locks"
LOCK_TIMEOUT = 300  # seconds

def _lock_path(lock_name: str) -> str:
    if not os.path.exists(LOCK_DIR):
        os.makedirs(LOCK_DIR)
    return os.path.join(LOCK_DIR, f"{lock_name}.lock")

def acquire_lock(lock_name: str) -> bool:
    """
    Creates a lock file to prevent concurrent scans.
    Returns True if lock acquired, False if already locked.
    """
    path = _lock_path(lock_name)

    if os.path.exists(path):
        age = time.time() - os.path.getmtime(path)
        if age < LOCK_TIMEOUT:
            log(f"🔒 Lock '{lock_name}' is active ({int(age)}s old).")
            return False
        else:
            log(f"⚠️ Stale lock '{lock_name}' detected. Overriding.")
            release_lock(lock_name)

    with open(path, "w") as f:
        f.write(str(time.time()))
    log(f"✅ Lock '{lock_name}' acquired.")
    return True

def release_lock(lock_name: str):
    """
    Removes the lock file.
    """
    path = _lock_path(lock_name)
    if os.path.exists(path):
        os.remove(path)
        log(f"🔓 Lock '{lock_name}' released.")

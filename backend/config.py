from __future__ import annotations

import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"
DEV_MODE = os.getenv("VITE_DEV_MODE", "true").lower() in {"true", "1", "yes"}
SECRET_KEY = os.getenv("SECRET_KEY", "development-only-secret-32-chars")

# config.py

from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent

DB_PATH = Path(
    os.getenv(
        "FINDEX_DB_PATH",
        PROJECT_ROOT / "data" / "countries.db"
    )
)

try:
    from config_local import DB_PATH
except ImportError:
    pass

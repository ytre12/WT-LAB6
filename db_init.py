import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_FILE = BASE_DIR / "schema.sql"
SEED_FILE = BASE_DIR / "seed.sql"


def ensure_database(db_path):
    """Створює базу зі schema.sql і один раз наповнює її seed.sql."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))

        seeded = connection.execute(
            "SELECT 1 FROM app_meta WHERE key = 'seeded'"
        ).fetchone()
        if seeded is None:
            connection.executescript(SEED_FILE.read_text(encoding="utf-8"))
            connection.execute(
                "INSERT OR REPLACE INTO app_meta (key, value) "
                "VALUES ('seeded', '1')"
            )

        connection.commit()
    finally:
        connection.close()

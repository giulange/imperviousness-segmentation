"""Configurazione centralizzata via variabili d'ambiente / file .env.

Sostituisce i file di credenziali in chiaro (prisma_credentials.json,
sentinelsat_credentials.json) e le stringhe `postgresql://user:pass@...`
hardcoded nei notebook.

Crea un file `.env` (vedi `.env.example`) — NON va committato.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Carica .env dalla root del progetto, se presente
_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    # --- PostGIS (dati OSM) ---
    pg_host: str = os.getenv("PG_HOST", "localhost")
    pg_port: int = int(os.getenv("PG_PORT", "65432"))
    pg_user: str = os.getenv("PG_USER", "giuliano")
    pg_password: str = os.getenv("PG_PASSWORD", "")
    pg_db: str = os.getenv("PG_DB", "osm")

    # --- Copernicus Data Space Ecosystem (sostituto di SciHub/SentinelSat) ---
    cdse_user: str = os.getenv("CDSE_USER", "")
    cdse_password: str = os.getenv("CDSE_PASSWORD", "")

    # --- Percorsi dati (non versionati) ---
    data_dir: Path = Path(os.getenv("DATA_DIR", str(_ROOT / "data")))
    osm_dir: Path = Path(os.getenv("OSM_DIR", str(_ROOT / "osm_data")))
    annotations_dir: Path = Path(os.getenv("ANNOTATIONS_DIR", str(_ROOT / "annotations")))


settings = Settings()


def pg_url(db: str | None = None) -> str:
    """Ritorna l'URL SQLAlchemy per PostGIS."""
    s = settings
    return (
        f"postgresql+psycopg2://{s.pg_user}:{s.pg_password}"
        f"@{s.pg_host}:{s.pg_port}/{db or s.pg_db}"
    )


def pg_engine(db: str | None = None):
    """Crea un SQLAlchemy Engine verso PostGIS (lazy import)."""
    from sqlalchemy import create_engine

    return create_engine(pg_url(db))

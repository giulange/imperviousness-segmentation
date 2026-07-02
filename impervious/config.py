"""Configurazione centralizzata via variabili d'ambiente / file .env.

Sostituisce i file di credenziali in chiaro (prisma_credentials.json,
sentinelsat_credentials.json) e le stringhe di connessione con credenziali
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
    # Chiavi S3 EODATA (per lettura finestrata COG/JP2 dal bucket CDSE)
    cdse_s3_access_key: str = os.getenv("CDSE_S3_ACCESS_KEY", "")
    cdse_s3_secret_key: str = os.getenv("CDSE_S3_SECRET_KEY", "")

    # --- SciHub / SentinelSat (legacy, dismesso: usato solo nei vecchi .ipynb) ---
    scihub_user: str = os.getenv("SCIHUB_USER", "")
    scihub_password: str = os.getenv("SCIHUB_PASSWORD", "")

    # --- Sentinel Hub (sentinelhub-py: usato nei vecchi .ipynb) ---
    sh_instance_id: str = os.getenv("SH_INSTANCE_ID", "")
    sh_client_id: str = os.getenv("SH_CLIENT_ID", "")
    sh_client_secret: str = os.getenv("SH_CLIENT_SECRET", "")

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

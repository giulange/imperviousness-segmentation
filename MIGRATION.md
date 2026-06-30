# Riattivazione & modernizzazione — guida

Obiettivo: rimettere in funzione la pipeline Python su **VM con A100**, con
ambiente riproducibile (**Pixi**), notebook **Marimo**, stack aggiornato (2026).

---

## 1. Architettura scelta

| Pezzo | Prima (2023) | Ora |
|-------|--------------|-----|
| Ambiente | pip manuale, versioni pinnate, GDAL a mano | **Pixi** (`pixi.toml` + lockfile, conda-forge) |
| Notebook | Jupyter `.ipynb` + `%load import.py` | **Marimo** (`.py` reattivi in `notebooks/`) |
| GPU | Docker YOLO separato | feature `gpu` in Pixi (PyTorch CUDA 12 + Ultralytics) |
| Credenziali | JSON in chiaro + URL hardcoded | `.env` + `impervious/config.py` |
| Acquisizione dati | SentinelSat / SciHub (**dismesso**) | **CDSE** (`cdsetool` / `pystac-client`) |
| DB | kartoza/postgis in Docker | invariato |

## 2. Setup sulla VM

```bash
git clone <repo> && cd imperviousness-segmentation
bash scripts/setup_vm.sh          # installa pixi, risolve env gpu, verifica A100
# compila .env (CDSE + PostGIS)
bash scripts/launch_marimo.sh     # avvia Marimo headless
```

Dal laptop: `ssh -N -L 2718:localhost:2718 utente@vm-a100`, poi apri l'URL col token.

## 3. Conversione dei notebook a Marimo

```bash
pixi run convert      # crea notebooks/<nome>.py da ogni .ipynb
```

La conversione è **meccanica**: dopo va sistemato il codice. Punti noti:

- **`%load import.py` / `%load_ext autoreload`** → rimuovere. Usare import
  espliciti per cella; per le utility: `from impervious.config import settings, pg_engine`.
- **celle `pip install ...`** → rimuovere: le dipendenze stanno in `pixi.toml`.
- **shapely 1.8 → 2.0**: `.geom_type`, niente più `.cascaded_union` (usa `shapely.ops.unary_union`); attenzione a `Polygon().exterior.coords.xy` (invariato) e all'iterazione su geometrie.
- **osmnx 1.2 → 2.x**: `ox.geometries_from_place` → **`ox.features_from_place`** (idem `..._from_polygon`). API rinominata.
- **geopandas 0.x → 1.x**: `explode(index_parts=False)` ok; `.to_crs(32633)` ok.
- **sqlalchemy 1.4 → 2.0**: connessioni via `engine.connect()`; `gpd.read_postgis(sql, con)` ok ma passare `text(sql)`.

## 4. Acquisizione dati: da SentinelSat a CDSE

`sentinelsat.ipynb` non funziona più: l'**Open Access Hub (SciHub)** è spento.
Va riscritto verso il **Copernicus Data Space Ecosystem**:
- ricerca STAC: `pystac-client` su `https://catalogue.dataspace.copernicus.eu/stac`
- download: `cdsetool` (autenticazione con `CDSE_USER` / `CDSE_PASSWORD` nel `.env`).

## 5. Training YOLO sull'A100

Stack già nell'env `gpu` (PyTorch CUDA 12 + Ultralytics ≥ 8.3). Non serve più il
Docker YOLO separato (resta un'opzione). Il dataset `imp_class` (classi
`0: building`, `1: street`) e gli `imgsz=480` restano validi; con A100 (40/80 GB)
puoi rialzare `batch` e provare `imgsz=640`/`yolo11-seg`.

## 6. Sicurezza — DA FARE

I file di credenziali erano **tracciati in git**. Sono stati rimossi dal tracking
e aggiunti a `.gitignore`, ma **restano nella history**. Azioni consigliate:
1. **Ruotare** le password (PostGIS, account Copernicus).
2. Ripulire la history (`git filter-repo --invert-paths --path prisma_credentials.json --path sentinelsat_credentials.json`) se il repo è/sarà condiviso.

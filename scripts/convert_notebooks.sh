#!/usr/bin/env bash
# =============================================================================
#  convert_notebooks.sh — converte i vecchi .ipynb in notebook Marimo (.py).
#
#  Marimo usa file .py puri (git-friendly, niente stato nascosto). Questo
#  script crea una copia .py in notebooks/ per ogni .ipynb della root.
#  NB: la conversione è meccanica — il codice 2023 (shapely<2, osmnx<2,
#  sentinelsat, magie %load/%pip) va poi adattato a mano. Vedi MIGRATION.md.
#
#  USO:
#    pixi run convert
# =============================================================================
set -euo pipefail

mkdir -p notebooks

# Notebook del pipeline (in ordine logico). I legacy/scratch
# (Imp_Class, sparse_notes, test-ee-api, visualize_landsat, bash_install_gdal)
# NON vengono convertiti. Per convertirne uno: marimo convert <nb>.ipynb -o notebooks/<nb>.py
CORE=(sentinelsat nuts4 osm annotations DL_modeling main)

for base in "${CORE[@]}"; do
  nb="${base}.ipynb"
  out="notebooks/${base}.py"
  [ -f "$nb" ] || { echo "==> SKIP (assente): $nb"; continue; }
  echo "==> $nb  ->  $out"
  marimo convert "$nb" -o "$out" || echo "    (conversione fallita per $nb — da fare a mano)"
done

echo ""
echo "==> Fatto. Apri con: pixi run marimo"

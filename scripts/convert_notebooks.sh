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

shopt -s nullglob
for nb in *.ipynb; do
  base="$(basename "$nb" .ipynb)"
  out="notebooks/${base}.py"
  echo "==> $nb  ->  $out"
  marimo convert "$nb" -o "$out" || echo "    (conversione fallita per $nb — da fare a mano)"
done

echo ""
echo "==> Fatto. Apri con: pixi run marimo"

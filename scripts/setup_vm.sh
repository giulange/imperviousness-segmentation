#!/usr/bin/env bash
# =============================================================================
#  setup_vm.sh — prepara la VM (A100) per il progetto.
#  Installa Pixi, risolve l'ambiente GPU, verifica la A100.
#
#  USO (sulla VM, dopo `git clone` + `cd imperviousness-segmentation`):
#    bash scripts/setup_vm.sh
# =============================================================================
set -euo pipefail

echo "==> 1/4  Installazione Pixi (se assente)"
if ! command -v pixi >/dev/null 2>&1; then
  curl -fsSL https://pixi.sh/install.sh | bash
  # Pixi finisce in ~/.pixi/bin: assicurati che sia nel PATH
  export PATH="$HOME/.pixi/bin:$PATH"
  echo "    Pixi installato. Aggiungi al tuo shell rc: export PATH=\"\$HOME/.pixi/bin:\$PATH\""
else
  echo "    Pixi già presente: $(pixi --version)"
fi

echo "==> 2/4  Risoluzione ambiente GPU (conda-forge + CUDA 12 + PyTorch + Ultralytics)"
pixi install -e gpu

echo "==> 3/4  Configurazione credenziali"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "    Creato .env da .env.example — COMPILALO (CDSE + PostGIS) prima di usare i notebook."
else
  echo "    .env già presente."
fi

echo "==> 4/4  Verifica A100 vista da PyTorch"
pixi run -e gpu gpu-check

echo ""
echo "==> Fatto. Per avviare Marimo:  bash scripts/launch_marimo.sh"

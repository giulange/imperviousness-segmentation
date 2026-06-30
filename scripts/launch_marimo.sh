#!/usr/bin/env bash
# =============================================================================
#  launch_marimo.sh — avvia Marimo sulla VM, accessibile dal tuo laptop.
#
#  USO (sulla VM):
#    bash scripts/launch_marimo.sh            # ambiente GPU (default sulla VM)
#    ENV=default bash scripts/launch_marimo.sh # ambiente CPU
#
#  Poi, DAL TUO LAPTOP, apri un tunnel SSH:
#    ssh -N -L 2718:localhost:2718 utente@vm-a100
#  e vai su http://localhost:2718 (Marimo stampa l'URL col token).
# =============================================================================
set -euo pipefail

ENV="${ENV:-gpu}"
PORT="${PORT:-2718}"

echo "==> Avvio Marimo (env=$ENV) su 0.0.0.0:$PORT"
echo "    Tunnel dal laptop:  ssh -N -L $PORT:localhost:$PORT <utente>@<vm-a100>"
echo ""
exec pixi run -e "$ENV" marimo edit --headless --host 0.0.0.0 --port "$PORT" notebooks

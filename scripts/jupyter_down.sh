#!/usr/bin/env bash
# =============================================================================
#  jupyter_down.sh — ferma il server JupyterLab detached (e il suo gruppo).
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

PIDFILE=".jupyter.pid"
if [ ! -f "$PIDFILE" ]; then
  echo "Nessun PID file: JupyterLab non risulta attivo."
  exit 0
fi

PID="$(cat "$PIDFILE")"
# setsid rende il PID capo-gruppo: -PID termina l'intero gruppo (pixi + jupyter)
if kill -TERM -- "-${PID}" 2>/dev/null || kill -TERM "${PID}" 2>/dev/null; then
  echo "JupyterLab (PID $PID) terminato."
else
  echo "Processo $PID non attivo (già chiuso)."
fi
rm -f "$PIDFILE"

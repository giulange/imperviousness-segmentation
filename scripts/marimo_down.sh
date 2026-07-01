#!/usr/bin/env bash
# =============================================================================
#  marimo_down.sh — ferma il server Marimo detached (e il suo gruppo di processi).
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

PIDFILE=".marimo.pid"
if [ ! -f "$PIDFILE" ]; then
  echo "Nessun PID file: Marimo non risulta attivo."
  exit 0
fi

PID="$(cat "$PIDFILE")"
# setsid rende il PID capo-gruppo: -PID termina l'intero gruppo (pixi + marimo)
if kill -TERM -- "-${PID}" 2>/dev/null || kill -TERM "${PID}" 2>/dev/null; then
  echo "Marimo (PID $PID) terminato."
else
  echo "Processo $PID non attivo (già chiuso)."
fi
rm -f "$PIDFILE"

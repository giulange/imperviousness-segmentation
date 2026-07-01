#!/usr/bin/env bash
# =============================================================================
#  marimo_status.sh — stato del server Marimo detached.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

PIDFILE=".marimo.pid"
PORT="${PORT:-2718}"
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "ATTIVO — PID $(cat "$PIDFILE"), porta :$PORT"
  echo "--- ultime righe di marimo.log ---"
  tail -n 5 marimo.log 2>/dev/null || true
else
  echo "NON attivo."
fi

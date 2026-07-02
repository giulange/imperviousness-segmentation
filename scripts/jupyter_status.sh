#!/usr/bin/env bash
# =============================================================================
#  jupyter_status.sh — stato del server JupyterLab detached.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

PIDFILE=".jupyter.pid"
PORT="${PORT:-8888}"
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "ATTIVO — PID $(cat "$PIDFILE"), porta :$PORT"
  echo "--- ultime righe di jupyter.log ---"
  tail -n 6 jupyter.log 2>/dev/null || true
else
  echo "NON attivo."
fi

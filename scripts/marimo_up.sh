#!/usr/bin/env bash
# =============================================================================
#  marimo_up.sh — avvia Marimo in modo DETACHED (sopravvive alla caduta SSH).
#
#  Usa setsid+nohup: il server diventa capo-sessione, slegato dal terminale SSH,
#  quindi NON riceve SIGHUP se la connessione cade. PID in .marimo.pid, log in
#  marimo.log.
#
#  USO (sulla VM):
#    bash scripts/marimo_up.sh              # env gpu, porta 2718
#    ENV=default PORT=2720 bash scripts/marimo_up.sh
#  Poi dal laptop:  ssh -N -L 2718:localhost:2718 g.langella@192.168.40.100
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

ENV="${ENV:-gpu}"
PORT="${PORT:-2718}"
PIDFILE=".marimo.pid"
LOG="marimo.log"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "Marimo già attivo (PID $(cat "$PIDFILE")). Usa scripts/marimo_status.sh"
  exit 0
fi

export PATH="$HOME/.pixi/bin:$PATH"
setsid nohup pixi run --frozen -e "$ENV" \
  marimo edit --headless --host 0.0.0.0 --port "$PORT" notebooks \
  > "$LOG" 2>&1 < /dev/null &
echo $! > "$PIDFILE"

sleep 3
echo "Marimo avviato DETACHED (PID $(cat "$PIDFILE"), env=$ENV) su :$PORT — log: $LOG"
echo "Chiudi con: bash scripts/marimo_down.sh"
echo "Tunnel dal laptop:  ssh -N -L $PORT:localhost:$PORT g.langella@192.168.40.100"
echo "--- URL con token (dal log) ---"
grep -m1 "http://127.0.0.1\|access_token\|http://0.0.0.0" "$LOG" || echo "  (ancora in avvio: controlla '$LOG')"

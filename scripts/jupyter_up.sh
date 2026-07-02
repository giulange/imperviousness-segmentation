#!/usr/bin/env bash
# =============================================================================
#  jupyter_up.sh — avvia JupyterLab in modo DETACHED (sopravvive alla caduta SSH).
#
#  Ambiente per l'ESPLORAZIONE LIBERA sui vecchi .ipynb (celle mutabili, esecuzione
#  fuori-ordine) — complementare a Marimo (notebooks/*.py, pipeline "finale").
#  Usa setsid+nohup: il server diventa capo-sessione, slegato dal terminale SSH,
#  quindi NON riceve SIGHUP se la connessione cade. PID in .jupyter.pid, log in
#  jupyter.log.
#
#  USO (sulla VM):
#    bash scripts/jupyter_up.sh              # env gpu, porta 8888
#    ENV=default PORT=8890 bash scripts/jupyter_up.sh
#  Poi dal laptop:  ssh -N -L 8888:localhost:8888 g.langella@192.168.40.100
#  E apri l'URL con token stampato qui sotto (o in jupyter.log).
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

ENV="${ENV:-gpu}"
PORT="${PORT:-8888}"
PIDFILE=".jupyter.pid"
LOG="jupyter.log"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "JupyterLab già attivo (PID $(cat "$PIDFILE")). Usa scripts/jupyter_status.sh"
  exit 0
fi

export PATH="$HOME/.pixi/bin:$PATH"
setsid nohup pixi run --frozen -e "$ENV" \
  jupyter lab --no-browser --ip 0.0.0.0 --port "$PORT" \
  > "$LOG" 2>&1 < /dev/null &
echo $! > "$PIDFILE"

sleep 4
echo "JupyterLab avviato DETACHED (PID $(cat "$PIDFILE"), env=$ENV) su :$PORT — log: $LOG"
echo "Chiudi con: bash scripts/jupyter_down.sh"
echo "Tunnel dal laptop:  ssh -N -L $PORT:localhost:$PORT g.langella@192.168.40.100"
echo "--- URL con token (dal log) ---"
grep -m1 "127.0.0.1:$PORT\|localhost:$PORT\|token=" "$LOG" || echo "  (ancora in avvio: controlla '$LOG')"

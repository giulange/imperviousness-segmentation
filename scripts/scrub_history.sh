#!/usr/bin/env bash
# =============================================================================
#  scrub_history.sh — RIMUOVE i segreti da TUTTA la history git (irreversibile).
#
#  Cosa fa:
#    - elimina dai commit i file di credenziali (prisma/sentinelsat .json)
#    - sostituisce ogni URL di connessione CON credenziali con un placeholder
#      (regex generica: NESSUN segreto scritto in questo script)
#    - crea un backup bundle prima di riscrivere
#
#  ⚠️ Da eseguire SOLO quando siamo pronti al rilascio: riscrive TUTTI gli hash
#     e git-filter-repo rimuove il remote 'origin' per sicurezza. Dopo servirà
#     un force-push coordinato (main + branch).
#
#  Prerequisito già soddisfatto: rotazione delle password (le vecchie non devono
#  più essere valide) — vedi docs/SECURITY.md.
#
#  USO:  bash scripts/scrub_history.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

command -v git-filter-repo >/dev/null 2>&1 || { echo "Serve git-filter-repo"; exit 1; }

echo "==> Backup della history in ../impervious-prescrub-backup.bundle"
git bundle create ../impervious-prescrub-backup.bundle --all

REPL="$(mktemp)"
# Regex generica: neutralizza qualsiasi stringa di connessione con credenziali.
cat > "$REPL" <<'EOF'
regex:postgresql(\+psycopg2)?://[^\s"'@]+@[^\s"'/]+==>postgresql://***REMOVED***
EOF

echo "==> Riscrittura history (rimozione JSON credenziali + redazione URL)"
git filter-repo --force \
  --path prisma_credentials.json --invert-paths \
  --path sentinelsat_credentials.json --invert-paths \
  --replace-text "$REPL"

rm -f "$REPL"

cat <<'NEXT'

==> Fatto. Passi successivi (manuali, coordinati):
    git remote add origin git@github.com:giulange/imperviousness-segmentation.git
    git push --force --all
    git push --force --tags
    # Ripristino in caso di problemi:
    #   git clone ../impervious-prescrub-backup.bundle recovered
NEXT

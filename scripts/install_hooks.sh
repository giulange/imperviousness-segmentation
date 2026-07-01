#!/usr/bin/env bash
# =============================================================================
#  install_hooks.sh — pre-commit hook che blocca i segreti (detect-secrets).
#  detect-secrets è nell'ambiente Pixi (pypi, cross-platform).
#  USO:  bash scripts/install_hooks.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.pixi/bin:$PATH"

# Baseline (fingerprint dei "falsi positivi" noti); nessun segreto in chiaro.
if [ ! -f .secrets.baseline ]; then
  echo "Genero .secrets.baseline ..."
  pixi run -e default detect-secrets scan > .secrets.baseline
fi

mkdir -p .git/hooks
cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
# Blocca il commit se detect-secrets trova NUOVI segreti negli staged.
export PATH="$HOME/.pixi/bin:$PATH"
command -v pixi >/dev/null 2>&1 || exit 0
files=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "$files" ] && exit 0
if ! echo "$files" | xargs pixi run -e default detect-secrets-hook --baseline .secrets.baseline; then
  echo "❌ detect-secrets: possibili segreti negli staged. Commit bloccato."
  echo "   (falso positivo? aggiorna la baseline: pixi run -e default detect-secrets scan --baseline .secrets.baseline)"
  exit 1
fi
HOOK
chmod +x .git/hooks/pre-commit
echo "pre-commit hook installato (detect-secrets). Baseline: .secrets.baseline"

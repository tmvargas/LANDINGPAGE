#!/usr/bin/env bash
set -euo pipefail

readonly APP_DIR="/opt/plansmart/sistemas/landingpage"
readonly EXPECTED_COMMIT="${1:-}"

if [[ -z "$EXPECTED_COMMIT" ]]; then
  echo "Uso: $0 <commit-main-autorizado>" >&2
  exit 2
fi

cd "$APP_DIR"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Deploy interrompido: árvore Git local não está limpa." >&2
  exit 3
fi

git fetch --prune origin main
git switch main
git merge --ff-only origin/main

readonly LOCAL_COMMIT="$(git rev-parse HEAD)"
readonly REMOTE_COMMIT="$(git rev-parse origin/main)"

if [[ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" || "$LOCAL_COMMIT" != "$EXPECTED_COMMIT" ]]; then
  echo "Deploy interrompido: HEAD, origin/main e commit autorizado divergem." >&2
  exit 4
fi

nginx -t
systemctl reload nginx

echo "Deploy concluído no commit $LOCAL_COMMIT"

#!/usr/bin/env bash
set -euo pipefail

# Generates compiled SQL artifacts into a dedicated folder for manual sanity checks.
# Usage:
#   scripts/dbt_sanity_sql.sh
#   SANITY_DIR=tmp/sanity_sql scripts/dbt_sanity_sql.sh --select marts.*

SANITY_DIR="${SANITY_DIR:-sanity_sql}"
TARGET_PATH="${SANITY_DIR}/target"
COMPILED_PATH="${TARGET_PATH}/compiled/fresh_segments/models"

mkdir -p "${SANITY_DIR}"

echo "[sanity] compiling dbt project into: ${TARGET_PATH}"
dbt compile \
  --target-path "${TARGET_PATH}" \
  --no-partial-parse \
  "$@"

echo "[sanity] compiled SQL files are available under: ${COMPILED_PATH}"

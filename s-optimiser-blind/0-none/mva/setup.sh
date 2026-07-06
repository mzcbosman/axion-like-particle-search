#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_DIR="${SCRIPT_DIR}"
REPO_ROOT=""
while [ "${CURRENT_DIR}" != "/" ]; do
  if [ -d "${CURRENT_DIR}/.git" ]; then
    REPO_ROOT="${CURRENT_DIR}"
    break
  fi
  CURRENT_DIR="$(dirname "${CURRENT_DIR}")"
done

if [ -z "${REPO_ROOT}" ]; then
  echo "Could not locate repository root." >&2
  exit 1
fi

source "${REPO_ROOT}/common/setup.sh"

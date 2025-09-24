#!/usr/bin/env bash
set -euo pipefail

cd "${COMFYUI_HOME:-/opt/ComfyUI}"

if [ -n "${CLI_ARGS:-}" ]; then
  set -- python main.py ${CLI_ARGS}
else
  set -- python main.py
fi

exec "$@"

#!/usr/bin/env bash
set -euo pipefail

missing=0
for command in python3 node npm curl; do
  if command -v "$command" >/dev/null 2>&1; then
    printf '%s: OK\n' "$command"
  else
    printf '%s: MISSING\n' "$command"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi
printf 'Environment OK\n'

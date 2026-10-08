#!/bin/sh
# Download the latest GitHub VS Code theme from Open VSX and regenerate themes/.
set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

URL=$(curl -fsSL https://open-vsx.org/api/GitHub/github-vscode-theme/latest |
  python3 -I -c 'import json, sys; print(json.load(sys.stdin)["files"]["download"])')

curl -fsSL -o "$WORK/theme.vsix" "$URL"
unzip -q "$WORK/theme.vsix" -d "$WORK/vsix"

python3 -I "$ROOT/scripts/generate.py" "$WORK/vsix/extension" "$ROOT/themes"

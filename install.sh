#!/bin/sh
# Install every GitHub theme into Otty.
#
#   curl -fsSL https://raw.githubusercontent.com/kingsleydon/otty-github-theme/main/install.sh | sh
#
# Re-running updates themes you already have.
set -eu

BASE="https://raw.githubusercontent.com/kingsleydon/otty-github-theme/main/themes"
THEMES="
github-dark-default
github-dark-dimmed
github-dark-high-contrast
github-dark-colorblind
github-dark
github-light-default
github-light-high-contrast
github-light-colorblind
github-light
"

if ! command -v otty >/dev/null 2>&1; then
  echo "otty CLI not found. Install Otty from https://otty.sh first." >&2
  exit 1
fi

for t in $THEMES; do
  otty theme import "$BASE/$t.ottytheme" --overwrite --quiet
  echo "Installed $t"
done

echo "Done. Pick a theme in Settings → Appearance → Themes."

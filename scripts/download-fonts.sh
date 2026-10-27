#!/usr/bin/env bash
# Download Poppins (SIL OFL 1.1, by Indian Type Foundry) into ./fonts/.
# Source: google/fonts repository on GitHub. Requires curl.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p fonts
BASE="https://raw.githubusercontent.com/google/fonts/main/ofl/poppins"
curl -fL "$BASE/Poppins-Regular.ttf" -o fonts/Poppins-Regular.ttf
curl -fL "$BASE/Poppins-Bold.ttf" -o fonts/Poppins-Bold.ttf
echo "Fonts downloaded to fonts/ (Poppins, SIL OFL 1.1)."

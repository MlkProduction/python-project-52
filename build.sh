#!/usr/bin/env bash
set -euo pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
if [[ -f "$HOME/.local/bin/env" ]]; then
  # shellcheck source=/dev/null
  source "$HOME/.local/bin/env"
else
  export PATH="$HOME/.local/bin:$PATH"
fi

make install
make collectstatic
make migrate


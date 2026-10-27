#!/usr/bin/env bash
# Same as publish.ps1, for macOS/Linux/Git Bash.
set -euo pipefail
name=world-system-monitor
owner=$(gh api user -q .login)
gh repo create "$name" --public --source . --remote origin --push \
  --description "Geopolitical & macro dashboard that scores 12 theories of world order against live data, publishes falsifiable forecasts, and Brier-scores itself." \
  --homepage "https://$owner.github.io/$name/"
for t in geopolitics dashboard forecasting data-visualization international-relations economics brier-score github-pages javascript portfolio; do
  gh repo edit "$owner/$name" --add-topic "$t"
done
gh api -X POST "repos/$owner/$name/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null
echo "Done: https://github.com/$owner/$name  ·  https://$owner.github.io/$name/"

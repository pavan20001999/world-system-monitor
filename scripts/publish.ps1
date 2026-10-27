# Publishes this folder as a public GitHub repo with GitHub Pages, topics and a description.
# Requires: git and GitHub CLI (https://cli.github.com), signed in with `gh auth login`.
# Run from the repo folder:  powershell -ExecutionPolicy Bypass -File scripts\publish.ps1
$ErrorActionPreference = "Stop"
$name = "world-system-monitor"
$owner = (gh api user -q .login)
$desc = "Geopolitical & macro dashboard that scores 12 theories of world order against live data, publishes falsifiable forecasts, and Brier-scores itself."

gh repo create $name --public --source . --remote origin --push --description $desc --homepage "https://$owner.github.io/$name/"
gh repo edit "$owner/$name" --add-topic geopolitics --add-topic dashboard --add-topic forecasting --add-topic data-visualization --add-topic international-relations --add-topic economics --add-topic brier-score --add-topic github-pages --add-topic javascript --add-topic portfolio
gh api -X POST "repos/$owner/$name/pages" -f "source[branch]=main" -f "source[path]=/" | Out-Null
Write-Host "Done. Repo: https://github.com/$owner/$name  Live site (ready in ~1 min): https://$owner.github.io/$name/"

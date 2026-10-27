# Methodology

The dashboard is a deterministic model. All judgment is confined to two disclosed places: **model design** (which indicators represent each theory, fixed in advance) and **outcome coding** (mapping each cited reading onto a five-level rubric). Everything after that is arithmetic running in the browser.

## 1. Theory Scoreboard

Each theory is broken into one **core claim** (weight 2) and two to four **auxiliary predictions** (weight 1). Each indicator is coded against the current reading:

| Outcome `o` | Meaning |
|---|---|
| 1.00 | hit |
| 0.75 | mostly |
| 0.50 | partial or still open |
| 0.25 | weak |
| 0.00 | miss |

```
S = 100 · Σ(wᵢ·oᵢ) / Σwᵢ
```

Verdict thresholds: **≥75 Supported · 55–74 Watch · 40–54 Mixed · <40 Weak**.

Each card also carries a **since-1945 score**: five to seven major post-war events coded on the same rubric with equal weights. The gap between the two scores shows where the present and history disagree.

## 2. Forecast Board

```
p = clamp(base + Σ adjustments, 0.02, 0.98)
```

- **Base rate**: an outside-view reference class (how often events of this kind resolve this way).
- **Adjustments**: ±0.03 to ±0.15, each tied to a specific reading and itemized on the card. Later editions append adjustments labelled `UPDATE No. N` instead of rewriting earlier ones.
- **Market check**: where a prediction market or futures-implied probability exists, it is shown, and a blend is computed with the Good Judgment aggregation `extremize(mean(model, market), a = 1.73)`.
- **Resolution**: each forecast has an ID, a deadline and a falsifier fixed at publication. Resolved forecasts move to the calibration ledger and are scored with the Brier score `(p − outcome)²`. Conditional forecasts whose condition fails are marked void and not scored.

No machine-learning model is used. With one world and roughly 20 inputs per edition, a fitted model would add false precision.

## 3. Country Instability Index (CII v8)

Adopted from the open-source World Monitor project:

```
event = 0.25·Unrest + 0.30·Conflict + 0.20·Security + 0.25·Information
CII   = 0.40·baseline + 0.60·event + boosts
```

Floors apply (UCDP active war → minimum 70) and results are clamped to 0–100. Boost caps: sanctions ≤14, displacement ≤20, alert blend ≤25. Bands: Critical 81–100 · High 66–80 · Elevated 51–65 · Normal 31–50 · Low 0–30. Countries without a published baseline (e.g. Sudan) are tracked on the Conflict Monitor but not CII-scored.

## 4. Comprehensive National Power (CNP)

Huang Shuofeng's seven components (PLA Academy of Military Science, 1985). Weights: economy 0.28 (Huang's published weight), diplomacy 0.07 (CASS's published weight), the remaining five interpolated to follow the CASS ordering and sum to 1. The China/US ratio feeds Graham Allison's "structural stress" indicator.

## 5. WSM Stress Index

A composite in the style of the GPR/EPU indices: six components (chokepoint status 0.25; conflict census, freight war premium, sanctions intensity, trade-war escalation and tech decoupling at 0.15 each), each normalized 0–100 against its post-1990 typical range. It is a gauge, not a forecast.

## 6. Market Radar

Seven binary signals with a fixed bullish rule each. The verdict is risk-on when at least 57% of signals are bullish (structure adopted from World Monitor). Informational only.

## 7. Refresh process

1. Collect current readings from public sources (web search and page fetch); sites that block automated access are covered through secondary reporting and labelled.
2. Update readings and re-code outcomes against the unchanged rubric.
3. Resolve any forecasts past their deadline; add new ones with fresh IDs.
4. Scores, ranks, charts and the ledger recompute on page load.
5. Increment the edition number and record changes and corrections in `CHANGELOG.md`.

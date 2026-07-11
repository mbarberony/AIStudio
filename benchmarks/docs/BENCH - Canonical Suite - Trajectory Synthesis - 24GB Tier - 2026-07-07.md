# AIStudio — Canonical Benchmark Suite
## Synthesis & Trajectory · 24 GB Tier (llama3.1:8b × gemma3:12b) · 2026-07-07

*Type: NOTES | Domain: AIS | Status: internal provenance — **hardware-tier edition**, sibling to the [27b Trajectory Synthesis](BENCH%20-%20Canonical%20Suite%20-%20Trajectory%20Synthesis%20-%202026-07-03.md). Where the 27b edition reads the arc across three time points on Beast, this reads the arc across **model tiers on a memory-constrained (24 GB) machine** — Suzanne's Mac, the box that historically returned 0/0/0 citations. IN PROGRESS: sec_10k complete; ESEF C/D pending tonight's runs.*

**Machine:** Suzanne / MacBook-Pro-2 · 24 GB unified memory · HEAD `093fabc`
**Tiers:** `llama3.1:8b` (small, ~fast) × `gemma3:12b` (mid, ~50% slower) · Top-K=10 · T=0.3 · α=0.5 · **system_prompt_tier=small (both <20B)**
**Reproduce:** `ais_bench --corpus sec_10k --model <M> [--questions frontier]` · ESEF: `--corpus esef_banks [--scope lang_en --questions lang_en]`
**Note:** 27b does **not** fit 24 GB (loads to VRAM then wedges — blocked HTTP, tiny RSS). The tier ceiling here is 12b.

---

## The suite at a glance — across model tiers (24 GB)

**sec_10k (complete):**
| Run | Set · axis | 8b | 12b | Tier finding |
|---|---|---|---|---|
| **A** | dependable surface | 9🟢/1🟡 · 44s | 8🟢/1🟡/1🔴 · 67s | both solid on calibrated surface; single-cell numeric exact ($177.6B) at both |
| **B** | synthesis/table frontier | 6🟢/2🟡/2🔴 · 29s | **9🟢/1🟡 · 50s** | **the tier split** — see below |

*(A/B shown at the +BlackRock shortcut-add state; Q9 is a known setup artifact pending the faithful re-add + re-run. Every other question is tier-clean.)*

**ESEF C/D (pending — tonight):**
| Run | Set · axis | 8b | 12b |
|---|---|---|---|
| **C** | esef · blended (language) | _pending_ | _pending_ |
| **D** | esef · English-matched (control) | _pending_ | _pending_ |

---

## The frontier this tier exposes — table-collapse is model-tier-dependent

The 27b edition's headline was *mechanical pass ≠ correct* (B-Q5's table, fluent and cited but wrong in the cells). On the 24 GB tier, the same B-Q5 table exposes something sharper: **the failure MODE itself changes with the model.**

- **8b FABRICATES — the dangerous mode.** B·8b·Q5 manufactures numbers from the wrong cells: Bank of America "total revenue" built by summing two *equity* rows ($272,400 + $263,249 = $535,649M); Citigroup revenue cell-duplicated across years; JPMorgan CET1 pulled on the wrong basis (Basel Advanced vs Standardized). Fluent, citation-rich, invented.
- **12b stays DISCIPLINED — the safe mode.** B·12b·Q5 opens "based solely on the provided sources," gives a correct causal read (Citi 2025 decrease → buybacks + RWA increase + dividends), and where a value is absent (BofA revenue) **declares it absent** rather than inventing one. Same corpus, same chunking limit — no fabrication.

The control holds at both tiers: **single-cell numeric (Q10, FY2024 net revenue $177.6B) is exact on 8b and 12b.** The split is entirely in the *multi-cell table* — the shape that requires binding a value to its row/year/basis coordinates.

**Structural cause:** chunking severs the value from its coordinate header. Both tiers hit that limit; they differ in what they do when they hit it — 8b patches with plausible arithmetic on the wrong cells, 12b hedges and omits.

---

## Secondary tier findings (sec_10k)

- **Citation-drop at 8b on the frontier.** B·8b Q6/Q8 returned correct-looking prose with **0 citations** (cd=0.0) at short latency — the citation mechanism, uniform everywhere else (`tier=small` engaged on all questions), wobbled on two frontier questions. 12b did not exhibit this. Needs a `/debug/retrieve` trace to separate retrieval starvation from generation-ignoring-context.
- **Latency is the 12b tax.** A·12b averaged 66.7s (peak 101s) vs 8b's 44.4s — ~50% slower on the 24 GB box, the cost of the disciplined tier.
- **BlackRock Q9 is a setup artifact, not a tier finding.** The +BlackRock runs used an incomplete corporate-action add (`--tkr BLK` → 2 of 5 filings, thin aliases); Q9's entity-filter miss/backfill reflects that, not model quality. Superseded by the faithful re-add + re-run (pending).

---

## The tier recommendation (the point of the exercise)

On a 24 GB machine:
- **Qualitative work** (disclosure, cyber, climate, digital strategy, single-cell numeric): **8b is sufficient** — correct, cited, ~50% faster.
- **Quantitative / multi-cell table work:** **12b is the safer tier** — it trades latency for *no fabrication*. Because the 8b fallback is the dangerous mode (invented numbers that look authoritative), **table-aware chunking** (bind value → row → year → basis at ingest) is the **top capability lever** — and it is *higher* priority for this tier than for Beast, since Beast can simply run the model that degrades safely.

---

## The constant (carried from the 27b edition)

The graceful-failure property holds here too, tier-dependently: **12b never invents a number** — it says less, hedges, or declines. 8b does invent on the table frontier — the one place the constant breaks at the small tier, and the reason the tier recommendation matters.

---

## How to read this against the 27b edition
The [27b Trajectory Synthesis](BENCH%20-%20Canonical%20Suite%20-%20Trajectory%20Synthesis%20-%202026-07-03.md) establishes the *durable calibrated baseline* on Beast (A 9/10, B ~6.5–7, C ~8–9/12, D ~7–8/8, zero fabrication). This edition asks: **what survives on 24 GB, and at which tier?** The answer so far — the calibrated surface survives at both tiers; the table frontier survives *safely* only at 12b; the language frontier (C/D) is tonight's measurement.

---

## Pending (completes this doc)
- **ESEF C/D × 8b/12b** — the language axis on the 24 GB tier (watch BNP/Erste/UniCredit for the non-EN drag; D is the EN control).
- **Faithful-BlackRock sec_10k re-run** — clean Q9 across the +BLK 2×2, superseding the shortcut-add rows above.
- Fold both into the tables + the tier recommendation once the data lands.

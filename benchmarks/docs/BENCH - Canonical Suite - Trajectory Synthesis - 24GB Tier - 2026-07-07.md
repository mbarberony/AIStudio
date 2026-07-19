# AIStudio — Canonical Benchmark Suite
## Synthesis & Trajectory · 24 GB Tier (llama3.1:8b × gemma3:12b) · 2026-07-07

*Type: NOTES | Domain: AIS | Status: internal provenance — **hardware-tier edition**, sibling to the [27b Trajectory Synthesis](BENCH%20-%20Canonical%20Suite%20-%20Trajectory%20Synthesis%20-%202026-07-03.md). Where the 27b edition reads the arc across three time points on a 128 GB machine, this reads the arc across **model tiers on a memory-constrained (24 GB) machine** — a 24 GB MacBook Pro — the machine that had historically returned zero citations. IN PROGRESS: sec_10k complete; ESEF C/D pending; **sweep-survival rows under re-measurement 2026-07-19 (AIStudio_1052)** — now **blocked on the bench sweep-starvation fix** (see *The memory envelope*, added 2026-07-17). Fit guard live-verified on this box 2026-07-17.*

> **Where this sits in the arc.** This is a waypoint, not a conclusion. It records what the suite established on this hardware at this date; later runs extend it and none of the findings below have been restated. Read it as "what we knew on 2026-07-07, plus what the memory work added on 2026-07-17" — the memory-envelope section is a later addition and is marked as such.

**Machine:** MacBook Pro · 24 GB unified memory · HEAD `093fabc`
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

> **Read this together with *The memory envelope* below**, added after later testing: the recommendation here is sound for **single queries**, but a model near this machine's ceiling may not sustain a long multi-question run. The original recommendation is unchanged; the caveat is additive.

On a 24 GB machine:
- **Qualitative work** (disclosure, cyber, climate, digital strategy, single-cell numeric): **8b is sufficient** — correct, cited, ~50% faster.
- **Quantitative / multi-cell table work:** **12b is the safer tier** — it trades latency for *no fabrication*. Because the 8b fallback is the dangerous mode (invented numbers that look authoritative), **table-aware chunking** (bind value → row → year → basis at ingest) is the **top capability lever** — and it is *higher* priority for this tier than for a large-memory machine, since such a machine can simply run the model that degrades safely.

---

## The memory envelope (added 2026-07-17) — *what fits* vs *what sustains*

The tier recommendation above answers **which model to trust**. Live verification on this box on 2026-07-17 added a second, orthogonal axis the recommendation must carry: **which model the machine can sustain for a given workload.** They are not the same question.

**The fit guard is verified live on this machine.** The memory-fit guard's block path had previously only been exercised by simulation on a large-memory machine. On this box every surface was confirmed: the `ais_start` Models footer (honest per-model verdicts that track live memory — `4b✅ 8b✅ · 12b⛔ 12b-qat⛔ 27b⛔` "2 of 5" at ~10 GB free; "4 of 5" at ~15 GB after `ollama stop`), the bench interactive picker (a real 3-model numbered list), all three `--fit-policy` modes (`force` wedged 27b at 🔴 0.02 s — the guard's value demonstrated), and the `/ask` per-request preflight. **This is the machine whose available-memory reading had been under-reporting by roughly 2.5×; the corrected measurement now reflects real free memory here.**

**Sweep survival is inversely proportional to model size.** A benchmark sweep accumulates per-question working memory (KV cache / retrieval context at `num_ctx=16384`) that is **not released between questions**. Instrumented trace (3 s sampling): idle 68% → 52% at model load → gradual drift → **23% by Q9–Q10**, at which point the `/ask` guard begins BLOCKing the remaining questions. Confirmed **endogenous** (process audit mid-run: sole consumer `llama-server` at 5.4 GB; free returns to ~69% post-run).

| Tier | Fits idle (24 GB)? | Sustains a 10-Q sweep? |
|---|---|---|
| `gemma3:4b` | ✅ | **yes — full 4-run matrix, zero blocks** (measured 2026-07-19) |
| `llama3.1:8b` | ✅ | ⚠️ *under re-measurement* — recorded as ~7–9 questions then guard-blocks |
| `gemma3:12b` | ✅ | ⚠️ *under re-measurement* — recorded as starving after ~1 question |
| `gemma3:12b-it-qat` | ✅ (at ≥~15 GB free) | untested; C/D runs were skipped by the pre-fix guard |
| `gemma3:27b` | ❌ never | — |

> **⚠️ The two ⚠️ rows are in doubt and are being re-measured (added 2026-07-19).** They were taken **before AIStudio_1052 was known**: the fit guard was running a single load-time test — *does this model's footprint fit in free memory?* — to answer two different questions, and applying it to a query against an **already-resident** model is wrong, because free memory is low *precisely because that model occupies it*. Observed live: a question answered at 25% free and the next refused at 23%. So "starvation" in those rows may be **partly, or entirely, the guard refusing work the machine could have done**, rather than real exhaustion.
>
> **Do not correct these figures by reasoning — re-measure them.** The evidence is the completed `gemma3:12b-it-qat` matrix on this box under the corrected harness (`bench` ≥2.26.3 + `api` ≥1.20.3), which has not yet been run. Until then: the **fits** column stands, the single-query tier recommendation stands, and only the sweep-survival column is in question. If a 12b-class model does sustain a sweep once the guard asks the right question, the tier ceiling moves up and the user-facing guidance moves with it.

**Consequence for the tier recommendation.** "12b for quantitative work" holds **for single queries** — it remains the non-fabricating tier and that finding is unchanged. Whether 12b can sustain a multi-question session on 24 GB is **open pending the re-measurement above**; the earlier "cannot" was measured under the defective guard. What is not in doubt is the shape of the axis: user guidance must split on workload, single-query versus batch, and a model near the ceiling is the one to watch on a long unattended run. Launching from a clean baseline (`ollama stop` first) buys questions; it does not remove the ceiling.

**⚠ Provisional status of constrained-tier sweep scores.** Because the harness does not reset per-question memory, a multi-question sweep on this machine partly measures **the harness's own memory hygiene**, not the model. Two harness defects follow, both filed:
1. **Sweep self-starvation** — per-question KV/context not released (PRIORITY; gates further constrained-tier benchmarking).
2. **The grader cannot distinguish a block from a miss.** Latency is the discriminator: **0.02 s + 0 citations = guard BLOCK** (memory; the advisory is returned as the answer, `ok:true`) versus **40–60 s + 0 citations = a genuine content miss.** Both currently score 🔴, making the constrained-box pass rate uninterpretable. A clean-baseline Run A scored 7/10 — but two of the three reds were blocks, leaving **one real miss** (Q3, 2-firm × 2-year cyber comparison, 48.56 s, substantive prose, zero `[N]` tags while siblings cited fine). Its faithfulness is **undetermined**: the report stores no retrieved chunks, so BENCH_HARNESS §179's "verify the cited chunk" is un-executable from the artifact.

**This does not invalidate the 2026-07-07 rows above.** Those runs completed without starvation (recorded `9🟢·1🟡·0🔴`, "without starvation"); reading them confirms it. The starvation is a newly-characterized mode under tight-baseline conditions.

---

## The constant (carried from the 27b edition)

The graceful-failure property holds here too, tier-dependently: **12b never invents a number** — it says less, hedges, or declines. 8b does invent on the table frontier — the one place the constant breaks at the small tier, and the reason the tier recommendation matters.

---

## How to read this against the 27b edition
The [27b Trajectory Synthesis](BENCH%20-%20Canonical%20Suite%20-%20Trajectory%20Synthesis%20-%202026-07-03.md) establishes the *durable calibrated baseline* on a 128 GB machine (A 9/10, B ~6.5–7, C ~8–9/12, D ~7–8/8, zero fabrication). This edition asks: **what survives on 24 GB, and at which tier?** The answer so far — the calibrated surface survives at both tiers; the table frontier survives *safely* only at 12b; the language frontier (C/D) was the next measurement planned.

---

## Pending (completes this doc)
- **ESEF C/D × 8b/12b** — the language axis on the 24 GB tier (watch BNP/Erste/UniCredit for the non-EN drag; D is the EN control).
- **Faithful-BlackRock sec_10k re-run** — clean Q9 across the +BLK 2×2, superseding the shortcut-add rows above.
- Fold both into the tables + the tier recommendation once the data lands.
- **⚠ BLOCKED ON HARNESS (added 2026-07-17):** run C/D only **after** the sweep-self-starvation fix + the block-vs-miss grader land — otherwise multi-question sweep scores on this box are starvation-confounded (see *The memory envelope*). Target shape is the **8-run matrix: (A,B,C,D) × (8b, 12b)**.
- **Resolve Q3-class faithfulness** — needs harness chunk-capture (`--save-context`) to test untagged-grounding vs fabrication.

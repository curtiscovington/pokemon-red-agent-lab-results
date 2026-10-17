# Model badge decline: trace investigation, 2026-10-17

## Verified outcomes and scope

Published v2.21:4/8 model wins (3/4 recovery,1/4 baseline); v2.22 model0/5; stopped v2.24 model0/6; completed v2.25 model0/15. Earlier wins and later completed-batch failures were independently verified from saved emulator states. Stopped v2.24 is development evidence only. No outcome exclusions or historical pooling.

## What the code comparison establishes

Existing Python files changed from v2.21 to v2.22:lab.py and presentation.py only. From v2.21 to v2.25:those plus interaction_guard.py. Added baseline modules do not participate in reactive action selection. Navigation, action macros, skill execution, objective guidance, memory, request builder, emulator and model guard source files are byte-identical. Model digest, safe-loader hash, ROM/save hashes and recorded PyBoy/pokemon-agent/httpx versions match. Core inference options match except seed IDs. We have not independently established identical historical backend binaries, machine load, thermal state or all installed dependency contents.

Lab diff adds baseline branches, decision tags/audits, schedule and freeze checks; model warmup/request/parse/execute logic is retained. Instrumentation could still affect timing, so code similarity alone does not prove behavioral equivalence. Actual request-builder functions from archived and current packages produce identical outputs on19346 same-input archived main-observation contexts across34 model runs. This checks the builder given equal inputs, not that independently running controllers generate identical histories or model outputs.

The interaction-guard correction cannot be the sole cause:the0/5 pilot and0/6 stopped-batch model results preceded it. Do not revert a reproduced fix on this evidence alone.

## Where the later runs lose opportunities

Compare recovery-enabled runs, avoiding mixing the published no-recovery arm into the direct comparison:

- Published4/4 reached the gym and all4 encountered Brock's Geodude;3 won.
- Latest9/15 reached the gym, only6/15 encountered Brock's Geodude;0 won.
- Median gym arrival with non-arrivals capped at60min:39:51 published recovery vs54:07 latest. This is a censored descriptive statistic, not mean arrival among successes.
- Median of per-run median model response latency:1.852s vs1.875s. No large response-latency slowdown appears in this measure. Total throughput can also depend on walking, battles, stale actions and repeated menus.
- Later runs that reach Brock generally use Ember; this is not uniformly the old scripted Scratch-selection defect. Some gym arrivals never reach the leader; one latest run repeatedly selected Scratch and visited the guide10times.
- First observed Geodude entries in both groups typically involve level12–13 Charmander. Later Onix entries sometimes begin with little HP (e.g.4HP in latest run41), but older winners also faced Onix with varied health. No single level/HP difference explains all outcomes.

The trace file records Geodude and Onix phases separately. Their count is NOT a count of independent Brock attempts:it can count both opponents in one battle. Use presence of a Geodude phase to identify runs that reached Brock, and inspect whole fights before describing repeated losses numerically. Approximate objective/map time sums use consecutive main observations and attribute intervening work to the preceding observed state.

## Current conclusion

The decline is not a badge-counter mistake. Later runs often arrive too late or fail to reach Brock, and runs with reasonable arrival times can still lose. There is no demonstrated single causal regression yet. Seed-dependent choices, encounters/battle outcomes, timing, and shared interaction changes remain possible contributors. The original4-run recovery result is small and development-selected; treating75% as a stable baseline rate would overstate it.

## Next diagnostic experiment

Eight one-hour model runs:archived v2.21 recovery loop vs current v2.25 recovery loop, seeds8000–8003, alternating order. Both start at the bedroom. This reuses the original recovery seed IDs and holds the current machine/backend constant. It is a diagnostic crossover, not a powered new model-ranking study. Matching policy seeds does not make encounter sequences identical. If archived behavior recovers while current does not, investigate loop/guard/timing differences. If neither reproduces the earlier wins, seed labels alone do not explain them and historical runtime drift/variability need more work. Mixed/low-count outcomes may remain inconclusive.

Evidence:research/model-regression-trace-audit.json; scripts/investigate-model-regression.py; research/model-badge-crosscheck-20261017.json. No historical artifacts edited.

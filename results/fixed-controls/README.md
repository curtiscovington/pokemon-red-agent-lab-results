# Fixed-controls comparison (v2.25)

Batch20261015-132403-64e4d3:45 completed one-hour runs,15 per policy. Script12 badges,model0,random0. All15 scripts reached Pewter/Gym;model13 reached Pewter,9 entered Gym,6 encountered Brock's Geodude. Random0 reached Pewter. All12 script wins have badge-state evidence, explicit award dialogue and matching final observations.

- [Frozen study plan](protocol.md)
- [Per-run outcomes](runs.csv), [aggregate estimates](aggregate.json)
- [Uniform45-run log audit](uniform-audit.json)
- [Model badge verification across historical batches](model-badge-crosscheck.json)
- [Model decline investigation](model-regression-investigation.md)
- [Original archives and SHA-256 member index](../../batches/v2.25/archive-index.json)
- [Audit implementation](../../scripts/audit-fixed-controls.py)

Uniform audit covers every scored event in every run for badge evidence, legal responses, Brock/Onix presence, named moves and guide visits, observed HP increases in centers, navigation outcomes, and all recorded error events. Also preserves first/every100th request context samples for every run. Same scope regardless of success. This completes the same sort of uniform automated log checks used for post1; it is not an exhaustive manual frame review. Historical per-run policy-audit manual_review flags remain pending, intentionally unchanged. Publication wording must distinguish these scopes.

No malformed/out-of-enum decisions. Three timeouts:random runs19/26 at deadline;run44 observation timeout at1560s and subsequently completed. No model recovery/resource-affected flags. No exclusions among45 completed runs. Stopped v2.24 remains development evidence and is not pooled. Its four script wins and failed scripts were all excluded together.

Scene: model run17 entered Gym at1655.461s, explicitly selected go:54-object-3 ten times (first1665.837s,last3457.086s), and had no observed Geodude phase. Original frame000530.png after tenth selection shows gym-guide greeting. [Image](../../images/fixed-controls/gym-guide-run17.png). These are destination calls, not every direct-button conversation, and do not alone explain the whole run's failure.

Pewter times:script mean25:44,median25:31 (15arrivals). Model mean41:31,median38:41 among13arrivals;all15 restricted mean43:59 with two administrative censors at60min. Gym restricted means:script27:19,model49:46. Speed differences combine route/battle choices, inference delay and other execution costs, not isolated causal effects.

To reproduce (extract all46 archives into one directory):

```sh
python3 scripts/verify-fixed-controls.py
mkdir -p extracted/v2.25
for archive in batches/v2.25/*.tar.gz; do tar -xzf "$archive" -C extracted/v2.25; done
python3 scripts/audit-fixed-controls.py extracted/v2.25 --output /tmp/v225-audit.json
cmp /tmp/v225-audit.json results/fixed-controls/uniform-audit.json
python3 scripts/analyze-fixed-comparison.py extracted/v2.25
```

The saved-state checks were performed locally; ROMs and emulator saves are excluded. Published logs/frames/source permit trace re-analysis, not exact game reruns without those external inputs. Per-run archives keep each file below GitHub's file-size limit. Prior six-batch index/verifier is unchanged; this batch has its own explicit index/verifier.

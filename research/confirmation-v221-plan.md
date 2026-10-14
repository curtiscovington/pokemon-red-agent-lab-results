# v2.21: bounded navigation recovery confirmation

Supersedes interrupted v2.20 batch20261013-100905-cacc2d by explicit user request.
Do not pool its partial run with this prospective batch. Original logs/status,
source freeze and terminal save retained, with interruption.json explaining the
restart and the supervisor's shutdown cleanup timeout.

Same primary and secondary endpoints as batch-v2.19-audit-and-confirmation.md.
Eight one-hour bedroom runs, paired fresh seeds8000–8003, alternating baseline /
full recovery order. Same model, starting-state checksum, staged goals and budget.
Both arms receive shared executor repairs; only the full recovery package differs.

General rules, no map-specific route overrides:
- Stop after a moving position/action/next-position transition repeats three times.
- Interior warps try each input direction at most once from the warp position;
  do not assume all usable doorway inputs lead into ordinary walkable tiles.
- Release retained routes on detected cycles, blocked walking, or a step limit
  that finishes where it began. Exclude the failed target from action schema.
- Release exclusion on map change or moving at least four Manhattan tiles from
  the failure location. Primitive moves and other targets remain available.
- Failure memory is per-run, capped at32 targets; transition counts at96 inputs.
  Existing compact event results record movement_cycle and failed_routes. No
  extra screenshots, model, or high-volume telemetry introduced.
- Successful advancing long routes and battle interruptions retain destinations.

Validation: 42 targeted tests passed across navigation, retained intent, real ROM
starter/healing/battle controls, recovery, goals, presentation and queueing.
The production-input doorway integration additionally traverses the archived
Route2 failure into the gate, back out onto its warp, and into the gate again,
each within12 inputs. Shared fixes are frozen before launch. Four pairs are a
small confirmation, not a powered significance claim; no mid-batch edits.

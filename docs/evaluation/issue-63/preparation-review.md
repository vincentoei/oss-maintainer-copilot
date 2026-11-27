# Issue #63 preparation review

Separate Standards and Spec reviews covered this preparation against merged
baseline `28f3d36` and GitHub issue #63. Execution and generated-report review are
not completed by this source review. The application default remains unchanged.

## Standards

No documented-standard breaches. The review found and resolved three issues:

- A durable reservation could outlive its report/call file on interruption. The
  scorer now reconciles ledger and call files onto all planned observations,
  retains missing results as charged-without-result and awards no agreement.
  The runner also persists KeyboardInterrupt state before propagating it.
- Historical and integration reports previously checked only selected type and
  quote nullness. They now replay through production report construction and
  compare complete report/context fields (excluding fresh trace IDs and context
  preparation timestamps). Missing private historical snapshots are disclosed.
- Browser verification hashed one executable but allowed Playwright to resolve
  another. Launch now passes the exact verified executable path.

The transport remains guarded in its closed state before server shutdown and
after execution, so late HTTP/browser workers cannot recover a bare model
transport. Budget matching also requires the active model alias before dispatch.
The final reviewer found no further material correctness concerns.

## Spec

The initial review identified GPU-placement verification, incomplete quote/reply
playback, and interruption-accounting gaps. All were corrected before freezing.
Reported placement is recomputed from captured digest, context and byte counts;
this does not establish physical tensor residency. Fresh and integration inputs
are public and replayable; diagnostics use the verified retained snapshot or
explicitly state which report fields were not replayed.

The independent Spec reviewer replayed all 45 fixed/diagnostic simulated reports
and checked reservation-only, saved-call and KeyboardInterrupt reconciliation.
Its sandbox could not repeat the full browser simulation because local sockets
were denied; the parent run exercised all 53 report paths and 55 reservations
with fake model responses, including the actual browser form/backend. No real
model calls, quality judgments or human report ratings followed from these tests.

All twelve expected types have actual user confirmation. The protocol keeps
fresh synthetic cases separate from exposed diagnostics, declares 55 calls /
14,080 output tokens, and requires explicit approval tied to the source/input
freeze. No actual default promotion is implied. Final review supports freezing
the preparation, with live evaluation and human ratings still outstanding.

Standards: 0 remaining findings. Spec: 0 remaining findings. The pre-freeze
accounting, playback and browser-path findings were resolved.

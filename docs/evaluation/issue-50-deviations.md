# Protocol execution deviations (before reserved outputs)

Iteration 1 completed only control A (20 dispatches), not B. Code review before
candidate inference found A lacked the additional passages intended for matching
underlying evidence. Treat that A run as unmatched observational evidence, not
promotion evidence. No quality rating was assigned or used for tuning. Its
responses, failed type selection and complete request ledger remain preserved.

Iteration 2 uses A and B with identical underlying opening/passages and common
512-token limit, then stops development regardless of usefulness. This reallocates
the planned 20-request B rerun to a corrected A run: still 60 development requests,
at most two development iterations and 120 total requests. This differs from the
published arm schedule, and must remain disclosed in any decision. The original
thresholds, reserved split, limits and one-pass pilot rule do not change. No
additional development iteration is authorized.

Corrected A receives the same passage payload as B while retaining selection-only
schema/task; B can propose a supported question or extractive explanation. Prompt
representation and schema differ by design. Cross-model B/C/D must freeze those
differences away. Rendering/validation corrections come from synthetic adversarial
review, never pilot contents. Pilot originals were inspected only for selection
and proposed annotation; their outputs have not been generated.

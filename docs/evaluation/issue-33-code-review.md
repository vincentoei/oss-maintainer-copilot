# Issue #33 two-axis code review

Fixed point: `422876ddae78d1638b6f1980fec5a28f42932355` (updated main).
Initial review command: `git diff 422876ddae78d1638b6f1980fec5a28f42932355...HEAD`.
Initial reviewed commit: `f65dfb7 feat(repositories): register and triage public GitHub repositories`.
Separate fresh-context Standards and Spec agents reviewed independently, then
rechecked the worktree corrections. Spec source: GitHub issue #33. Standards:
AGENTS.md, its linked agent instructions, glossary, ADRs, pyproject.toml and CI,
plus the skill's Fowler smell baseline. No CONTRIBUTING/CODING_STANDARDS file exists.

## Standards

No documented-standard breaches found. Two initial judgment-call observations:

- Duplicated quote/negation validation between repository context and pytest
  evaluation is resolved: `label_evidence.py` now owns the algorithm, with the
  compatible pytest wrapper retained. The reviewer verified both call sites.
- Possible repeated profile switches remain a **non-blocking heuristic**. The
  reviewer accepted the rationale that these branches select the deliberately
  supported bundled pytest and generic policies; additional repository
  registrations add no branch. ADR-0004 records that boundary. Another policy
  abstraction would offer limited benefit within #33; revisit if new built-in
  policies add dispatch sites.

The reviewer also verified `SourceExcerpt.validates_location` consolidates
HTTP/fixed/agent provenance, requested-location and output-bound validation, with
a public regression for injected foreign source evidence. Code inspection only;
the Standards agent claimed no test execution or inference.

## Spec

Three initial P2 findings were fixed, each after a failing public regression:

- Markdown preparation previously truncated a twenty-first configured requirement
  without an omission. Oversized heading sets are now explicitly omitted with
  an actionable error, preserving honest limited context.
- Fenced Markdown examples previously established form headings and false missing
  requirements. A shared section scanner now excludes fenced/indented code and
  uses the same structure to find section answers and template citation lines.
- The Python `structured_template_available=False` control was ignored unless
  another historical override was supplied. It now disables conclusions after
  context resolution on fixed and optional agent paths.

The reviewer rechecked all three with direct offline reproductions and found no
remaining actionable Spec defect or scope creep. It also confirmed consistent
source validation. Its attempted HTTP pytest run stalled in the restricted
sandbox and is not counted as a successful check; the parent's public regressions
ran outside that sandbox and are recorded in the acceptance report.

Initial findings: Standards 2 heuristics / Spec 3 P2 defects. Remaining: Standards
0 documented breaches and 1 non-blocking heuristic / Spec 0 actionable defects.


The later PR verification found two additional P2 defects at `b25d574`; these were
reproduced and corrected in the follow-up fix. Its separate
[Standards and Spec review](issue-33/follow-up/fix-review.md) reports zero findings
in the new diff, backed by public regressions and a real browser verification.

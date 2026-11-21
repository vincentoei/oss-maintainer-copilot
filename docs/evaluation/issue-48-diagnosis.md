# Issue #48 diagnosis before fixes

Base: `04755b8d2a8db6d6a1ccb326bee965439c2d70db`. The immutable
[real before run](issue-45-results.json), [human reasons](issue-45-human-review.json)
and [hash manifest](issue-48-provenance.json) are the starting evidence.
[Controlled isolation](issue-48-isolation-before.json) replays all twenty openings
with content verification, original cutoffs, pinned commits and the same candidate
catalog. Its client selects every permitted statement and abstains on type.
It establishes available choices and rendering behavior, never model quality.
Contributor bodies were acquired into `/tmp`, not added as fixtures (ADR 0003).

## Falsifiable hypotheses and isolation

1. Detail rules create redundant requests: selecting all or only required IDs will
   reproduce the requests without a real model. Confirmed: #12116 package table
   fails the exact heading recognizer; #12201/#12226/#12228 scenario prose fails the
   limited use-case patterns. Both public API tests reproduce the package request.
2. Candidate assessment creates noise: keeping the candidate source fixed and
   replacing model selection cannot improve the report's relationship fields.
   Confirmed: `issue_search.assess_match` accepts one shared title word or two body
   words, including template boilerplate/code/URLs, and emits alphabetically sorted
   overlap. `triage_issue` publishes these fields before calling the model. The
   model receives the generated reason, title/URL, but not the candidate body.
3. The reply-choice construction prevents targeted follow-up: a select-all client
   still cannot produce the requested investigation. Confirmed for #12146/#12204/
   #12219: no comparison/clarification/minimization statement exists. The model
   cannot write new text under `ModelSuggestion`; rendering only copies selected
   statements. It passes through these omissions rather than creating them.
4. Model selection independently loses useful choices or fails validation.
   Confirmed #12079: #11871 was offered but omitted. #12216's type/quote mismatch
   is rejected by `validate_suggestion`; fallback abstains. This is a model-choice
   failure, distinct from missing options and retrieval noise. Do not relax the
   validator to improve apparent quality.

## Twenty-case matrix

Each row refers to its `issue_number` in the before and isolation JSON files.
The isolation artifact records exact required IDs, available statement text,
controlled report, content hash, cutoff and commit. The before artifact supplies
raw real selections, type quotes, final reports and retrieval/model trace events.
Opening evidence is linked by issue number; later comments are annotation only.

| Issue | Symptom from review | Relevant input → output | Observed cause / bounded limit |
| --- | --- | --- | --- |
| [7312](https://github.com/pytest-dev/pytest/issues/7312) | #349 connection obscured; #7012 noise | Fixture-derived parameter request + #349 body → “case, currently, def” | Assessment loses substantive connection. #2959 is a regression, not automatically a duplicate. Frozen generic template profile intentionally abstains on details. |
| [10156](https://github.com/pytest-dev/pytest/issues/10156) | Repeats linked #2959 without contribution guidance | Dynamic fixture documentation proposal → overlap statements only | Candidate reason and available reply limits. No evidence authorizes welcoming contribution or picking documentation location; those answers remain unresolved. |
| [12053](https://github.com/pytest-dev/pytest/issues/12053) | Debugger request unanswered; fixture noise | `--pdbcls` configuration proposal → #8655 plus fixture matches | Detail fix from #45 works. Assessment admits unrelated topics; no verified configuration guidance offered. |
| [12072](https://github.com/pytest-dev/pytest/issues/12072) | Understates #12066; no details | Same `call_runtest_hook` import error → related overlap | Assessment ignores distinctive error. `template_for` misses “broken” in title; no mandatory detail statements. |
| [12079](https://github.com/pytest-dev/pytest/issues/12079) | Redundant use-case request; omits #11871 | Interdependency investigation prose → missing use case; #11871 offered → not selected | Parser causes redundant request; model independently omits supported lead. Empty alternative section genuinely lacks an answer. |
| [12081](https://github.com/pytest-dev/pytest/issues/12081) | Generic documentation/source claims | `readouterr` output loss + pinned reset docstring → generic source-line existence statement | Assessment/statement construction, not renderer. Verified excerpt has resetting text, but deeper behavior not proved by line existence. |
| [12083](https://github.com/pytest-dev/pytest/issues/12083) | Vague abstention despite collection example | Pytest 7/8 comparison → no reply options | `template_for` misses regression prose; verified opening already has example. No supported diagnosis available; cannot promise intended behavior. |
| [12116](https://github.com/pytest-dev/pytest/issues/12116) | Asks for supplied packages | Backticked compound heading + Package/Version table → required pip-list ID | Exact heading recognizer creates request; model must select it. Renderer passes it through. Child-process support/contribution decision remains unresolved. |
| [12146](https://github.com/pytest-dev/pytest/issues/12146) | No controlled comparison | Different session versions and printed tuple order → zero choices | Reply construction lacks evidence-supported comparison. No evidence establishes fixture-scope root cause. |
| [12189](https://github.com/pytest-dev/pytest/issues/12189) | JUnit/capture interaction ignored; noise | `-s`, `junit_logging`, XML output → readouterr overlaps | Assessment conflates capture scenarios. A one-variable rerun can be proposed without asserting an undocumented cause. OS version remains absent; title doesn't select bug template. |
| [12197](https://github.com/pytest-dev/pytest/issues/12197) | No actual configuration/test request | `log_disable` ineffective in ini → configuration-theme matches | Weak assessment and template selection; no verified evidence of supported ini setting. Do not claim addopts fixes it from later comments. |
| [12201](https://github.com/pytest-dev/pytest/issues/12201) | Supplied use case/workaround requested | Windows/POSIX path tests + copied `skipif` tests → two required requests | Use-case and alternative recognizers miss “I'm currently writing” / “making use” prose. Both requests originate upstream. |
| [12203](https://github.com/pytest-dev/pytest/issues/12203) | Generic example request despite sketch | Non-runnable fixture sketch + unchecked minimal example → mandatory generic request | Missing example is supported; request lacks logging/configuration/exception specificity. Other relationships are overlap noise. |
| [12204](https://github.com/pytest-dev/pytest/issues/12204) | Conflicting versions ignored; noise | Package pytest/pluggy 8.1.1/1.4.0 vs session 8.0.0/1.3.0 → no clarification | Reply construction offers irrelevant relationships only. Controlled select-all cannot create version clarification. No traceback root cause inferred. |
| [12216](https://github.com/pytest-dev/pytest/issues/12216) | Fallback gives no help | Collection-error opening → invalid type quote → validation failure | Model choice fails validation; template selection also misses bug context. Preserve rejection and partial report. Unresolved fixture-injection guidance needs verified API evidence. |
| [12219](https://github.com/pytest-dev/pytest/issues/12219) | Ignores working-vs-affected discrepancy | Hook works in minimized example; affected external project not fetched → #4064 overlap | Reply construction misses request for a minimized *failing* example. Bare `def test` is insufficient proof of reproduction. No external project diagnosis permitted. |
| [12223](https://github.com/pytest-dev/pytest/issues/12223) | JUnit message-vs-body request ignored | Concrete assertion + parser failures → unrelated overlap statements | Assessment and choices; no evidence to prescribe XML change. Title doesn't select template. This specialized guidance remains unresolved. |
| [12224](https://github.com/pytest-dev/pytest/issues/12224) | #11871 confuses test selection with session control | Session lifecycle proposal vs argument-file request → related | Template/code overlap causes false relationship; candidate lacks shared lifecycle behavior. No verified public session API to recommend. |
| [12226](https://github.com/pytest-dev/pytest/issues/12226) | Bash/CI use case requested again | Bash/CI quote difficulty + proposed syntax → missing use case | Scenario recognizer misses explicit domain prose; empty alternatives remain genuinely absent. Can ask for failing command without claiming shell fix. |
| [12228](https://github.com/pytest-dev/pytest/issues/12228) | Concrete docs gap gets generic requests | TOML addopts types and target pages → missing use case/alternative | Parser misses concrete configuration scenario. Expected alternative request is preserved for comparability, though its usefulness is disputed. Actual TOML parsing semantics need verified source evidence; not inferred from proposed docs. |

## Scope of fixes

Recognize bounded supplied-detail patterns, require substantive technical anchors
and source excerpts for relationships, and offer bounded investigative questions
supported by opening evidence. Keep existing model selection schema, validation,
read-only tool limits, partial reports and abstention. Record any retrieval-recall
regression rather than treating conservative filtering as universally better.
#16 workflow comparison and #33 repository expansion remain outside this work.

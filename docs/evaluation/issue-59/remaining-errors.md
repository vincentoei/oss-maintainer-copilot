# Where the 21 disagreements come from

At 8d52071 Qwen selected bug 31 times, enhancement 17, regression once and docs
once. All 13 expected bugs and all 14 expected enhancements were correct.
The other two agreements were a regression and a docs report. The six recovered
cases offset six previously correct cases. There were 50 valid selections,
zero abstentions, and zero unavailable expected types. In contrast the old
contract made 18 answers unreachable. The initial free-quote replacement had
19 validation failures and 14/50 agreement. The indexed follow-up used a
separately frozen 50-call extension after the original 100. [Phase records](../issue-60.md)

These are opening-level diagnostic observations by the investigator. I checked
all 21 disputed openings and the focal docs gain against their catalog content
hashes and creation timestamps, inspected the sampled options from the actual
encoder, and compared the selected quotes with the recorded rationales. The
table describes possible explanations, without assigning new expected types or
rating generated reports. Numbers refer to pytest-dev/pytest. Bold numbers are
regressions. [Recorded selections and excerpts](../issue-60/type-changes.json)

| Expected → selected | Cases | What the opening and available excerpts distinguish |
|---|---|---|
| regression → bug | 12083, 12263, 12293, **12328**, 12367 | Compared releases, prior working version, or introducing commit are visible in the options. 12293 explicitly describes previously passing tests after an upgrade. 12328's selected title itself names the break. Bug describes a symptom but misses the change over time. |
| regression → bug | 12273, 12308 | 12273 gives a failure on one release and downstream compatibility uncertainty. Its family relationship helps the annotation. 12308 names a possible introducing change in the opening, but the sampled body is dominated by logs and packages. |
| question → bug | **12189**, 12242, 12357 | Title names a failure. 12189's closing request for help is missing from the options. Package trees or stack frames dominate 12242/12357. Option discovery and hook semantics need interpretation. The whole body remains available. |
| question → bug | 12197, 12287, **12298**, 12305 | 12197 reports ineffective settings without an explicit question, making intent debatable from the opening. 12287 asks if the behavior is expected in an available option. 12298 asks for a fixture-lifetime explanation but the selected quote is an HTML tag. 12305 asks for help with ordering and considers several explanations. |
| docs → enhancement | 10156, **12228** | Request to document behavior resembles a feature request, particularly with a feature template. The requested artifact is explicit even in the offered title. |
| docs → bug | **12360** | Old guidance and observed assertion output conflict. Both a runtime fix and a text correction are plausible from the title alone. Sampling drops the full disputed claim, while the complete body identifies it. |
| selftests → bug | 12323, 12352 | Offered excerpts identify pytest's own failing test nodes or explicitly name a self test. Qwen selects a fence or the title, then classifies the failure generically. |
| null → bug | **12278** | All five excerpts offered. No code, package list or OS release establishes why six processes appeared. The accepted abstention reflects uncertainty about the cause even with a temporal association. |
| proposal → enhancement | 12376 | A public fixture-registration API would also be an enhancement. Choosing one of these overlapping repository labels requires a convention beyond the literal request. |

Four regressions gained a previously unavailable wrong alternative. Bug was
absent for 12189, 12298, and 12360. No label was offered for 12278. The other two
regressions (12228 and 12328) chose labels already offered before. Choice-set
expansion alone cannot explain those two. Prompt wording, quote representation
and schema changed together in #60, so the paired records cannot isolate their
individual effects. [Old availability](../issue-60/before/results.json)

Seven of eight expected regressions and all seven expected questions went to
bug. This concentration, including mistakes with decisive text in the selected
quote, rules out unavailable labels and missing excerpts as *necessary*
explanations. Excerpt coverage can still affect particular cases. The prompt
supplies label names and broad intent guidance but no precedence for overlapping
categories. Whether definitions improve selection is an empirical question.
Linked later diagnoses can explain an annotation to a reviewer but do not
belong in historical inputs. A model change, taxonomy-wide definitions, quote
resampling or calibration work would require separate scope and measurements.

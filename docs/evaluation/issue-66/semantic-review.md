# Actual report semantic review for issue #66

Reviewer: Codex implementing issue #66 (GPT-6 family; exact deployed variant unavailable). **AI review, not human ratings.**

Not blinded or independent: reviewer authored candidate/examples and knew outcomes and expectations. No additional model/API calls produced these judgments. Attributed AI assessment does not satisfy the frozen human adoption gate.

All actual report types/quotes, complete synthetic inputs and sampler options, hash-verified retained historical openings at original cutoffs, and complete saved report/citation payloads. No later live issue labels, edits or comments used.

Whole-input type support and actual selected-quote relevance are separate yes/no/uncertain/N/A judgments. Null types receive N/A plus separate abstention-appropriateness judgments. Semantic support is distinct from preferred benchmark agreement.

The requesting user confirmed new expected outcomes and authorized execution in `approval.json`; that response does not rate these generated reports. All 48 report reviews follow.

## control / ordinary-bug

[Actual report](run/control-ordinary-bug-report.json) · fingerprint `e26cea2db0d8a69bfd245fc128e8a76888b62ca690660229c5adcbd91e5f081f`

Selected type: `type: bug`

Selected quote:

> The test passes, but its finalizer never closes the file on either release I tested. Please fix the leaked file.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The finalizer fails to close a file on both releases. The complete selected quote states the malfunction and persistence, supporting bug without a version break.

Human review: pending.

## candidate / ordinary-bug

[Actual report](run/candidate-ordinary-bug-report.json) · fingerprint `7fa915165b331503064ad6d4db7eccc10d23f98519581683fa5c51397cf50039`

Selected type: `type: bug`

Selected quote:

> The test passes, but its finalizer never closes the file on either release I tested. Please fix the leaked file.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The finalizer fails to close a file on both releases. The complete selected quote states the malfunction and persistence, supporting bug without a version break.

Human review: pending.

## control / version-break

[Actual report](run/control-version-break-report.json) · fingerprint `d58c1778a10d9fab76095a756c5705131e5cfc676672c96669248a3915881ab5`

Selected type: `type: regression`

Selected quote:

> The same test closes the file on pytest 8.2 but leaks it on 8.3. Reinstalling 8.2 restores cleanup.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The same test works on 8.2, fails on 8.3 and recovers on reinstalling 8.2. The selected quote retains that controlled comparison, supporting regression.

Human review: pending.

## candidate / version-break

[Actual report](run/candidate-version-break-report.json) · fingerprint `b29c340bb838bd1b949d5fec0983422eeafe7002d8ed651d074c9cf8fcecab76`

Selected type: `type: regression`

Selected quote:

> The same test closes the file on pytest 8.2 but leaks it on 8.3. Reinstalling 8.2 restores cleanup.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The same test works on 8.2, fails on 8.3 and recovers on reinstalling 8.2. The selected quote retains that controlled comparison, supporting regression.

Human review: pending.

## control / old-docs

[Actual report](run/control-old-docs-report.json) · fingerprint `b8dfa36f102b14ce54c5cfedb484d2acfdbf359d346926ef566c17e50548705c`

Selected type: `type: question`

Selected quote:

> The documented hook never runs in my project. An older manual also lists this hook; I have not tried an older release.

Whole-input type support: **no**. Selected-quote relevance: **no**. Abstention appropriate: **N/A**.

The input and quote report a documented hook failing, without asking how to use functioning behavior. They support an ordinary bug, not the selected question; an older manual does not establish a version break.

Human review: pending.

## candidate / old-docs

[Actual report](run/candidate-old-docs-report.json) · fingerprint `fa9b359f3ad8deba0c1cb403ecaf8e6b31f6ec741412c127d1836ff40f8bc270`

Selected type: `None`

Selected quote:

*Abstained; no selected quote.*

Whole-input type support: **N/A**. Selected-quote relevance: **N/A**. Abstention appropriate: **no**.

The candidate avoids inventing a version comparison but abstains despite an offered complete quote supporting an ordinary hook malfunction. This is avoidable abstention and remains an expected-type miss.

Human review: pending.

## control / extension

[Actual report](run/control-extension-report.json) · fingerprint `040578c6049bc977ec7f2306ee6bab38f210adfde00f638c1a71b2d57235af47`

Selected type: `type: enhancement`

Selected quote:

> The XML output is valid and consumers work. Please add a separate option to shorten the message attribute.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

Working XML and consumers plus an explicit new option request support enhancement. The selected quote includes current functioning behavior and the requested change.

Human review: pending.

## candidate / extension

[Actual report](run/candidate-extension-report.json) · fingerprint `633302bddd8884c1fd08b29571f193d2b579b5439bace5bba674da750ced578d`

Selected type: `type: enhancement`

Selected quote:

> The XML output is valid and consumers work. Please add a separate option to shorten the message attribute.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

Working XML and consumers plus an explicit new option request support enhancement. The selected quote includes current functioning behavior and the requested change.

Human review: pending.

## control / overlap

[Actual report](run/control-overlap-report.json) · fingerprint `be4e6a093d0086144367d6aaa963239a75cb87288fb5867dd6415e18184dc1db`

Selected type: `type: enhancement`

Selected quote:

> My consumer crashes on large valid message attributes; please add a separate attribute-size option.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The consumer malfunction supports bug, and the explicit attribute-size option request also supports enhancement. The quote includes both; enhancement is defensible despite the unchanged preferred bug expectation.

Human review: pending.

## candidate / overlap

[Actual report](run/candidate-overlap-report.json) · fingerprint `dae6d1c65e2d433c595699184fb8de0e52d31d7bec2fa8cf8a60cef8d7d1e771`

Selected type: `type: enhancement`

Selected quote:

> My consumer crashes on large valid message attributes; please add a separate attribute-size option.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The consumer malfunction supports bug, and the explicit attribute-size option request also supports enhancement. The quote includes both; enhancement is defensible despite the unchanged preferred bug expectation.

Human review: pending.

## control / quote-misses-request

[Actual report](run/control-quote-misses-request-report.json) · fingerprint `bbb5279244675ec96b20e8526d939aaee8d724c9ebd35192a307fd8eef033463`

Selected type: `type: enhancement`

Selected quote:

> I am requesting a new optional attribute-size limit, not a repair to existing XML output.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The selected quote explicitly requests a new optional size limit and disclaims repairing existing XML output. It supports enhancement; neither arm selects the failure-only counterexample.

Human review: pending.

## candidate / quote-misses-request

[Actual report](run/candidate-quote-misses-request-report.json) · fingerprint `665c5fc8478671b1c8421edca83b4e9976baa0d0cf4f97fb6094376d209c1df3`

Selected type: `type: enhancement`

Selected quote:

> I am requesting a new optional attribute-size limit, not a repair to existing XML output.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The selected quote explicitly requests a new optional size limit and disclaims repairing existing XML output. It supports enhancement; neither arm selects the failure-only counterexample.

Human review: pending.

## control / insufficient

[Actual report](run/control-insufficient-report.json) · fingerprint `cc1c5587a688838fdc1cb293bb06839bcdb9bb914c8f1cc2e79a21d452284a3e`

Selected type: `None`

Selected quote:

*Abstained; no selected quote.*

Whole-input type support: **N/A**. Selected-quote relevance: **N/A**. Abstention appropriate: **yes**.

Both type fields abstain. The input explicitly withholds a problem, desired change or question, so abstention is appropriate.

Human review: pending.

## candidate / insufficient

[Actual report](run/candidate-insufficient-report.json) · fingerprint `27076f901169c3727211265b013c39b6e9dad940c764e510c17003ea474dc4f9`

Selected type: `None`

Selected quote:

*Abstained; no selected quote.*

Whole-input type support: **N/A**. Selected-quote relevance: **N/A**. Abstention appropriate: **yes**.

Both type fields abstain. The input explicitly withholds a problem, desired change or question, so abstention is appropriate.

Human review: pending.

## control / negated-comparison

[Actual report](run/control-negated-comparison-report.json) · fingerprint `ce2fa7a340c9b2d98f6278a6d926a6e3dc7caa8cfb55c765323fc923c3fc291c`

Selected type: `type: bug`

Selected quote:

> The file leaks on both 8.2 and 8.3; the claim that switching back restores cleanup was mistaken.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

Both versions leak and the restoration claim is explicitly retracted. The complete selected quote supports persistent bug and contradicts a demonstrated version break.

Human review: pending.

## candidate / negated-comparison

[Actual report](run/candidate-negated-comparison-report.json) · fingerprint `7398edaa4b351a4dd1007acdfb001c52af2cc086682faa0a613c792a5f6d88e9`

Selected type: `type: bug`

Selected quote:

> The file leaks on both 8.2 and 8.3; the claim that switching back restores cleanup was mistaken.

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

Both versions leak and the restoration claim is explicitly retracted. The complete selected quote supports persistent bug and contradicts a demonstrated version break.

Human review: pending.

## control / omitted-support

[Actual report](run/control-omitted-support-report.json) · fingerprint `2b0174c98ec821e7c4dc18c68b07222a6da0413c90ea8def6e41e425031012ef`

Selected type: `type: regression`

Selected quote:

> Observation 01: no additional diagnostic information.

Whole-input type support: **yes**. Selected-quote relevance: **no**. Abstention appropriate: **N/A**.

The whole input contains a credible unchanged-test version break, so regression has whole-input support. The selected generic observation has no diagnostic evidence. The informative line is absent from all offered quotes; the frozen report-contract expectation remains null.

Human review: pending.

## candidate / omitted-support

[Actual report](run/candidate-omitted-support-report.json) · fingerprint `7be0dfe37a2845a1a5d5d89dc9ac28686b6a8e459bca3e062fd13955bf7e5183`

Selected type: `None`

Selected quote:

*Abstained; no selected quote.*

Whole-input type support: **N/A**. Selected-quote relevance: **N/A**. Abstention appropriate: **yes**.

The sampler omits the only informative comparison while retaining it in the full input. The candidate abstains appropriately under the selected-quote support contract; this does not mean the whole input lacks regression evidence.

Human review: pending.

## control / log-bug

[Actual report](run/control-log-bug-report.json) · fingerprint `bc3fe33c8ca6074e54590e2e8553d60e889e224dca1ebb01cee07758efe5c52d`

Selected type: `type: bug`

Selected quote:

> With --log-file enabled, each emitted log record appears twice in the output file. The same unchanged project shows this on both pytest 8.2 and 8.3. Please fix

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The selected quote describes duplicate log records on both versions, supporting persistent bug. Clipping the final request does not remove the malfunction or comparison.

Human review: pending.

## candidate / log-bug

[Actual report](run/candidate-log-bug-report.json) · fingerprint `f32134551842ecc3215128793c76b91dd46a99a17ff76864fb70dbd2408d5f02`

Selected type: `type: bug`

Selected quote:

> With --log-file enabled, each emitted log record appears twice in the output file. The same unchanged project shows this on both pytest 8.2 and 8.3. Please fix

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The selected quote describes duplicate log records on both versions, supporting persistent bug. Clipping the final request does not remove the malfunction or comparison.

Human review: pending.

## control / log-regression

[Actual report](run/control-log-regression-report.json) · fingerprint `4cfe06f9f1099ecf10b102a3de83665e37f8d54bb552e9394c9ca21ad9ff9a4e`

Selected type: `type: regression`

Selected quote:

> The unchanged project writes each log record once with pytest 8.2 and twice with 8.3. Switching back to 8.2 restores single writes. Please restore the earlier b

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The selected quote retains single writes on 8.2, duplicate writes on 8.3 and restoration on switching back, supporting regression despite its clipped ending.

Human review: pending.

## candidate / log-regression

[Actual report](run/candidate-log-regression-report.json) · fingerprint `d85a92f0fc700d23483d834415ac624bd08df93982386b5ce7cc9ba2bd78e317`

Selected type: `type: regression`

Selected quote:

> The unchanged project writes each log record once with pytest 8.2 and twice with 8.3. Switching back to 8.2 restores single writes. Please restore the earlier b

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The selected quote retains single writes on 8.2, duplicate writes on 8.3 and restoration on switching back, supporting regression despite its clipped ending.

Human review: pending.

## control / fixture-question

[Actual report](run/control-fixture-question-report.json) · fingerprint `f6f2a7f6fac4dc92c76aeb8077d5145278d3f1ad406ea633c2d33c9534621c8b`

Selected type: `type: question`

Selected quote:

> My function-scoped connection fixture opens and closes correctly. I want to reuse one connection across all tests in a module. Which fixture scope should I choo

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

Correct fixture behavior and a request for help choosing a reuse scope support question. The quote retains working behavior, desired reuse and the scope query despite a clipped final word.

Human review: pending.

## candidate / fixture-question

[Actual report](run/candidate-fixture-question-report.json) · fingerprint `30a633b3cac750bb171e65a89f313e6a77a9345ee9ad08dc4233fb12fa7bac46`

Selected type: `type: question`

Selected quote:

> My function-scoped connection fixture opens and closes correctly. I want to reuse one connection across all tests in a module. Which fixture scope should I choo

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

Correct fixture behavior and a request for help choosing a reuse scope support question. The quote retains working behavior, desired reuse and the scope query despite a clipped final word.

Human review: pending.

## control / fixture-bug

[Actual report](run/control-fixture-bug-report.json) · fingerprint `2c816b3cbe0d6c6c2c8b2e9dc41cbb0af882ce892f0f43e1345976f65302cde4`

Selected type: `type: bug`

Selected quote:

> A function-scoped fixture opens one connection, yields it to one passing test, and should then close it. Its teardown never runs, leaving the connection open. T

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The selected quote reports that a yielded connection remains open because teardown never runs; this supports bug. The full input says it also happens on the previous release, without a demonstrated working version.

Human review: pending.

## candidate / fixture-bug

[Actual report](run/candidate-fixture-bug-report.json) · fingerprint `c2c5b41d9aaf2760efa3320347da0d71abbacdd43d6b8b2b10ffd542a9cea989`

Selected type: `type: regression`

Selected quote:

> his also happens on the previous release.

Whole-input type support: **no**. Selected-quote relevance: **no**. Abstention appropriate: **N/A**.

The full input says teardown fails on the previous release too; it establishes no version that worked. The selected fragment only says the same issue happens on the previous release. Both the regression inference and its quote are unsupported, losing a previously supported ordinary-bug report.

Human review: pending.

## control / exit-bug

[Actual report](run/control-exit-bug-report.json) · fingerprint `178e2128cab7c8133b18ca0ba5387a153658b37748fa01e2950f54c45b2d6f16`

Selected type: `type: bug`

Selected quote:

> A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote contains the failing-test/zero-exit-status mismatch, supporting bug. The full input reports the same problem across tested releases, not a working-to-broken change.

Human review: pending.

## candidate / exit-bug

[Actual report](run/candidate-exit-bug-report.json) · fingerprint `b332cc00fb85cbfa689d16e6ae26bce8a9bbdb05c7d4c8f0f22664996acd3ce7`

Selected type: `type: bug`

Selected quote:

> A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote contains the failing-test/zero-exit-status mismatch, supporting bug. The full input reports the same problem across tested releases, not a working-to-broken change.

Human review: pending.

## control / exit-regression

[Actual report](run/control-exit-regression-report.json) · fingerprint `377c925c1ab1e65bc083f28984c7aaa60b2aaaa46f43a529c96dec2972c55114`

Selected type: `type: regression`

Selected quote:

> For the same failing test, pytest 8.2 exits with status 1 and pytest 8.3 exits with status 0. The summary reports the failure in both. Reinstalling 8.2 restores

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote retains the same failing test, status 1 on 8.2, status 0 on 8.3 and restoration after reinstalling 8.2. It supports regression despite clipping the final status digit.

Human review: pending.

## candidate / exit-regression

[Actual report](run/candidate-exit-regression-report.json) · fingerprint `51b22f4343cc5128f1a5b9ae34456c47f0442b36487345f9771a136bd9333e61`

Selected type: `type: regression`

Selected quote:

> For the same failing test, pytest 8.2 exits with status 1 and pytest 8.3 exits with status 0. The summary reports the failure in both. Reinstalling 8.2 restores

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote retains the same failing test, status 1 on 8.2, status 0 on 8.3 and restoration after reinstalling 8.2. It supports regression despite clipping the final status digit.

Human review: pending.

## control / precedence-docs

[Actual report](run/control-precedence-docs-report.json) · fingerprint `3ba3d31c8d38d1094d12b4db3dd7f341d1eec9017ef7e138282e4db708f1b1b0`

Selected type: `type: docs`

Selected quote:

> The reference says a project configuration value overrides the command-line value. The implementation and intended behavior give the command line priority. Plea

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote contrasts incorrect reference guidance with intended implemented precedence, supporting docs. The clipped correction request does not remove the documentation defect.

Human review: pending.

## candidate / precedence-docs

[Actual report](run/candidate-precedence-docs-report.json) · fingerprint `6a1450177a5b890c3197f5dd2206963fbdaad014d3e66d5f75c48045f004a133`

Selected type: `type: docs`

Selected quote:

> The reference says a project configuration value overrides the command-line value. The implementation and intended behavior give the command line priority. Plea

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote contrasts incorrect reference guidance with intended implemented precedence, supporting docs. The clipped correction request does not remove the documentation defect.

Human review: pending.

## control / precedence-question

[Actual report](run/control-precedence-question-report.json) · fingerprint `4183d7437243234646dfc6dc31c99df921a0e63fea3215eafed7653c4a6ef47c`

Selected type: `type: question`

Selected quote:

> The reference correctly says the command line overrides project configuration, and that works for me. How can I choose a different value for just one invocation

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote says documented precedence works and asks how to choose a per-invocation value. It supports question, with intent intact despite the clipped ending.

Human review: pending.

## candidate / precedence-question

[Actual report](run/candidate-precedence-question-report.json) · fingerprint `f4faceb48672f759417c72fffb184259f68349c586e90ed36fc6b5639f27a720`

Selected type: `type: question`

Selected quote:

> The reference correctly says the command line overrides project configuration, and that works for me. How can I choose a different value for just one invocation

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote says documented precedence works and asks how to choose a per-invocation value. It supports question, with intent intact despite the clipped ending.

Human review: pending.

## control / teardown-regression

[Actual report](run/control-teardown-regression-report.json) · fingerprint `b12b1dcb3e4b458847561d283d2d582f5c2727b0bf084d679db5eaf701aa2222`

Selected type: `type: regression`

Selected quote:

> The same plugin and test suite close their temporary directory at session end with pytest 8.2. After upgrading to 8.3, the cleanup callback is never called. Rol

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote retains the same suite and plugin, working cleanup with 8.2 and a missing callback after upgrading to 8.3. This supports regression even before the clipped rollback sentence.

Human review: pending.

## candidate / teardown-regression

[Actual report](run/candidate-teardown-regression-report.json) · fingerprint `cd959e5d636bf9b057b1764d223bebc47bc8fc62921de82ec5725afcaaf8c9cf`

Selected type: `type: regression`

Selected quote:

> The same plugin and test suite close their temporary directory at session end with pytest 8.2. After upgrading to 8.3, the cleanup callback is never called. Rol

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote retains the same suite and plugin, working cleanup with 8.2 and a missing callback after upgrading to 8.3. This supports regression even before the clipped rollback sentence.

Human review: pending.

## control / traceback-bug

[Actual report](run/control-traceback-bug-report.json) · fingerprint `1f90bd0242e3c5b0e5f8240cfd39d16d67fa2caa3d6900f3057d9861205b22b9`

Selected type: `type: bug`

Selected quote:

> A failing test raises ValueError with a message, but the displayed traceback attributes it to an unrelated test that passed. The problem occurs on both tested r

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote attributes a failing test traceback to an unrelated passing test. This mismatch supports bug; a version comparison is unnecessary for that broad category.

Human review: pending.

## candidate / traceback-bug

[Actual report](run/candidate-traceback-bug-report.json) · fingerprint `525e648eb5628b26c7b78e580c74948f8e7b6bc875f7300807430b7463fb1c91`

Selected type: `type: bug`

Selected quote:

> A failing test raises ValueError with a message, but the displayed traceback attributes it to an unrelated test that passed. The problem occurs on both tested r

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote attributes a failing test traceback to an unrelated passing test. This mismatch supports bug; a version comparison is unnecessary for that broad category.

Human review: pending.

## control / warning-question

[Actual report](run/control-warning-question-report.json) · fingerprint `6ce5eea34474aa2ea437e0a80673d20b7e3224143acdbed7f99709b04de7ff2b`

Selected type: `type: question`

Selected quote:

> All my tests pass, and the warning correctly describes a deprecated option I still use. Where can I configure pytest to hide this warning temporarily while I up

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote says tests pass and the warning is correct, then asks where to configure suppression. It supports question rather than malfunction; the clipped ending does not remove the question.

Human review: pending.

## candidate / warning-question

[Actual report](run/candidate-warning-question-report.json) · fingerprint `a3a9b625e4af1181413685c8cc34feba06ab1d570f45f2db1779a37d0023ade8`

Selected type: `type: question`

Selected quote:

> All my tests pass, and the warning correctly describes a deprecated option I still use. Where can I configure pytest to hide this warning temporarily while I up

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The quote says tests pass and the warning is correct, then asks where to configure suppression. It supports question rather than malfunction; the clipped ending does not remove the question.

Human review: pending.

## control / uncertain

[Actual report](run/control-uncertain-report.json) · fingerprint `2b3363d9f8c0026e8b7c842539e1e6d4b9d518d03fcb7393737ee64636602f23`

Selected type: `None`

Selected quote:

*Abstained; no selected quote.*

Whole-input type support: **N/A**. Selected-quote relevance: **N/A**. Abstention appropriate: **yes**.

The incomplete note establishes neither failure nor a request for help or change. Both type fields abstain appropriately.

Human review: pending.

## candidate / uncertain

[Actual report](run/candidate-uncertain-report.json) · fingerprint `85ec7c0d1fe54dce21f933dd5d4504725182468b943c49b52f4bbba5756e2f5b`

Selected type: `None`

Selected quote:

*Abstained; no selected quote.*

Whole-input type support: **N/A**. Selected-quote relevance: **N/A**. Abstention appropriate: **yes**.

The incomplete note establishes neither failure nor a request for help or change. Both type fields abstain appropriately.

Human review: pending.

## control / h-12219

[Actual report](run/control-h-12219-report.json) · fingerprint `1ca4968e832b1af1aa07996fe9db937014f3da33cec376bcd4db64bb76df21e3`

Selected type: `type: regression`

Selected quote:

> ts.tarfile). When I run the tests, the setUpModule is never called.

Whole-input type support: **uncertain**. Selected-quote relevance: **no**. Abstention appropriate: **N/A**.

The frozen opening reports a hook malfunction, cites older feature support and shows a working minimized current-version example. It does not demonstrate that the same affected project worked before a version change. Regression remains plausible but uncertain. Neither actual selected span establishes a working-to-broken comparison, so the quote does not support regression.

Human review: pending.

## candidate / h-12219

[Actual report](run/candidate-h-12219-report.json) · fingerprint `290f7e513d63cd02c03179fe230d3ff5a877faf061a673af0fa42c76d2ccaf1f`

Selected type: `type: regression`

Selected quote:

> However, with pytest 8.x, I'm finding that it's not supported, even though the [docs say it is](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73

Whole-input type support: **uncertain**. Selected-quote relevance: **no**. Abstention appropriate: **N/A**.

The frozen opening reports a hook malfunction, cites older feature support and shows a working minimized current-version example. It does not demonstrate that the same affected project worked before a version change. Regression remains plausible but uncertain. Neither actual selected span establishes a working-to-broken comparison, so the quote does not support regression.

Human review: pending.

## control / h-12223

[Actual report](run/control-h-12223-report.json) · fingerprint `acfaf6d01afcc37172de2c322b104c69e4f229f19bddc755640acc7ab6c58b84`

Selected type: `type: enhancement`

Selected quote:

> for parsers, and projects like BeautifulSoup and lxml will fail to parse this correctly (truncating or crashing, respectively).

Whole-input type support: **yes**. Selected-quote relevance: **uncertain**. Abstention appropriate: **N/A**.

The full frozen opening supports enhancement as requested output-size control and bug as consumer interoperability failure. Preserve that ambiguity and the original bug expectation. The selected quote describes parser failure without the requested control, leaving enhancement quote relevance uncertain; the sampler omits the explicit request.

Human review: pending.

## candidate / h-12223

[Actual report](run/candidate-h-12223-report.json) · fingerprint `910f41061877d5c14ab7a1ad18990218c533e595e239546c07c0b0cc5d144b62`

Selected type: `type: enhancement`

Selected quote:

> for parsers, and projects like BeautifulSoup and lxml will fail to parse this correctly (truncating or crashing, respectively).

Whole-input type support: **yes**. Selected-quote relevance: **uncertain**. Abstention appropriate: **N/A**.

The full frozen opening supports enhancement as requested output-size control and bug as consumer interoperability failure. Preserve that ambiguity and the original bug expectation. The selected quote describes parser failure without the requested control, leaving enhancement quote relevance uncertain; the sampler omits the explicit request.

Human review: pending.

## control / h-12249

[Actual report](run/control-h-12249-report.json) · fingerprint `d56455b287589a595e0617bd205e851a646803f31aacdfd2b8b5a44a46750e41`

Selected type: `type: enhancement`

Selected quote:

> ctions, then they get raised early and cannot be controlled by the pytest `filterwarnings` config, which is unfortunate. There should be a good way to suppress

Whole-input type support: **yes**. Selected-quote relevance: **yes**. Abstention appropriate: **N/A**.

The full frozen opening requests extending normal filtering to early import/rewrite. Enhancement is a defensible alternative to the unchanged bug expectation. The control quote includes inability to control warnings and the request to suppress them, supporting the type.

Human review: pending.

## candidate / h-12249

[Actual report](run/candidate-h-12249-report.json) · fingerprint `d22359cfd910a7060bdd89c85c4b6a13d102573b6bca4584f67dddba10f77bf5`

Selected type: `type: enhancement`

Selected quote:

> these with normal pytest config options.

Whole-input type support: **yes**. Selected-quote relevance: **no**. Abstention appropriate: **N/A**.

Enhancement remains defensible from the full request to extend filtering. The newly selected fragment, "these with normal pytest config options.", has neither the warnings referent nor the suppression request or limitation. It does not express the requested extension; the control selected a supporting available chunk. This is a selected-quote support loss, not a changed benchmark annotation.

Human review: pending.

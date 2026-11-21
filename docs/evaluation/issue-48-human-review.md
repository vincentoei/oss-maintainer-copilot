# Issue #48: twenty-reply human review

The requesting user explicitly reviewed all twenty final After replies: **3 useful, 7 partly useful, 10 not useful**; none unsure. Ratings improved for five cases, stayed unchanged for fifteen, and regressed for none. Rubric: Does the reply ask for needed details and explain relevant evidence without misleading claims?

Before ratings belong only to #45. Final #48 usefulness ratings and verbatim reasons below are confirmed by the requesting user. Separate citation support, relationship labels and other-field abstention judgments remain pending; usefulness reasons do not automatically confirm those judgments. These development-informed cases provide regression evidence, not independent generalization evidence.

## #7312

[Opening](https://github.com/pytest-dev/pytest/issues/7312); cutoff `2020-06-03T14:20:24+00:00`; pinned commit `61a6ac97054c0bd6f812642b46847c4b7cbede2a`.

Before: **partly useful** — #349 is a promising lead because it also requests fixture-derived parameter values, but the draft obscures that connection with generic word overlap. It should explain the potential duplicate relationship and distinguish #2959’s regression from this enhancement request. #7012 appears unrelated and adds noise. The draft neither acknowledges the requested behavior nor offers a clear next step for the maintainer.

> Thanks for sharing this issue.
> - Earlier issue #349 may be relevant: Shared topic: case, currently, def; one report negates a shared condition. [C1]
> - Earlier issue #2959 may be relevant: Shared topic: case, config, def; the same failure or request is not established. [C2]
> - Earlier issue #7012 may be relevant: Shared topic: def, session, single; the same failure or request is not established. [C3]

Report status: complete; type: type: enhancement.
Missing details: none

- Relationship #349: Shared topic: case, currently, def; one report negates a shared condition.
- Relationship #2959: Shared topic: case, config, def; the same failure or request is not established.
- Relationship #7012: Shared topic: def, session, single; the same failure or request is not established.
- [C1: pytest issue #349: Using fixtures in pytest.mark.parametrize](https://github.com/pytest-dev/pytest/issues/349)
- [C2: pytest issue #2959: pytest 3.3.0 immutable fixture params](https://github.com/pytest-dev/pytest/issues/2959)
- [C3: pytest issue #7012: Quotation marks in pytest command collects duplicate tests](https://github.com/pytest-dev/pytest/issues/7012)

After (real response received: True):

> Thanks for sharing this issue.
> - Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Report status: complete; type: type: enhancement.
Missing details: none

- Relationship #349: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values.
- [C1: pytest issue #349: Using fixtures in pytest.mark.parametrize](https://github.com/pytest-dev/pytest/issues/349)

New usefulness rating: **partly useful**. Reason: Explains the shared fixture-derived parametrization request and the differing examples. It provides a relevant lead, but stops short of explaining the potential duplicate relationship or a concrete next step.

Rating category versus #45: **unchanged**.

## #10156

[Opening](https://github.com/pytest-dev/pytest/issues/10156); cutoff `2022-07-19T20:03:50+00:00`; pinned commit `34a285986e456406b22b62aa563a64331f640e7f`.

Before: **not useful** — The draft does not address whether the documentation contribution is welcome, whether the workaround is understood correctly, or where the example belongs. It repeats #2959, which the reporter already cited, without explaining its connection to their implementation. Generic word overlap offers little help in assessing or responding to the proposal.

> Thanks for sharing this issue.
> - Earlier issue #7312 may be relevant: Shared topic: case, config, def; the same failure or request is not established. [C1]
> - Earlier issue #349 may be relevant: Shared topic: arg, but, case; one report negates a shared condition. [C2]
> - Earlier issue #2959 may be relevant: Shared topic: case, com, config; the same failure or request is not established. [C3]

Report status: complete; type: type: question.
Missing details: none

- Relationship #7312: Shared topic: case, config, def; the same failure or request is not established.
- Relationship #349: Shared topic: arg, but, case; one report negates a shared condition.
- Relationship #2959: Shared topic: case, com, config; the same failure or request is not established.
- [C1: pytest issue #7312: Feature Request - Support using session scope-fixtures when using pytest.mark.parametrize ](https://github.com/pytest-dev/pytest/issues/7312)
- [C2: pytest issue #349: Using fixtures in pytest.mark.parametrize](https://github.com/pytest-dev/pytest/issues/349)
- [C3: pytest issue #2959: pytest 3.3.0 immutable fixture params](https://github.com/pytest-dev/pytest/issues/2959)

After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: type: question.
Missing details: none


New usefulness rating: **not useful**. Reason: The generic abstention does not address the documentation proposal, assess the workaround, or help determine where the example belongs.

Rating category versus #45: **unchanged**.

## #12053

[Opening](https://github.com/pytest-dev/pytest/issues/12053); cutoff `2024-03-03T14:58:35+00:00`; pinned commit `00043f7f1047b29fdaeb18e169fe9d6146988cb8`.

Before: **not useful** — The draft does not address storing the debugger class in configuration or suggest a next step. #8655 provides debugger-option context, but the draft never explains that connection. The fixture-parametrization issues add noise, and generic word overlap does not help a maintainer assess the requested enhancement.

> Thanks for sharing this issue.
> - Earlier issue #8655 may be relevant: Shared topic: bit, currently, debugger; one report negates a shared condition. [C1]
> - Earlier issue #7312 may be relevant: Shared topic: case, configuration, currently; the same failure or request is not established. [C2]
> - Earlier issue #10156 may be relevant: Shared topic: case, https, like; one report negates a shared condition. [C3]

Report status: complete; type: type: enhancement.
Missing details: none

- Relationship #8655: Shared topic: bit, currently, debugger; one report negates a shared condition.
- Relationship #7312: Shared topic: case, configuration, currently; the same failure or request is not established.
- Relationship #10156: Shared topic: case, https, like; one report negates a shared condition.
- [C1: pytest issue #8655: Help text is misleading about the behavior of --pdb](https://github.com/pytest-dev/pytest/issues/8655)
- [C2: pytest issue #7312: Feature Request - Support using session scope-fixtures when using pytest.mark.parametrize ](https://github.com/pytest-dev/pytest/issues/7312)
- [C3: pytest issue #10156: Document how to build dynamic session-scoped fixtures](https://github.com/pytest-dev/pytest/issues/10156)

After (real response received: True):

> Thanks for sharing this issue.
> - Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Report status: complete; type: type: enhancement.
Missing details: none

- Relationship #8655: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help.
- [C1: pytest issue #8655: Help text is misleading about the behavior of --pdb](https://github.com/pytest-dev/pytest/issues/8655)

New usefulness rating: **partly useful**. Reason: Clearly distinguishes the configuration request from #8655’s command-line help issue. That context is relevant, but it provides no guidance on configuring the debugger class or assessing the enhancement.

Rating category versus #45: **improved**.

## #12072

[Opening](https://github.com/pytest-dev/pytest/issues/12072); cutoff `2024-03-04T13:04:55+00:00`; pinned commit `0951cbc6e4880ee7dfc9b7e56948d83ee086e74b`.

Before: **partly useful** — Linking #12066 gives the maintainer a strong lead, but the draft understates the match: both report flaky failing to import call_runtest_hook with pytest 8.1, supporting a duplicate candidate. It offers no explanation or next step and does not request the missing environment details or reproducer.

> Thanks for sharing this issue.
> - Earlier issue #12066 may be relevant: Shared topic: assertion, bootstrap, call_runtest_hook; the same failure or request is not established. [C1]

Report status: complete; type: type: bug.
Missing details: none

- Relationship #12066: Shared topic: assertion, bootstrap, call_runtest_hook; the same failure or request is not established.
- [C1: pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'](https://github.com/pytest-dev/pytest/issues/12066)

After (real response received: True):

> Thanks for sharing this issue.
> - Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Report status: complete; type: type: bug.
Missing details: none

- Relationship #12066: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established.
- [C1: pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'](https://github.com/pytest-dev/pytest/issues/12066)

New usefulness rating: **partly useful**. Reason: Identifies and quotes the matching import error, giving a strong investigative lead. The unexplained statement that the same failure is not established understates the match; missing environment details and a reproducer are not requested.

Rating category versus #45: **unchanged**.

## #12079

[Opening](https://github.com/pytest-dev/pytest/issues/12079); cutoff `2024-03-05T12:31:13+00:00`; pinned commit `03e54712dd123138aa4c1035a027e17d0dd9a86c`.

Before: **partly useful** — Asking about attempted alternatives is appropriate because that section is empty. Asking for a real-world use case overlooks the stated goal of investigating dependencies between tests. The draft also omits #11871, a strong potential duplicate that would help the maintainer assess the request.

> Thanks for sharing this issue.
> - Could you add a real-world use case this would enable? [C1]
> - Could you add any workaround or alternative you have tried, or that there is none? [C2]

Report status: complete; type: type: enhancement.
Missing details: real-world use case, alternative solutions

- Relationship #11871: Shared topic: additional, all, alternative; the same failure or request is not established.
- Relationship #10156: Shared topic: here, like, only; the same failure or request is not established.
- [C1: pytest feature report template: real-world use case](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L19)
- [C2: pytest feature report template: alternative solutions](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21)
- [C3: pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument](https://github.com/pytest-dev/pytest/issues/11871)
- [C4: pytest issue #10156: Document how to build dynamic session-scoped fixtures](https://github.com/pytest-dev/pytest/issues/10156)

After (real response received: True):

> Thanks for sharing this issue.
> - Could you add any workaround or alternative you have tried, or that there is none? [C1]

Report status: complete; type: type: enhancement.
Missing details: alternative solutions

- Relationship #11871: Both concern reading test-selection arguments from a file. This report: "… file, and run selected subsets of it using `pytest`"; earlier: "…irs`, to compliment the positional `file_or_dir` argument.". the same failure or request is not established.
- [C1: pytest feature report template: alternative solutions](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21)
- [C2: pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument](https://github.com/pytest-dev/pytest/issues/11871)

New usefulness rating: **partly useful**. Reason: Appropriately asks about attempted alternatives without repeating the supplied use case. However, the final reply omits #11871 and its closely matching request to read test-selection arguments from a file.

Rating category versus #45: **unchanged**.

## #12081

[Opening](https://github.com/pytest-dev/pytest/issues/12081); cutoff `2024-03-06T00:03:25+00:00`; pinned commit `03e54712dd123138aa4c1035a027e17d0dd9a86c`.

Before: **not useful** — The draft repeats #3448, which the reporter already linked, without explaining the matching behavior or potential duplicate relationship. The documentation statement is too general, and the source citation never states that readouterr() resets the buffer. It does not address retaining output, the proposed API change, or documentation improvements.

> Thanks for sharing this issue.
> - Earlier issue #3448 may be relevant: Shared topic: assert, assertionerror, call; one report negates a shared condition. [C1]
> - pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C2]
> - At commit 03e54712dd123138aa4c1035a027e17d0dd9a86c, pytest source src/_pytest/capture.py:935 contains the cited line. [C3]

Report status: complete; type: type: enhancement.
Missing details: none

- Relationship #3448: Shared topic: assert, assertionerror, call; one report negates a shared condition.
- [C1: pytest issue #3448: capture: keep all output for "Captured stdout call" etc](https://github.com/pytest-dev/pytest/issues/3448)
- [C2: pytest documentation: capture](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110)
  Evidence: The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is
- [C3: pytest source: src/_pytest/capture.py:935](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/src/_pytest/capture.py#L935)
  Evidence:         """Read and return the captured output so far, resetting the internal

After (real response received: True):

> Thanks for sharing this issue.
> - Earlier issue #3448 may be relevant: Both concern readouterr consuming captured output. This report: "…turing via readouterr() consume stdout, meaning that logs are no longer available in the "Captured s…"; earlier: "…uterr()` in a test also resets what pytest displays in case of failed tests.". This opening names copyouterr; compare its proposed behavior with the earlier readouterr report. [C1]
> - pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C2]
> - At commit 03e54712dd123138aa4c1035a027e17d0dd9a86c, pytest source src/_pytest/capture.py:935 contains the cited line. [C3]

Report status: complete; type: type: enhancement.
Missing details: none

- Relationship #3448: Both concern readouterr consuming captured output. This report: "…turing via readouterr() consume stdout, meaning that logs are no longer available in the "Captured s…"; earlier: "…uterr()` in a test also resets what pytest displays in case of failed tests.". This opening names copyouterr; compare its proposed behavior with the earlier readouterr report.
- [C1: pytest issue #3448: capture: keep all output for "Captured stdout call" etc](https://github.com/pytest-dev/pytest/issues/3448)
- [C2: pytest documentation: capture](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110)
  Evidence: The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is
- [C3: pytest source: src/_pytest/capture.py:935](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/src/_pytest/capture.py#L935)
  Evidence:         """Read and return the captured output so far, resetting the internal

New usefulness rating: **partly useful**. Reason: Explains the shared output-consumption behavior and suggests comparing the proposed API with #3448. The documentation statement remains generic, and the source reference still fails to explain that readouterr() resets the buffer.

Rating category versus #45: **improved**.

## #12083

[Opening](https://github.com/pytest-dev/pytest/issues/12083); cutoff `2024-03-06T10:53:11+00:00`; pinned commit `03e54712dd123138aa4c1035a027e17d0dd9a86c`.

Before: **not useful** — The draft does not acknowledge the demonstrated collection regression or the reporter’s question about intended behavior. Its vague abstention gives the maintainer no explanation, targeted follow-up, or next step despite the concrete reproduction details supplied.

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: type: bug.
Missing details: none


After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: type: bug.
Missing details: none


New usefulness rating: **not useful**. Reason: The abstention provides no help investigating the demonstrated collection difference or clarifying whether the behavior is intentional.

Rating category versus #45: **unchanged**.

## #12116

[Opening](https://github.com/pytest-dev/pytest/issues/12116); cutoff `2024-03-13T13:37:51+00:00`; pinned commit `c0532dda18a5cfd0e6f67113bb164485fa80eb86`.

Before: **not useful** — The draft requests package information already supplied in the opening. It does not address the missing child-process log records, the provided reproducer and workaround, or the request for guidance on contributing multiprocessing support.

> Thanks for sharing this issue.
> - Could you add the output of `pip list` from the virtual environment you are using? [C1]

Report status: complete; type: type: bug.
Missing details: pip list output

- Relationship #12081: Shared topic: assert, capturing, code; one report negates a shared condition.
- [C1: pytest bug report template: pip list output](https://github.com/pytest-dev/pytest/blob/c0532dda18a5cfd0e6f67113bb164485fa80eb86/.github/ISSUE_TEMPLATE/1_bug_report.md#L14)
- [C2: pytest issue #12081: Capture: copy output when using readouterr() instead of consuming it](https://github.com/pytest-dev/pytest/issues/12081)

After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: type: bug.
Missing details: none


New usefulness rating: **not useful**. Reason: Avoids requesting the already supplied package list, but gives no guidance about child-process logging, the reproducer, or the proposed multiprocessing support.

Rating category versus #45: **unchanged**.

## #12146

[Opening](https://github.com/pytest-dev/pytest/issues/12146); cutoff `2024-03-21T12:06:34+00:00`; pinned commit `470edc5884faf7ae9e5297f233a4909d4579fbdb`.

Before: **not useful** — The draft gives no targeted help despite the supplied examples. It should ask the reporter to compare both scenarios using the same pytest version and identical tuple values, so the apparent fixture-scope change can be investigated without those confounding differences.

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: None.
Missing details: none


After (real response received: True):

> Thanks for sharing this issue.
> - The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Report status: complete; type: None.
Missing details: none

- [C1: Submitted issue under review: investigative follow-up](https://github.com/pytest-dev/pytest/issues/12146)
  Evidence: pytest-8.1.1 / pytest-7.4.4 / pytest         8.1.1

New usefulness rating: **useful**. Reason: Identifies the version mismatch and requests a controlled comparison with identical tuple values and order. Asking for setup/teardown output provides a concrete way to isolate the reported behavior without assuming its cause.

Rating category versus #45: **improved**.

## #12189

[Opening](https://github.com/pytest-dev/pytest/issues/12189); cutoff `2024-04-05T09:14:51+00:00`; pinned commit `4e3dd21506a9e543c04c63ebff966a9b604d2b9e`.

Before: **not useful** — The draft does not examine the key interaction between -s, output capture and JUnit logging, or suggest a targeted check. The readouterr() reports concern a different capture scenario, while the other links add unrelated noise. Generic word overlap does not help answer the reporter’s configuration question.

> Thanks for sharing this issue.
> - Earlier issue #12081 may be relevant: Shared topic: any, but, captured; one report negates a shared condition. [C1]
> - Earlier issue #3448 may be relevant: Shared topic: captured, def, err; one report negates a shared condition. [C2]
> - Earlier issue #11871 may be relevant: Shared topic: all, but, command; the same failure or request is not established. [C3]
> - Earlier issue #12066 may be relevant: Shared topic: command, config, environment; one report negates a shared condition. [C4]
> - Earlier issue #12146 may be relevant: Shared topic: conftest, def, import; one report negates a shared condition. [C5]

Report status: complete; type: type: bug.
Missing details: none

- Relationship #12081: Shared topic: any, but, captured; one report negates a shared condition.
- Relationship #3448: Shared topic: captured, def, err; one report negates a shared condition.
- Relationship #11871: Shared topic: all, but, command; the same failure or request is not established.
- Relationship #12066: Shared topic: command, config, environment; one report negates a shared condition.
- Relationship #12146: Shared topic: conftest, def, import; one report negates a shared condition.
- [C1: pytest issue #12081: Capture: copy output when using readouterr() instead of consuming it](https://github.com/pytest-dev/pytest/issues/12081)
- [C2: pytest issue #3448: capture: keep all output for "Captured stdout call" etc](https://github.com/pytest-dev/pytest/issues/3448)
- [C3: pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument](https://github.com/pytest-dev/pytest/issues/11871)
- [C4: pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'](https://github.com/pytest-dev/pytest/issues/12066)
- [C5: pytest issue #12146: Parametrization with Variables Unexpectedly Changes Fixture Scope from Class-Level to Function-Level](https://github.com/pytest-dev/pytest/issues/12146)

After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: type: bug.
Missing details: none


New usefulness rating: **not useful**. Reason: The abstention does not examine the supplied command or suggest investigating how -s, capture and JUnit output interact.

Rating category versus #45: **unchanged**.

## #12197

[Opening](https://github.com/pytest-dev/pytest/issues/12197); cutoff `2024-04-08T11:30:37+00:00`; pinned commit `74f05648d5ea9e69d75f27a77972756ee32f6730`.

Before: **not useful** — The draft does not address whether log_disable is a supported ini setting or request the actual configuration and a reproducing test. #12053 shares a configuration theme, but the draft explains no actionable connection. The remaining links and generic word overlap add noise without helping investigate the behavior.

> Thanks for sharing this issue.
> - Earlier issue #12053 may be relevant: Shared topic: configuration, ini, option; one report negates a shared condition. [C1]
> - Earlier issue #12189 may be relevant: Shared topic: any, log, one; the same failure or request is not established. [C2]
> - Earlier issue #7312 may be relevant: Shared topic: being, one; the same failure or request is not established. [C3]
> - Earlier issue #12066 may be relevant: Shared topic: disable, possible; the same failure or request is not established. [C4]

Report status: complete; type: None.
Missing details: none

- Relationship #12053: Shared topic: configuration, ini, option; one report negates a shared condition.
- Relationship #12189: Shared topic: any, log, one; the same failure or request is not established.
- Relationship #7312: Shared topic: being, one; the same failure or request is not established.
- Relationship #12066: Shared topic: disable, possible; the same failure or request is not established.
- [C1: pytest issue #12053: pdbcls as a configuration option?](https://github.com/pytest-dev/pytest/issues/12053)
- [C2: pytest issue #12189: No output written to JUnit XML files](https://github.com/pytest-dev/pytest/issues/12189)
- [C3: pytest issue #7312: Feature Request - Support using session scope-fixtures when using pytest.mark.parametrize ](https://github.com/pytest-dev/pytest/issues/7312)
- [C4: pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'](https://github.com/pytest-dev/pytest/issues/12066)

After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: None.
Missing details: none


New usefulness rating: **not useful**. Reason: Provides no investigation of the CLI-versus-ini behavior and does not request the missing configuration snippet or reproducing test.

Rating category versus #45: **unchanged**.

## #12201

[Opening](https://github.com/pytest-dev/pytest/issues/12201); cutoff `2024-04-09T14:22:08+00:00`; pinned commit `17fc20af78d0c7b739806c4e461d2c9b8c30ceeb`.

Before: **not useful** — Both requests ask for information already supplied: testing Windows/POSIX paths is the use case, and duplicated tests with skipif are the current workaround. The draft overlooks that content and offers no guidance on the proposed conditional parametrization.

> Thanks for sharing this issue.
> - Could you add a real-world use case this would enable? [C1]
> - Could you add any workaround or alternative you have tried, or that there is none? [C2]

Report status: complete; type: type: enhancement.
Missing details: real-world use case, alternative solutions

- Relationship #12146: Shared topic: def, list, mark; the same failure or request is not established.
- [C1: pytest feature report template: real-world use case](https://github.com/pytest-dev/pytest/blob/17fc20af78d0c7b739806c4e461d2c9b8c30ceeb/.github/ISSUE_TEMPLATE/2_feature_request.md#L19)
- [C2: pytest feature report template: alternative solutions](https://github.com/pytest-dev/pytest/blob/17fc20af78d0c7b739806c4e461d2c9b8c30ceeb/.github/ISSUE_TEMPLATE/2_feature_request.md#L21)
- [C3: pytest issue #12146: Parametrization with Variables Unexpectedly Changes Fixture Scope from Class-Level to Function-Level](https://github.com/pytest-dev/pytest/issues/12146)

After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: type: enhancement.
Missing details: none


New usefulness rating: **not useful**. Reason: Removes the redundant information requests, but the resulting abstention offers no help assessing platform-dependent parameter values or the existing duplication-and-skipif workaround.

Rating category versus #45: **unchanged**.

## #12203

[Opening](https://github.com/pytest-dev/pytest/issues/12203); cutoff `2024-04-10T09:18:43+00:00`; pinned commit `1f001cd1051a4ca4bef251d93e472e625578aaf7`.

Before: **partly useful** — A standalone minimal example is missing, so the request could help reproduce the logging failure. It would be more actionable if it acknowledged the supplied sketch and asked for a runnable fixture and test showing the logging configuration, exception and missing output.

> Thanks for sharing this issue.
> - Could you add a minimal example, if possible? [C1]

Report status: complete; type: type: bug.
Missing details: minimal example

- Relationship #12081: Shared topic: actual, but, capture; one report negates a shared condition.
- Relationship #3448: Shared topic: capture, def, failed; one report negates a shared condition.
- Relationship #12066: Shared topic: description, detailed, environment; one report negates a shared condition.
- [C1: pytest bug report template: minimal example](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16)
- [C2: pytest issue #12081: Capture: copy output when using readouterr() instead of consuming it](https://github.com/pytest-dev/pytest/issues/12081)
- [C3: pytest issue #3448: capture: keep all output for "Captured stdout call" etc](https://github.com/pytest-dev/pytest/issues/3448)
- [C4: pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'](https://github.com/pytest-dev/pytest/issues/12066)

After (real response received: True):

> Thanks for sharing this issue.
> - Could you add a minimal example, if possible? [C1]

Report status: complete; type: type: bug.
Missing details: minimal example

- [C1: pytest bug report template: minimal example](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16)

New usefulness rating: **partly useful**. Reason: Correctly requests a missing minimal example. It should acknowledge the existing sketch and specify that a runnable fixture/test with logging configuration and the exception path is needed.

Rating category versus #45: **unchanged**.

## #12204

[Opening](https://github.com/pytest-dev/pytest/issues/12204); cutoff `2024-04-10T10:45:32+00:00`; pinned commit `1f001cd1051a4ca4bef251d93e472e625578aaf7`.

Before: **not useful** — Neither cited issue explains the growing exception tracebacks, and generic word overlap gives no useful investigative lead. The draft ignores the supplied reproducer and misses a targeted clarification: which pytest/pluggy versions produced the output, given the conflicting package list and session header.

> Thanks for sharing this issue.
> - Earlier issue #12066 may be relevant: Shared topic: args, attr, call; one report negates a shared condition. [C1]
> - Earlier issue #12116 may be relevant: Shared topic: code, def, example; one report negates a shared condition. [C2]

Report status: complete; type: type: bug.
Missing details: none

- Relationship #12066: Shared topic: args, attr, call; one report negates a shared condition.
- Relationship #12116: Shared topic: code, def, example; one report negates a shared condition.
- [C1: pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'](https://github.com/pytest-dev/pytest/issues/12066)
- [C2: pytest issue #12116: Capturing logs does not work with multiprocessing](https://github.com/pytest-dev/pytest/issues/12116)

After (real response received: True):

> Thanks for sharing this issue.
> - The opening contains conflicting version evidence (pytest: 8.1.1 / 8.0.0; pluggy: 1.4.0 / 1.3.0). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C1]

Report status: complete; type: type: bug.
Missing details: none

- [C1: Submitted issue under review: investigative follow-up](https://github.com/pytest-dev/pytest/issues/12204)
  Evidence: pytest    8.1.1 / pytest-8.0.0 / pluggy    1.4.0 / pluggy-1.3.0

New usefulness rating: **useful**. Reason: Accurately identifies the conflicting pytest and pluggy versions and asks which environment produced the output. This is a focused clarification that helps reproduce the traceback growth without inventing a diagnosis.

Rating category versus #45: **improved**.

## #12216

[Opening](https://github.com/pytest-dev/pytest/issues/12216); cutoff `2024-04-15T07:38:50+00:00`; pinned commit `5f6e825a2687f6bb8bc437e67a59c0a92fb16c06`.

Before: **not useful** — The fallback does not acknowledge the collection error or the fixture body failing to execute. It offers no guidance, targeted clarification or next step despite the supplied reproducer, so it gives the maintainer no help responding to the fixture-injection question.

> Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Report status: partial; type: None.
Missing details: none

- Relationship #12146: Shared topic: def, fixture, fixturenames; one report negates a shared condition.
- Relationship #7312: Shared topic: case, def, fixture; the same failure or request is not established.
- [C1: pytest issue #12146: Parametrization with Variables Unexpectedly Changes Fixture Scope from Class-Level to Function-Level](https://github.com/pytest-dev/pytest/issues/12146)
- [C2: pytest issue #7312: Feature Request - Support using session scope-fixtures when using pytest.mark.parametrize ](https://github.com/pytest-dev/pytest/issues/7312)

After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Report status: partial; type: None.
Missing details: none


New usefulness rating: **not useful**. Reason: The fallback offers no guidance or targeted follow-up about the collection error and unexecuted fixture body despite the supplied reproducer.

Rating category versus #45: **unchanged**.

## #12219

[Opening](https://github.com/pytest-dev/pytest/issues/12219); cutoff `2024-04-16T08:22:38+00:00`; pinned commit `58844247f7ae4a7a213a73c8af2462253b3d8fc7`.

Before: **not useful** — The draft repeats #4064, which the reporter already cited, without explaining its relevance. It misses the key discrepancy between the working example and the affected project and should request a minimized failing example to help identify what prevents the hooks from running.

> Thanks for sharing this issue.
> - Earlier issue #4064 may be relevant: Shared topic: blob, but, com; one report negates a shared condition. [C1]

Report status: complete; type: type: docs.
Missing details: none

- Relationship #4064: Shared topic: blob, but, com; one report negates a shared condition.
- Relationship #12216: Shared topic: add, but, com; one report negates a shared condition.
- [C1: pytest issue #4064: Docs: is setUpModule/tearDownModule supported?](https://github.com/pytest-dev/pytest/issues/4064)
- [C2: pytest issue #12216: Adding parameterized fixture in pytest_generate_test is not executing the fixture's code, even if it is marked as "indirect"](https://github.com/pytest-dev/pytest/issues/12216)

After (real response received: True):

> Thanks for sharing this issue.
> - You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Report status: complete; type: type: docs.
Missing details: none

- Relationship #4064: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation.
- [C1: pytest issue #4064: Docs: is setUpModule/tearDownModule supported?](https://github.com/pytest-dev/pytest/issues/4064)
- [C2: Submitted issue under review: investigative follow-up](https://github.com/pytest-dev/pytest/issues/12219)
  Evidence: Interestingly, the hook does seem to be honored in a minimized example.

New usefulness rating: **useful**. Reason: Acknowledges that the small example works and requests a minimized failing case with layout, configuration and command. Comparing the two gives a concrete investigative next step without asserting a cause.

Rating category versus #45: **improved**.

## #12223

[Opening](https://github.com/pytest-dev/pytest/issues/12223); cutoff `2024-04-17T09:00:30+00:00`; pinned commit `58844247f7ae4a7a213a73c8af2462253b3d8fc7`.

Before: **not useful** — The draft does not address shortening the message attribute while preserving the detailed failure body. #12189 concerns a different JUnit XML symptom, and the other links offer no clear investigative lead. Generic word overlap does not help assess the reported tool failures or requested change.

> Thanks for sharing this issue.
> - Earlier issue #12189 may be relevant: Shared topic: anything, but, classname; one report negates a shared condition. [C1]
> - Earlier issue #12081 may be relevant: Shared topic: assert, assertionerror, both; the same failure or request is not established. [C2]
> - Earlier issue #3448 may be relevant: Shared topic: assert, assertionerror, def; the same failure or request is not established. [C3]
> - Earlier issue #12116 may be relevant: Shared topic: assert, correctly, def; one report negates a shared condition. [C4]
> - Earlier issue #12079 may be relevant: Shared topic: file, like, only; the same failure or request is not established. [C5]

Report status: complete; type: type: bug.
Missing details: none

- Relationship #12189: Shared topic: anything, but, classname; one report negates a shared condition.
- Relationship #12081: Shared topic: assert, assertionerror, both; the same failure or request is not established.
- Relationship #3448: Shared topic: assert, assertionerror, def; the same failure or request is not established.
- Relationship #12116: Shared topic: assert, correctly, def; one report negates a shared condition.
- Relationship #12079: Shared topic: file, like, only; the same failure or request is not established.
- [C1: pytest issue #12189: No output written to JUnit XML files](https://github.com/pytest-dev/pytest/issues/12189)
- [C2: pytest issue #12081: Capture: copy output when using readouterr() instead of consuming it](https://github.com/pytest-dev/pytest/issues/12081)
- [C3: pytest issue #3448: capture: keep all output for "Captured stdout call" etc](https://github.com/pytest-dev/pytest/issues/3448)
- [C4: pytest issue #12116: Capturing logs does not work with multiprocessing](https://github.com/pytest-dev/pytest/issues/12116)
- [C5: pytest issue #12079: Read tests to be executed from a file instead of from positional arguments](https://github.com/pytest-dev/pytest/issues/12079)

After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: type: bug.
Missing details: none


New usefulness rating: **not useful**. Reason: The abstention does not address the oversized message attribute, downstream tool failures, or the request to preserve the detailed failure body.

Rating category versus #45: **unchanged**.

## #12224

[Opening](https://github.com/pytest-dev/pytest/issues/12224); cutoff `2024-04-18T05:51:07+00:00`; pinned commit `58844247f7ae4a7a213a73c8af2462253b3d8fc7`.

Before: **not useful** — #11871 concerns supplying test-selection arguments, not controlling a session across individual test runs. The draft does not address the proposed API, repeated fixture initialization, or the costly Pyodide workaround, so it offers no useful basis for assessing the enhancement.

> Thanks for sharing this issue.
> - Earlier issue #11871 may be relevant: Shared topic: additional, alternative, but; one report negates a shared condition. [C1]

Report status: complete; type: type: enhancement.
Missing details: none

- Relationship #11871: Shared topic: additional, alternative, but; one report negates a shared condition.
- [C1: pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument](https://github.com/pytest-dev/pytest/issues/11871)

After (real response received: True):

> Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Report status: complete; type: type: enhancement.
Missing details: none


New usefulness rating: **not useful**. Reason: Gives no help assessing the requested session-control API, repeated fixture initialization, or costly Pyodide workaround.

Rating category versus #45: **unchanged**.

## #12226

[Opening](https://github.com/pytest-dev/pytest/issues/12226); cutoff `2024-04-19T11:34:17+00:00`; pinned commit `ad95d59d6158076768cccd0000b968cd691cb62a`.

Before: **partly useful** — Asking about attempted alternatives could help because none are described. Asking for a use case overlooks the stated difficulty quoting marker expressions in Bash-based CI scripts. A more useful follow-up would ask for a concrete failing command and why existing quoting approaches are unsuitable.

> Thanks for sharing this issue.
> - Could you add a real-world use case this would enable? [C1]
> - Could you add any workaround or alternative you have tried, or that there is none? [C2]

Report status: complete; type: type: enhancement.
Missing details: real-world use case, alternative solutions

- Relationship #12224: Shared topic: additional, alternative, context; one report negates a shared condition.
- Relationship #7312: Shared topic: like, problem, solve; the same failure or request is not established.
- Relationship #349: Shared topic: like, syntax, what; the same failure or request is not established.
- [C1: pytest feature report template: real-world use case](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L19)
- [C2: pytest feature report template: alternative solutions](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21)
- [C3: pytest issue #12224: More granular scripting interface](https://github.com/pytest-dev/pytest/issues/12224)
- [C4: pytest issue #7312: Feature Request - Support using session scope-fixtures when using pytest.mark.parametrize ](https://github.com/pytest-dev/pytest/issues/7312)
- [C5: pytest issue #349: Using fixtures in pytest.mark.parametrize](https://github.com/pytest-dev/pytest/issues/349)

After (real response received: True):

> Thanks for sharing this issue.
> - Could you add any workaround or alternative you have tried, or that there is none? [C1]

Report status: complete; type: type: enhancement.
Missing details: alternative solutions

- [C1: pytest feature report template: alternative solutions](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21)

New usefulness rating: **partly useful**. Reason: Asking about attempted alternatives is appropriate and no longer repeats the supplied use case. A concrete failing CI command and the limitations of existing quoting approaches would make the follow-up more actionable.

Rating category versus #45: **unchanged**.

## #12228

[Opening](https://github.com/pytest-dev/pytest/issues/12228); cutoff `2024-04-19T17:30:10+00:00`; pinned commit `ad95d59d6158076768cccd0000b968cd691cb62a`.

Before: **not useful** — The reporter already supplies a concrete documentation gap, an addopts example and the pages needing clarification. Asking for a use case repeats that information, while requesting workarounds adds little to assessing the documentation change. The draft does not address accepted TOML types or how array elements are interpreted.

> Thanks for sharing this issue.
> - Could you add a real-world use case this would enable? [C1]
> - Could you add any workaround or alternative you have tried, or that there is none? [C2]

Report status: complete; type: type: docs.
Missing details: real-world use case, alternative solutions

- Relationship #12053: Shared topic: bit, case, configuration; one report negates a shared condition.
- Relationship #12081: Shared topic: additional, any, because; the same failure or request is not established.
- Relationship #2959: Shared topic: case, com, github; one report negates a shared condition.
- [C1: pytest feature report template: real-world use case](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L19)
- [C2: pytest feature report template: alternative solutions](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21)
- [C3: pytest issue #12053: pdbcls as a configuration option?](https://github.com/pytest-dev/pytest/issues/12053)
- [C4: pytest issue #12081: Capture: copy output when using readouterr() instead of consuming it](https://github.com/pytest-dev/pytest/issues/12081)
- [C5: pytest issue #2959: pytest 3.3.0 immutable fixture params](https://github.com/pytest-dev/pytest/issues/2959)

After (real response received: True):

> Thanks for sharing this issue.
> - Could you add any workaround or alternative you have tried, or that there is none? [C1]

Report status: complete; type: type: docs.
Missing details: alternative solutions

- [C1: pytest feature report template: alternative solutions](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21)

New usefulness rating: **not useful**. Reason: Asking for workarounds does little to assess this already concrete documentation gap. The reply does not address accepted TOML types or argument interpretation within addopts arrays.

Rating category versus #45: **unchanged**.

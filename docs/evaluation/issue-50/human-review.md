# Issue #50 fresh anonymous development review

Review each reply: useful / partly useful / not useful, with a reason.
Separately mark each factual assertion or question presupposition supported /
unsupported / unsure; assess supplied-detail redundancy, relationships and
abstention. Citation syntax and exact quotes do not establish semantic support.
Failures remain in denominators. No #48 rating is transferred.

## R01: pytest #12053

[Opening](https://github.com/pytest-dev/pytest/issues/12053)
Cutoff: 2024-03-03T14:58:35+00:00; revision: 00043f7f1047b29fdaeb18e169fe9d6146988cb8.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/8655
Review: pending. Reason: pending. Semantic support: pending.

## R02: pytest #12223

[Opening](https://github.com/pytest-dev/pytest/issues/12223)
Cutoff: 2024-04-17T09:00:30+00:00; revision: 58844247f7ae4a7a213a73c8af2462253b3d8fc7.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R03: pytest #12146

[Opening](https://github.com/pytest-dev/pytest/issues/12146)
Cutoff: 2024-03-21T12:06:34+00:00; revision: 470edc5884faf7ae9e5297f233a4909d4579fbdb.

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/12146

> pytest-8.1.1
> pytest-7.4.4
> pytest         8.1.1

Review: pending. Reason: pending. Semantic support: pending.

## R04: pytest #10156

[Opening](https://github.com/pytest-dev/pytest/issues/10156)
Cutoff: 2022-07-19T20:03:50+00:00; revision: 34a285986e456406b22b62aa563a64331f640e7f.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R05: pytest #12228

[Opening](https://github.com/pytest-dev/pytest/issues/12228)
Cutoff: 2024-04-19T17:30:10+00:00; revision: ad95d59d6158076768cccd0000b968cd691cb62a.

Thanks for sharing this issue. Could you add the following details?
- any workaround or alternative you have tried, or that there is none [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21
Review: pending. Reason: pending. Semantic support: pending.

## R06: pytest #12189

[Opening](https://github.com/pytest-dev/pytest/issues/12189)
Cutoff: 2024-04-05T09:14:51+00:00; revision: 4e3dd21506a9e543c04c63ebff966a9b604d2b9e.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R07: pytest #12226

[Opening](https://github.com/pytest-dev/pytest/issues/12226)
Cutoff: 2024-04-19T11:34:17+00:00; revision: ad95d59d6158076768cccd0000b968cd691cb62a.

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21
Review: pending. Reason: pending. Semantic support: pending.

## R08: pytest #12116

[Opening](https://github.com/pytest-dev/pytest/issues/12116)
Cutoff: 2024-03-13T13:37:51+00:00; revision: c0532dda18a5cfd0e6f67113bb164485fa80eb86.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R09: pytest #12204

[Opening](https://github.com/pytest-dev/pytest/issues/12204)
Cutoff: 2024-04-10T10:45:32+00:00; revision: 1f001cd1051a4ca4bef251d93e472e625578aaf7.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/12204

> pytest    8.1.1
> pytest-8.0.0
> pluggy    1.4.0
> pluggy-1.3.0

Review: pending. Reason: pending. Semantic support: pending.

## R10: pytest #12081

[Opening](https://github.com/pytest-dev/pytest/issues/12081)
Cutoff: 2024-03-06T00:03:25+00:00; revision: 03e54712dd123138aa4c1035a027e17d0dd9a86c.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/3448
- [C2] https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110

> The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is

- [C3] https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/src/_pytest/capture.py#L935

>         """Read and return the captured output so far, resetting the internal

Review: pending. Reason: pending. Semantic support: pending.

## R11: pytest #7312

[Opening](https://github.com/pytest-dev/pytest/issues/7312)
Cutoff: 2020-06-03T14:20:24+00:00; revision: 61a6ac97054c0bd6f812642b46847c4b7cbede2a.

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/349
Review: pending. Reason: pending. Semantic support: pending.

## R12: pytest #12219

[Opening](https://github.com/pytest-dev/pytest/issues/12219)
Cutoff: 2024-04-16T08:22:38+00:00; revision: 58844247f7ae4a7a213a73c8af2462253b3d8fc7.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/4064
- [C2] https://github.com/pytest-dev/pytest/issues/12219

> Interestingly, the hook does seem to be honored in a minimized example.

Review: pending. Reason: pending. Semantic support: pending.

## R13: pytest #12223

[Opening](https://github.com/pytest-dev/pytest/issues/12223)
Cutoff: 2024-04-17T09:00:30+00:00; revision: 58844247f7ae4a7a213a73c8af2462253b3d8fc7.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R14: pytest #12079

[Opening](https://github.com/pytest-dev/pytest/issues/12079)
Cutoff: 2024-03-05T12:31:13+00:00; revision: 03e54712dd123138aa4c1035a027e17d0dd9a86c.

Thanks for sharing this issue. Could you add the following details?
- any workaround or alternative you have tried, or that there is none [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21
- [C2] https://github.com/pytest-dev/pytest/issues/11871
Review: pending. Reason: pending. Semantic support: pending.

## R15: pytest #12203

[Opening](https://github.com/pytest-dev/pytest/issues/12203)
Cutoff: 2024-04-10T09:18:43+00:00; revision: 1f001cd1051a4ca4bef251d93e472e625578aaf7.

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16
Review: pending. Reason: pending. Semantic support: pending.

## R16: pytest #12228

[Opening](https://github.com/pytest-dev/pytest/issues/12228)
Cutoff: 2024-04-19T17:30:10+00:00; revision: ad95d59d6158076768cccd0000b968cd691cb62a.

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21
Review: pending. Reason: pending. Semantic support: pending.

## R17: pytest #12189

[Opening](https://github.com/pytest-dev/pytest/issues/12189)
Cutoff: 2024-04-05T09:14:51+00:00; revision: 4e3dd21506a9e543c04c63ebff966a9b604d2b9e.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R18: pytest #12203

[Opening](https://github.com/pytest-dev/pytest/issues/12203)
Cutoff: 2024-04-10T09:18:43+00:00; revision: 1f001cd1051a4ca4bef251d93e472e625578aaf7.

Thanks for sharing this issue. Could you add the following details?
- a minimal example, if possible [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16
Review: pending. Reason: pending. Semantic support: pending.

## R19: pytest #12204

[Opening](https://github.com/pytest-dev/pytest/issues/12204)
Cutoff: 2024-04-10T10:45:32+00:00; revision: 1f001cd1051a4ca4bef251d93e472e625578aaf7.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/12204

> pytest    8.1.1
> pytest-8.0.0
> pluggy    1.4.0
> pluggy-1.3.0

Review: pending. Reason: pending. Semantic support: pending.

## R20: pytest #12224

[Opening](https://github.com/pytest-dev/pytest/issues/12224)
Cutoff: 2024-04-18T05:51:07+00:00; revision: 58844247f7ae4a7a213a73c8af2462253b3d8fc7.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R21: pytest #12146

[Opening](https://github.com/pytest-dev/pytest/issues/12146)
Cutoff: 2024-03-21T12:06:34+00:00; revision: 470edc5884faf7ae9e5297f233a4909d4579fbdb.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/12146

> pytest-8.1.1
> pytest-7.4.4
> pytest         8.1.1

Review: pending. Reason: pending. Semantic support: pending.

## R22: pytest #12083

[Opening](https://github.com/pytest-dev/pytest/issues/12083)
Cutoff: 2024-03-06T10:53:11+00:00; revision: 03e54712dd123138aa4c1035a027e17d0dd9a86c.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R23: pytest #12116

[Opening](https://github.com/pytest-dev/pytest/issues/12116)
Cutoff: 2024-03-13T13:37:51+00:00; revision: c0532dda18a5cfd0e6f67113bb164485fa80eb86.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R24: pytest #12197

[Opening](https://github.com/pytest-dev/pytest/issues/12197)
Cutoff: 2024-04-08T11:30:37+00:00; revision: 74f05648d5ea9e69d75f27a77972756ee32f6730.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R25: pytest #12083

[Opening](https://github.com/pytest-dev/pytest/issues/12083)
Cutoff: 2024-03-06T10:53:11+00:00; revision: 03e54712dd123138aa4c1035a027e17d0dd9a86c.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R26: pytest #12072

[Opening](https://github.com/pytest-dev/pytest/issues/12072)
Cutoff: 2024-03-04T13:04:55+00:00; revision: 0951cbc6e4880ee7dfc9b7e56948d83ee086e74b.

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/12066
Review: pending. Reason: pending. Semantic support: pending.

## R27: pytest #12201

[Opening](https://github.com/pytest-dev/pytest/issues/12201)
Cutoff: 2024-04-09T14:22:08+00:00; revision: 17fc20af78d0c7b739806c4e461d2c9b8c30ceeb.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R28: pytest #12079

[Opening](https://github.com/pytest-dev/pytest/issues/12079)
Cutoff: 2024-03-05T12:31:13+00:00; revision: 03e54712dd123138aa4c1035a027e17d0dd9a86c.

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21
- [C2] https://github.com/pytest-dev/pytest/issues/11871
Review: pending. Reason: pending. Semantic support: pending.

## R29: pytest #12053

[Opening](https://github.com/pytest-dev/pytest/issues/12053)
Cutoff: 2024-03-03T14:58:35+00:00; revision: 00043f7f1047b29fdaeb18e169fe9d6146988cb8.

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/8655
Review: pending. Reason: pending. Semantic support: pending.

## R30: pytest #12226

[Opening](https://github.com/pytest-dev/pytest/issues/12226)
Cutoff: 2024-04-19T11:34:17+00:00; revision: ad95d59d6158076768cccd0000b968cd691cb62a.

Thanks for sharing this issue. Could you add the following details?
- any workaround or alternative you have tried, or that there is none [C1]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21
Review: pending. Reason: pending. Semantic support: pending.

## R31: pytest #12216

[Opening](https://github.com/pytest-dev/pytest/issues/12216)
Cutoff: 2024-04-15T07:38:50+00:00; revision: 5f6e825a2687f6bb8bc437e67a59c0a92fb16c06.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R32: pytest #12216

[Opening](https://github.com/pytest-dev/pytest/issues/12216)
Cutoff: 2024-04-15T07:38:50+00:00; revision: 5f6e825a2687f6bb8bc437e67a59c0a92fb16c06.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R33: pytest #7312

[Opening](https://github.com/pytest-dev/pytest/issues/7312)
Cutoff: 2020-06-03T14:20:24+00:00; revision: 61a6ac97054c0bd6f812642b46847c4b7cbede2a.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/349
Review: pending. Reason: pending. Semantic support: pending.

## R34: pytest #12081

[Opening](https://github.com/pytest-dev/pytest/issues/12081)
Cutoff: 2024-03-06T00:03:25+00:00; revision: 03e54712dd123138aa4c1035a027e17d0dd9a86c.

Thanks for sharing this issue.
- Earlier issue #3448 may be relevant: Both concern readouterr consuming captured output. This report: "…turing via readouterr() consume stdout, meaning that logs are no longer available in the "Captured s…"; earlier: "…uterr()` in a test also resets what pytest displays in case of failed tests.". This opening names copyouterr; compare its proposed behavior with the earlier readouterr report. [C1]
- pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C2]
- At commit 03e54712dd123138aa4c1035a027e17d0dd9a86c, pytest source src/_pytest/capture.py:935 contains the cited line. [C3]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/3448
- [C2] https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110

> The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is

- [C3] https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/src/_pytest/capture.py#L935

>         """Read and return the captured output so far, resetting the internal

Review: pending. Reason: pending. Semantic support: pending.

## R35: pytest #10156

[Opening](https://github.com/pytest-dev/pytest/issues/10156)
Cutoff: 2022-07-19T20:03:50+00:00; revision: 34a285986e456406b22b62aa563a64331f640e7f.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R36: pytest #12197

[Opening](https://github.com/pytest-dev/pytest/issues/12197)
Cutoff: 2024-04-08T11:30:37+00:00; revision: 74f05648d5ea9e69d75f27a77972756ee32f6730.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R37: pytest #12219

[Opening](https://github.com/pytest-dev/pytest/issues/12219)
Cutoff: 2024-04-16T08:22:38+00:00; revision: 58844247f7ae4a7a213a73c8af2462253b3d8fc7.

Thanks for sharing this issue.
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/4064
- [C2] https://github.com/pytest-dev/pytest/issues/12219

> Interestingly, the hook does seem to be honored in a minimized example.

Review: pending. Reason: pending. Semantic support: pending.

## R38: pytest #12072

[Opening](https://github.com/pytest-dev/pytest/issues/12072)
Cutoff: 2024-03-04T13:04:55+00:00; revision: 0951cbc6e4880ee7dfc9b7e56948d83ee086e74b.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

- [C1] https://github.com/pytest-dev/pytest/issues/12066
Review: pending. Reason: pending. Semantic support: pending.

## R39: pytest #12224

[Opening](https://github.com/pytest-dev/pytest/issues/12224)
Cutoff: 2024-04-18T05:51:07+00:00; revision: 58844247f7ae4a7a213a73c8af2462253b3d8fc7.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

## R40: pytest #12201

[Opening](https://github.com/pytest-dev/pytest/issues/12201)
Cutoff: 2024-04-09T14:22:08+00:00; revision: 17fc20af78d0c7b739806c4e461d2c9b8c30ceeb.

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence supplied in report:

Review: pending. Reason: pending. Semantic support: pending.

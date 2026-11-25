# Issue #19 fresh blinded reply review

Rate useful (2), partly useful (1), or not useful (0). Preserve verbatim reasons. Review semantic support, unsupported claims or presuppositions, redundant requests, relationships and abstentions. Do not consult the separate identity key or transfer old ratings.

## R01: pytest #12223

Report fingerprint: `066e0c192a002871c121d18857b2f84a109474128cacebfaa21aabef464e7e35`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R02: pytest #12308

Report fingerprint: `920ef6cdf3a36863743364db7ce143558e0f848c9093518435d4465032a0a4c8`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R03: pytest #12328

Report fingerprint: `2ce49c1b30eb6bb4de0b4875cfdfa1ccf64eebc46fc84e759d34a42504d4886d`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.0 / 7.4.4). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fa1d5be3e8b0a34106b35eff092adaa67c9de503/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12328): Submitted issue under review: investigative follow-up
  Passage: pytest 8.2.0
pytest-8.2.0
pytest 7.4.4
pytest-7.4.4
pytest     8.2.0

Rating / verbatim reason / semantic notes: pending

## R04: pytest #12281

Report fingerprint: `53127c4ba1f0edb826f4a90ccfeea5059b36cf0c9c1f140e8fe2981b6f8c6b91`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R05: pytest #12263

Report fingerprint: `4ee3ddb2ec1f60a7f0cdedf39942e9d80577c2a05a64f759dbfe2a6b6928bd63`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R06: pytest #12197

Report fingerprint: `3ea0efab774ffe61d598337bf50dd298f09e72760d34b67f9b77134510169fbb`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R07: pytest #12255

Report fingerprint: `6dbf03f10f7a63b80e8cc677f718b40b9cee7acc057d77fef8e96daf4eddc400`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R08: pytest #12116

Report fingerprint: `6e1f7b9976ef46c7263b036ee715889feace2fcb9851b388cd5355e0afbcf65f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R09: pytest #12081

Report fingerprint: `44e530a927c980b498cbbe145db73746723a83917c3db493001453990aba2631`

Thanks for sharing this issue.
- Earlier issue #3448 may be relevant: Both concern readouterr consuming captured output. This report: "…turing via readouterr() consume stdout, meaning that logs are no longer available in the "Captured s…"; earlier: "…uterr()` in a test also resets what pytest displays in case of failed tests.". This opening names copyouterr; compare its proposed behavior with the earlier readouterr report. [C1]
- pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C2]
- At commit 03e54712dd123138aa4c1035a027e17d0dd9a86c, pytest source src/_pytest/capture.py:935 contains the cited line. [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/3448): pytest issue #3448: capture: keep all output for "Captured stdout call" etc
- [C2](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110): pytest documentation: capture
  Passage: The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is
- [C3](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/src/_pytest/capture.py#L935): pytest source: src/_pytest/capture.py:935
  Passage:         """Read and return the captured output so far, resetting the internal

Rating / verbatim reason / semantic notes: pending

## R10: pytest #12146

Report fingerprint: `d7ec6df3f6bff451cedae9c9c39dbe95996bffa29d348e91c5a7e7e00583d5af`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R11: pytest #12303

Report fingerprint: `8b513edf8c6691bad03d82f3c32b9a9f9fc63117370196d94c7cdc98466fa8da`

Thanks for sharing this issue.
- Could you add your pytest and operating system versions? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R12: pytest #12366

Report fingerprint: `87950b3ea0398b2f3a24a30ca9260eebb3fe4779485d00bf5aeddf5851f3214d`

Thanks for sharing this issue.
- Could you add the solution you would like? [C1]
- Could you add a real-world use case this would enable? [C2]
- Could you add any workaround or alternative you have tried, or that there is none? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L16): pytest feature report template: proposed solution
- [C2](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C3](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R13: pytest #12323

Report fingerprint: `10bc96bc817edc18499ab6303ce629b5b131f8633f834c3564eb8fbb0c83f33e`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R14: pytest #12249

Report fingerprint: `ed0dfc9ab4d62b07bcc4098cdc92a6c45499309d62c8ed56482e487622a25f49`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R15: pytest #12312

Report fingerprint: `fcc5a19663e2c2e744aa50177e37b672024ca5e370e6a9f87424e2b6f9526b75`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R16: pytest #12300

Report fingerprint: `0f5d4c9db3146c65431c304b8febbc681f6b7aece558c27bfef6b660687dd0dc`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R17: pytest #12305

Report fingerprint: `e72d732900bd87b24a1d3bfa5af3bd597435dabb10900eab983a3105b4950f2a`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R18: pytest #12290

Report fingerprint: `cc3f3f6aade21673be6c711f9161f90466a4da0184c2481e8a3d2f6df5f2d4e0`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C2](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R19: pytest #12328

Report fingerprint: `640dc359d39baea3b9918febaf30bfaddaa65d85724989695e1c4d3be8c1d709`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.0 / 7.4.4). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fa1d5be3e8b0a34106b35eff092adaa67c9de503/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12328): Submitted issue under review: investigative follow-up
  Passage: pytest 8.2.0
pytest-8.2.0
pytest 7.4.4
pytest-7.4.4
pytest     8.2.0

Rating / verbatim reason / semantic notes: pending

## R20: pytest #12189

Report fingerprint: `f3ccab8e33ce90eb4ebb263ed3afb95f88dbae277f11f6939ebdb6bb10a3870c`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R21: pytest #12307

Report fingerprint: `d0e5d4831875139848340b0fc7fd8b33fd8d8ab812d975dae1bfa8fe50558a35`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R22: pytest #12146

Report fingerprint: `727398c3da2e8c996647bc9449e0e6d135f8dfaf5f353ed074ece30ac9121ad2`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R23: pytest #12278

Report fingerprint: `dadf38d6d4dd773ecc47f14fcfb7b6c4de05581fa1570d0a1d9980bb50de498f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R24: pytest #12079

Report fingerprint: `76271b5f655fb1f1b14f22c74835cb2a6cecabeffa6d256a405952dd39f5d180`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]
- Earlier issue #11871 may be relevant: Both concern reading test-selection arguments from a file. This report: "… file, and run selected subsets of it using `pytest`"; earlier: "…irs`, to compliment the positional `file_or_dir` argument.". the same failure or request is not established. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R25: pytest #12079

Report fingerprint: `27f23ea3770a82db47fd20e3dc18ac285c222b7d503c432d216e11c032863eb6`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R26: pytest #12287

Report fingerprint: `97eccc0ae37789106f125dcc24aed6ce02dda5ccfa357483933832a3e54273b6`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R27: pytest #12226

Report fingerprint: `b59e56c895aae7ca67adbc0c27ced379a378169995c64017f25f18334d125fab`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R28: pytest #12242

Report fingerprint: `5b7aa7abe6e6ac61d318b28bbbe283f13367b0ba5144f794c9d11ee9dcbb1e02`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R29: pytest #12377

Report fingerprint: `eb8bee07634e05dea452b5970a5f2d8b22d0bf68ab12b736483b81b7904ac978`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R30: pytest #12290

Report fingerprint: `bf646a3ebbf975562340020c153e477f68a595266ef24f38a09bdf7506638348`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C2](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R31: pytest #12255

Report fingerprint: `8a6725eed62ddc233c2d932099aef84cfc36c2d6599674ad96c10d97aa43fa13`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R32: pytest #12363

Report fingerprint: `f263c7a28865930aa248a5a229765477a9a22feb6ef186516d349ef476ddba69`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R33: pytest #12201

Report fingerprint: `4b52ff824a9ba8056c509cfd8658acb8ba3606153490d3933a758affc88d4bb5`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R34: pytest #12307

Report fingerprint: `ad61b0ab94cc386f87a83153603d75dcb46d3c690387973df463b4adc87b285a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R35: pytest #12308

Report fingerprint: `42129636b76375e37c6f8ff26848ca04f7bde53e9843ac87e6769bf2749d4f36`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R36: pytest #12223

Report fingerprint: `f56de6eaeb042e7dcbab99116026e10c5a62cba45ba0217eea2d233c3a9155ed`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R37: pytest #12081

Report fingerprint: `9e3d2123336034809b5182329b135b16548f8ec14c63e5e17cd96830ab9ec3ec`

Thanks for sharing this issue.
- Earlier issue #3448 may be relevant: Both concern readouterr consuming captured output. This report: "…turing via readouterr() consume stdout, meaning that logs are no longer available in the "Captured s…"; earlier: "…uterr()` in a test also resets what pytest displays in case of failed tests.". This opening names copyouterr; compare its proposed behavior with the earlier readouterr report. [C1]
- pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C2]
- At commit 03e54712dd123138aa4c1035a027e17d0dd9a86c, pytest source src/_pytest/capture.py:935 contains the cited line. [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/3448): pytest issue #3448: capture: keep all output for "Captured stdout call" etc
- [C2](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110): pytest documentation: capture
  Passage: The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is
- [C3](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/src/_pytest/capture.py#L935): pytest source: src/_pytest/capture.py:935
  Passage:         """Read and return the captured output so far, resetting the internal

Rating / verbatim reason / semantic notes: pending

## R38: pytest #12072

Report fingerprint: `47d125c059a1326582b3442be27dd13849285458984942da6e7c33794363128f`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R39: pytest #12228

Report fingerprint: `97204f88745787150d6a94cbb38d42f3fecba531f4d76f7bb68468fb49e1ac17`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R40: pytest #12351

Report fingerprint: `d27588ee0a9e4849068a6e9cff06829590a5eba7ecaccb0ca4f0a6249d138b15`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.1 / 8.1.1). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12351): Submitted issue under review: investigative follow-up
  Passage: pytest-8.2.1
pytest                        8.1.1

Rating / verbatim reason / semantic notes: pending

## R41: pytest #12312

Report fingerprint: `52dd5bdf075276e5a0cfd0ebd505b15093551a91cf66d088e21a3a84411dd2be`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R42: pytest #12303

Report fingerprint: `fc5302d390dee68f3374dd585a92c95fd7297f5d33c0d6fde98355a8519b9c57`

Thanks for sharing this issue.
- Could you add your pytest and operating system versions? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R43: pytest #12360

Report fingerprint: `3d84ade8242f096bdb168fa68403d114acee86037b4b2dbe10320bbe40056096`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R44: pytest #12146

Report fingerprint: `d14e28a63d5c5435037af4268dc42ea736b713e726909c706acfd9b7545d7e24`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R45: pytest #12298

Report fingerprint: `083072596ce6a0e56efff497d5db212714eb4954206a3385530d2ba03aa7ae70`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R46: pytest #12328

Report fingerprint: `46d3193ce642a1d3f98630a3d64aa898ba2d909071f724fb9c8df1bac775bd2a`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.0 / 7.4.4). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fa1d5be3e8b0a34106b35eff092adaa67c9de503/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12328): Submitted issue under review: investigative follow-up
  Passage: pytest 8.2.0
pytest-8.2.0
pytest 7.4.4
pytest-7.4.4
pytest     8.2.0

Rating / verbatim reason / semantic notes: pending

## R47: pytest #12053

Report fingerprint: `3142b41c23d6735beabe23b0f7f19e68101969a8431de3d6c1e25596a05d971b`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R48: pytest #12201

Report fingerprint: `80cd418c4d133ef75037e9badbc9cf31945b011492bdac55801add7611bf78d7`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R49: pytest #12298

Report fingerprint: `9076c6f375dd6f8c0a8eb82efa268bd12602d62c9a33383d89a96e1116ddba65`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R50: pytest #12219

Report fingerprint: `0df19d2b59e47b4f58875c8cd0032527e9582ab9778d514d082dfaa124c1d939`

Thanks for sharing this issue.
- Earlier issue #4064 may be relevant: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation. [C1]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R51: pytest #12053

Report fingerprint: `6cfa0281dd762fcb33929799e2ef046c91c8646645c0c8b613a3094b3eec0d77`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R52: pytest #12083

Report fingerprint: `b41c435c732e1bbaa3e126ab02c33f55942ef69c619c12f811d2161e091c4745`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R53: pytest #12079

Report fingerprint: `7cabe06e2ccbf999db5ccf228175528eb3927d00d1bd272a15b870b091b18db7`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R54: pytest #12249

Report fingerprint: `73648f1b00d1ca2acb0dc412eb935cb3a6decb7e33e9b02765c81aefe4e3e5b0`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R55: pytest #12351

Report fingerprint: `ab779c278660c342a85e5bc0e9344904e77e9254c8ddb9e2ab45fa86198fc488`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.1 / 8.1.1). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12351): Submitted issue under review: investigative follow-up
  Passage: pytest-8.2.1
pytest                        8.1.1

Rating / verbatim reason / semantic notes: pending

## R56: pytest #12308

Report fingerprint: `6540a189746512126034246399a1008403b8ce13596abfe2a2ae7b79a69ec157`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R57: pytest #12204

Report fingerprint: `7daead1130d3b7d878b9f562d861b6940520ea89f9827be8c6f6c50de5f38e46`

Thanks for sharing this issue.
- The opening contains conflicting version evidence (pytest: 8.1.1 / 8.0.0; pluggy: 1.4.0 / 1.3.0). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12204): Submitted issue under review: investigative follow-up
  Passage: pytest    8.1.1
pytest-8.0.0
pluggy    1.4.0
pluggy-1.3.0

Rating / verbatim reason / semantic notes: pending

## R58: pytest #12216

Report fingerprint: `495d40b78bb12baaec8220a7646a3044e8b27775c9d404631837846bd52b92c7`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R59: pytest #12223

Report fingerprint: `83c69cb44dbda4d79fc71fd7826e28c4094dbabf63ed465a558da0c615a26ccf`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R60: pytest #12224

Report fingerprint: `61b1c3b52b063390d18030bee06b695f41eb7be8bf0dfcf17a7e4d8f9bc580af`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R61: pytest #12352

Report fingerprint: `9473bd65fa4fbbe491b7d20c99b449b42e08a88578718e0ccdd14683ccecd754`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.1 / 8.1.1). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12352): Submitted issue under review: investigative follow-up
  Passage: pytest-8.2.1
pytest                        8.1.1

Rating / verbatim reason / semantic notes: pending

## R62: pytest #12216

Report fingerprint: `dbed8bff05cbca6d123f43c5c35eb69744e63e95f185c832ad327b2a2c3aa287`

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R63: pytest #12197

Report fingerprint: `28a84053d6ca18b8c2ebf368821ce555bd125b6c7abfaf04a9886b3173fa8df4`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R64: pytest #12357

Report fingerprint: `51fd5d449494359321fd4022be4da221c91bacb643e5204e498ca11a960a8a98`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R65: pytest #12290

Report fingerprint: `5bffe7f5d58c6d66ded1a30a3a5f379eebc44d7d1c68ebccc67a409edd2b1e69`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C2](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R66: pytest #12255

Report fingerprint: `5306eed48b27591e178d04d8113a24ffbe116818b48d9e83de28070dba6b25e4`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R67: pytest #12300

Report fingerprint: `c9023590dfd0e70d466bea732aa6ea0d497d53ed2515c3bbf9b949a38f9f4e19`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R68: pytest #10156

Report fingerprint: `ab42a27e1bde394d5d95d005012a1640bd2538bf9c069c8de071be97dd2919c1`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R69: pytest #12298

Report fingerprint: `dd9a9402e951560afb85bdc9b8bfa5814445dcd83ac1fc3cec1e488c1d40f1f6`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R70: pytest #12224

Report fingerprint: `48aac7ebf67762c96747b01af90817d806aa1638368a312cb4eead63a2332301`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R71: pytest #12189

Report fingerprint: `8507d5a41abefcf684efac87c1f9253eedb4aca7148d5d712193a53b65357d4b`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R72: pytest #12083

Report fingerprint: `45b1c5944f52befd0c536a0fb28ddf24b88217fbca96249984138bdd2f97c82b`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R73: pytest #12366

Report fingerprint: `06f5a1092c783ca321b89878c92d86b757e27d2ea8de38a1cbcf5d597e8e8201`

Thanks for sharing this issue.
- Could you add the solution you would like? [C1]
- Could you add a real-world use case this would enable? [C2]
- Could you add any workaround or alternative you have tried, or that there is none? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L16): pytest feature report template: proposed solution
- [C2](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C3](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R74: pytest #12376

Report fingerprint: `586a896d3bdab17883aa22fefb74757c1dc475d82d1bc5dc49b1dc270d6a4c6e`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/24abe4eb03f64bfed301e6d70dfcf4f0c6a8cc0e/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case

Rating / verbatim reason / semantic notes: pending

## R75: pytest #12300

Report fingerprint: `1598a46cb77fd850e2905af8de6ad0de9bf531c66a303517e9e4fef154acd056`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R76: pytest #12352

Report fingerprint: `9e461cb6da522ae8e2a7a29c2512e85eb14fc6c3d189487bfe61f22779c8bbcc`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.1 / 8.1.1). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12352): Submitted issue under review: investigative follow-up
  Passage: pytest-8.2.1
pytest                        8.1.1

Rating / verbatim reason / semantic notes: pending

## R77: pytest #12081

Report fingerprint: `3e442a3809449da58ff946091b78443a2729be5cee0fa0d9edf31351a7c9ec2f`

Thanks for sharing this issue.
- pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110): pytest documentation: capture
  Passage: The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is

Rating / verbatim reason / semantic notes: pending

## R78: pytest #12367

Report fingerprint: `c01cd21bfa59d98ed9aa06fb46affee29990017cdd71cb67b36c9557d0569ade`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R79: pytest #12281

Report fingerprint: `9ea64eba96256b6a95420c2df5acca05cb9d22fed119e9f70b687d5f4955c2ec`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R80: pytest #12293

Report fingerprint: `2e98a7b911d944ff5200219f98bfa5424994d005883288d67bba4f7673fe2d33`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R81: pytest #12360

Report fingerprint: `17b1446651ef2ba5d2f5eec82e3e2f51d260703ce7a55e540859b044b4d65921`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R82: pytest #12371

Report fingerprint: `0b20ab718ddbc10985072c1bdc077a28c6083413dfb7bb1a5cc6f68c5e36cf21`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R83: pytest #12231

Report fingerprint: `ecac5f55bbf55451172c636bd9b2ba81b575d9b6ddc5b1b377fa5cdd8fc24b87`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/3617ef1c79d686a42ce645b0e28dda824a74e715/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R84: pytest #12116

Report fingerprint: `cb38a913de4bcb79fe5b9bb3d74954c5de56220f1460f91a33970ac056a6db04`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R85: pytest #12053

Report fingerprint: `21cbd9ba650546e3f009c75fb34e0d8dbd21332b2d737ab0e3788e5df15a7077`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R86: pytest #12287

Report fingerprint: `6a89b13784b460c3ea141ae8842cfe9e42e5335a0cfcea4f000d0eb41d88d007`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R87: pytest #12377

Report fingerprint: `7062fbcdcbbca9b8899a7fca0af0bc8968eeca8e0b3527641d9c0fbf99feba55`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R88: pytest #12204

Report fingerprint: `0547fdb2bef67426c0cfd3fb1d27aeacecb2fb4fb8ce2fad956b16ffbdcad735`

Thanks for sharing this issue.
- The opening contains conflicting version evidence (pytest: 8.1.1 / 8.0.0; pluggy: 1.4.0 / 1.3.0). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12204): Submitted issue under review: investigative follow-up
  Passage: pytest    8.1.1
pytest-8.0.0
pluggy    1.4.0
pluggy-1.3.0

Rating / verbatim reason / semantic notes: pending

## R89: pytest #12203

Report fingerprint: `ae8b8f3012db69900a10fe5e112ebc2b514539fec699d912f7706f6734790af6`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R90: pytest #12312

Report fingerprint: `6791fd59835c6efcf7a0a63ed6ad817a51405447a5dd14a3804d714b9ced5390`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R91: pytest #12083

Report fingerprint: `c04cc93484571355c5d5fd6f2ef912a5c11a9242a20dcacbd1c3f4fb8872df0e`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R92: pytest #12231

Report fingerprint: `689ae59a63edd7cbb3a2cd69c9bf5ec56e6d52d3bba009026d5460e8ceb889c4`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/3617ef1c79d686a42ce645b0e28dda824a74e715/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R93: pytest #12197

Report fingerprint: `39617f4a9bf76e8048e5707fac8cf09d57786ea12ddfe3ccd923b36fde824fe6`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R94: pytest #12219

Report fingerprint: `ef232902691dce54c58a3e1a509c68d9c3f949698c11c017e26648dc2946b39d`

Thanks for sharing this issue.
- Earlier issue #4064 may be relevant: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation. [C1]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R95: pytest #12371

Report fingerprint: `fb8f544d7fc0b71a4e8c16badfe115d082e25921a2717b934788fa674c4f92a9`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R96: pytest #7312

Report fingerprint: `323e8650e705741bee4e24aec639a93712f89b3811b37685c55dfc10eb5f4dd3`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R97: pytest #12072

Report fingerprint: `0f269216778e6339c0a576a4689426eee700160b2710748010159a6e2ab0bda2`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R98: pytest #12363

Report fingerprint: `639312adf24bddf4834721d46f0fb6849685fa4897bbe720c9d835744d31cced`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R99: pytest #12357

Report fingerprint: `9a60a5c0fa9a511bf4d8d60c49bb3b435202740f106776f34da7db7ed0a0940b`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R100: pytest #12263

Report fingerprint: `ab34e6a171da7f86c459a02dc94f55f285f832f8c198806a9070254cb44efe57`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R101: pytest #12323

Report fingerprint: `72a39ad06fa1d8fa84e5d5819e1c683314a68a720175bdebaf22a96afc082910`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R102: pytest #12376

Report fingerprint: `36831ecbdbf4b2bd987aac7190a7631c2cfd1f8f3b18ddf0f09568d65cd3aea7`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/24abe4eb03f64bfed301e6d70dfcf4f0c6a8cc0e/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case

Rating / verbatim reason / semantic notes: pending

## R103: pytest #12116

Report fingerprint: `6a6f1a10c8d1c790aeffee4df98ac4e81136455c4556063c2cc165f30dc84b27`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R104: pytest #12281

Report fingerprint: `4e626e93fea017867d35618639f08712cb2a61aa03f42b399cc4666134646bcd`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R105: pytest #12367

Report fingerprint: `304a4e7e64427160b03c10e2c10876b8dec5134586aeba65b0906c2947a7e725`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R106: pytest #12226

Report fingerprint: `010fa74c3a357837ccf4b13f4d26d38e4889d6c5f8d5e0c29e1ad97727248ee1`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R107: pytest #12242

Report fingerprint: `971ff8ff01011a63ea1e26c843b99b6ba4669f03116517904330779d45bbb32c`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R108: pytest #12216

Report fingerprint: `847d74d8a7821518d974c6315ac98d0a40a5ec28d6e527696ea06fddba059d2b`

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R109: pytest #12072

Report fingerprint: `837be0bb1c07c4e00f6d8757129a4629a644a4d8f2439096220aeb8f5d3dae04`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R110: pytest #12371

Report fingerprint: `83e94569e498aa58d432af89ec3c6eff29609d9cb8ffd5350c3b77f9f60c7d6f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R111: pytest #12224

Report fingerprint: `b9eb0bf75cc98fdf6293eb5f9a164583f70885284eafa68267192d24217af4e6`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R112: pytest #12201

Report fingerprint: `8da92204b2b3760c960db3fe5a12b75e20d7f021db4eeadd5baa026aa8bc22cf`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R113: pytest #12219

Report fingerprint: `2d50b51eedb8e51700c08a43c826f3de554a6020c0c7d71d8ac1ccc4628a0ea7`

Thanks for sharing this issue.
- Earlier issue #4064 may be relevant: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation. [C1]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R114: pytest #12357

Report fingerprint: `774bf657e36b345f3c17648ea1571ea549a392d03a80bbde4be5693098cd9860`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R115: pytest #12303

Report fingerprint: `622cfa06ff2efe7080fb3370bdfc83db02de158d53bd1ebc76ffa0990eb27177`

Thanks for sharing this issue.
- Could you add your pytest and operating system versions? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R116: pytest #12189

Report fingerprint: `29fbcb103b6bab677ac26ab8f182d286aefe3bbb025a6a3e9ba2666492a2d930`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R117: pytest #12203

Report fingerprint: `58cd3e6bcebf9edaf756fc9a469586dd51cb27c4339151e9c3cdbfc0dcebbbef`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R118: pytest #12293

Report fingerprint: `a89661e9c953a48184d823fdbabe163f6279ba8a4d4dcb04924cdc1959b36a42`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R119: pytest #12377

Report fingerprint: `5bc7fc35d7c08dcbe833a0df67c7b4a368c456468b43626b5a107152103e1178`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R120: pytest #12273

Report fingerprint: `b830d23f73ac7b60cb1eff827a24e7a0d78bb63449cebbc06644fe47ecd0fdd0`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R121: pytest #12376

Report fingerprint: `241571404f393478c38705a91b0e0efa5338bed7041cef3c47734233247af5ae`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/24abe4eb03f64bfed301e6d70dfcf4f0c6a8cc0e/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case

Rating / verbatim reason / semantic notes: pending

## R122: pytest #12228

Report fingerprint: `bb25dbe18a7cd1561b8634f3a181a482811c3d9245f891c577609f3f5a012130`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R123: pytest #10156

Report fingerprint: `57880e94a539151f889f6020dc9e4235f70de2efae9987a4f74738917f33076a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R124: pytest #12278

Report fingerprint: `0046fae09547a82504cd5f07e249d90f245fc1b89b0592d2f66803a061b064fc`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R125: pytest #12363

Report fingerprint: `5d1bebe2cd736eeeb23b82f107a2bc729d800627b1e98a2b4704f05508f37f06`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R126: pytest #12366

Report fingerprint: `e9bff7f5959d854733df61989d0c7c210639e93c3d8e035522e24cebdd1e420f`

Thanks for sharing this issue.
- Could you add the solution you would like? [C1]
- Could you add a real-world use case this would enable? [C2]
- Could you add any workaround or alternative you have tried, or that there is none? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L16): pytest feature report template: proposed solution
- [C2](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C3](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R127: pytest #12305

Report fingerprint: `6446bda5682daaf782c3c9b53a57e7eb59b2b98f6e50e5bcad2256f0b2f44c96`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R128: pytest #12204

Report fingerprint: `28e6d6e168e186347973564c55ad02de7cd2212cf06f387b594740f21bc832a2`

Thanks for sharing this issue.
- The opening contains conflicting version evidence (pytest: 8.1.1 / 8.0.0; pluggy: 1.4.0 / 1.3.0). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12204): Submitted issue under review: investigative follow-up
  Passage: pytest    8.1.1
pytest-8.0.0
pluggy    1.4.0
pluggy-1.3.0

Rating / verbatim reason / semantic notes: pending

## R129: pytest #12360

Report fingerprint: `a1dab07d0e44dbb480e25d4d091a367a079637183a6c135fad593ca3718a832a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R130: pytest #12242

Report fingerprint: `eef07f8fe172f38e4ea4a1b5923f72d2c31fddf290e15828579d484230e903d1`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R131: pytest #12367

Report fingerprint: `ee08c102d389261345b2fecbd7c43a256c3591419a50029da85efb4b0e93fd39`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R132: pytest #10156

Report fingerprint: `3ce2d5276f2073495d944c33a82877fe97346f7d5430133e865453586bb0aed1`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R133: pytest #12278

Report fingerprint: `bdf3bc4a5268f548aed30c2cd24b49eeb58b4cc1fa7bd684d30329d43914120a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R134: pytest #12203

Report fingerprint: `e5233cc52bca8a8c679759161aea0c212c0e0066ded7660a5fc834fc0594f0d6`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R135: pytest #12287

Report fingerprint: `4302efe2a1f0a742ab475ff400ff1b0f377837dd9889d10d9f080672df4d8baf`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R136: pytest #12273

Report fingerprint: `7f5a91776f67ef8bf531b4d6ff52dd3c5d8d66251a0d24c38be5ff929c89fd39`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R137: pytest #12273

Report fingerprint: `8df7cf1b6f9ffbc894021b6d1f0c551b3b0b9a2fc9f867e30609497fcc3e73a2`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R138: pytest #7312

Report fingerprint: `74e9cd24ce6b9a55d466f80fd7c0a3f92b7ebfad66b2d535c7eb211dd4beea77`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R139: pytest #12226

Report fingerprint: `c969a18eee665b78987d88b96b525eb9621d2a9a95ff0320bc696a7dca73faa1`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R140: pytest #12231

Report fingerprint: `83d4459eef05f52019de95bf232a5e9f6d3856f9b32419e3c985c9dbd9b6d3fd`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/3617ef1c79d686a42ce645b0e28dda824a74e715/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R141: pytest #12249

Report fingerprint: `7b04395d015455e32f3dcbc5f94d450047d15dbd108d6153d86ca461872ba38f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R142: pytest #12305

Report fingerprint: `e8864bb9080fa25c3f6046523bf8685e721013d1b8298e5b5627bce83df335e5`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R143: pytest #7312

Report fingerprint: `d521e4cc543c4a786450894e3f70e017c3ec414ba769aab2daf0e68e5a2e9038`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R144: pytest #12323

Report fingerprint: `5bf96c016f9a8135ae16420cb0f382018d2117e3ebd5bf6c82f6deeb4c7d8f3f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R145: pytest #12228

Report fingerprint: `38b7ebd76fe33194d26d06f8767ed618cb12f58a77dff78b823ed6ed3483c9b2`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R146: pytest #12307

Report fingerprint: `fc58408fe78be98091177d1e8d8060c4c0de2f3e7a66ee5c9b76aaab03ae1ea9`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R147: pytest #12263

Report fingerprint: `909706d11c0dfbb574b0b6c519bfedeb5b02ee3e9beb7b3a37937ecb3d17d907`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R148: pytest #12352

Report fingerprint: `af5f0cd70c97849896f4e6ce8a89cee34c3c035d5dceffc21d4ee2409c37254f`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.1 / 8.1.1). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12352): Submitted issue under review: investigative follow-up
  Passage: pytest-8.2.1
pytest                        8.1.1

Rating / verbatim reason / semantic notes: pending

## R149: pytest #12351

Report fingerprint: `8080eb1649ccff7c068775fe7b24820b130d80cfc2236bb22965d0fe5634c38c`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]
- The opening contains conflicting version evidence (pytest: 8.2.1 / 8.1.1). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C2](https://github.com/pytest-dev/pytest/issues/12351): Submitted issue under review: investigative follow-up
  Passage: pytest-8.2.1
pytest                        8.1.1

Rating / verbatim reason / semantic notes: pending

## R150: pytest #12293

Report fingerprint: `d14372f5544f6b777be6024dbb403e6b7254e63328f80e3d7dc9077ee340dee1`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

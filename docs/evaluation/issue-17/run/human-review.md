# Issue #17 fresh blinded reply review

Rate useful (2), partly useful (1), or not useful (0). Preserve verbatim reasons. Review semantic support, unsupported claims or presuppositions, redundant requests, relationships and abstentions. Do not consult the separate identity key or transfer old ratings.

## R01: pytest #12201

Report fingerprint: `4a9c3b16a27f139eb3d0841e57eebe217711a272f6fc4902402a4da6eda4e6e3`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R02: pytest #12273

Report fingerprint: `6ca1870f281c8c889efbbea2e7af0054c7084d40db12725391990daecca988cc`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R03: pytest #12053

Report fingerprint: `80fd5849cc622f77a39d8be282e397419eb16a47359bd67fd2b862af12796e27`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R04: pytest #12290

Report fingerprint: `c6bde6180069b4191b45307e602efbbf20ea51d060b9ca0b0918de7491b6056b`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C2](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R05: pytest #12079

Report fingerprint: `54127a91daae87e5fd20f88c867e6b9421a8945a517d634db6d80e9cce390730`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]
- Earlier issue #11871 may be relevant: Both concern reading test-selection arguments from a file. This report: "… file, and run selected subsets of it using `pytest`"; earlier: "…irs`, to compliment the positional `file_or_dir` argument.". the same failure or request is not established. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R06: pytest #12216

Report fingerprint: `4e134447a02f440ef752f8fdd1f511e5cf98d90cc21c3a361fbeaace669bb3f8`

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R07: pytest #12081

Report fingerprint: `09c35fa8897517dc096101bd69b617804888a9a9cc7ee9b90a1dcd225c4f7b67`

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

## R08: pytest #12079

Report fingerprint: `fa9ee8d4003422e7c1cc7888d98102f0a30352016bd60d6e570a2956ec7ce792`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R09: pytest #12072

Report fingerprint: `e6d58c4cb2394838d58d9255b70c4e0f2e8c58430033c24d0cc5254d269f6552`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R10: pytest #12053

Report fingerprint: `414e6d3cf1e089e745541de2ad20685350da4b72963b51da16cf8f92840c54b9`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R11: pytest #12242

Report fingerprint: `b9b6d3e01871a4e1e3db1e71f8e614f882e9d34a421f24d97772ed46c3029b45`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R12: pytest #12278

Report fingerprint: `a565f9460305745f2f58add50c1860137e9cd1c6211f0e24e3fce19467c161d7`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R13: pytest #12053

Report fingerprint: `78a022352b00b4500cab75785f45dd988cd31c4933432d34d7abd71c7b97e027`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R14: pytest #12116

Report fingerprint: `dc2c115f2bd031b0c86c16b09fa3bfa2f467ffc02e5cc4f6e17360b006721554`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R15: pytest #12223

Report fingerprint: `22b1328b32d074a884d8ae508448fcc712b432f89338116f030989459ab62b7a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R16: pytest #12273

Report fingerprint: `fd82c3213965062527548105ee10f3cd33ab2c9f216a6f4dc79b50dcbae4181c`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R17: pytest #12281

Report fingerprint: `1bdac8bc49c1b1053b3caccf35330b20fe2acb3c2a9edcd280643a48cb41b72d`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R18: pytest #12255

Report fingerprint: `2830b087ca716f73f3efaa80b84addfa7d98813c14cc3bfaef8078f407f29484`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R19: pytest #12219

Report fingerprint: `9d149543d493c3d731e898699c2c8d355793822a9f9eb030a0fdbcdbfd68c247`

Thanks for sharing this issue.
- Earlier issue #4064 may be relevant: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation. [C1]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R20: pytest #12201

Report fingerprint: `96c49501e77c3c7e77cf41cf462f72c3c37af8773fdf0840c5a7d8877722a709`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R21: pytest #12146

Report fingerprint: `fb4795e313817d3a3d2ed1cb12c24d5bd8c35175c9067e052b66f74d00841d27`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R22: pytest #12249

Report fingerprint: `9f79b166afd94b19f3c751f5c35a6243316a56346f9c8b882027a89ddf41d6aa`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R23: pytest #12146

Report fingerprint: `db87eaf98653edc6a608007bdf6cf9da36cfe405d396cfdd85f3b9a81d173a31`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R24: pytest #12281

Report fingerprint: `ba28e9a27f74005c5dbfe4f9a552dc8b1daa2f45a2f4fa080f9b4fa3cc9f8e1f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R25: pytest #12255

Report fingerprint: `d4551e9a8a259db54c28ed4bca5e244ccc3c485472da3bc46ef0f2212fb5adc8`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R26: pytest #12231

Report fingerprint: `0178d2174055b3d91466c1bf01c89445847f26ea8c81908708935951591a377f`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/3617ef1c79d686a42ce645b0e28dda824a74e715/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R27: pytest #12263

Report fingerprint: `43aa1d4447b1a7a58cfa7f43a12af124f344642135c47bbeb81069bc40b6b255`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R28: pytest #12204

Report fingerprint: `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b`

Unavailable: 1 validation error for IssueUnderReview
body
  String should have at most 16000 characters [type=string_too_long, input_value='My session fixture can r...ot 2.7 GiB logs :-)\r\n', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/string_too_long

Evidence:


Rating / verbatim reason / semantic notes: pending

## R29: pytest #12263

Report fingerprint: `1f55948fa1f080ad1ebbba0c1d5184b1f5cde546715fcb44db3676e215755ccd`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R30: pytest #12226

Report fingerprint: `3bc7877dd231ec721b76f103339673bc61c45154cd9ee4c4e2904db24f8025c6`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R31: pytest #12216

Report fingerprint: `4543d469833c2cc9e73acd9b78325af06a48c50a1ffa71af87bb301731058545`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R32: pytest #10156

Report fingerprint: `c46da5c6a6cb912bb417865ce2a9ec241dfce11ca34ef31b1f5089c48eb0cd03`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R33: pytest #12226

Report fingerprint: `dba25ddd3a184fe74763faadd24b5a2766bada99f74f544b80ab09fae9008073`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R34: pytest #12287

Report fingerprint: `13e2f0568b6f2de4c23096db46e7779bd5037234a53b12717d364059a902092a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R35: pytest #12083

Report fingerprint: `0643f1c982090cb34f6b2f935622ac7e71092662eddc9ec6f8cbceca5eec2a18`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R36: pytest #12223

Report fingerprint: `4547ee9667a6e422b5ea6ac38bace79977e238d9224ee5ade41dbc9fd1f62584`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R37: pytest #12290

Report fingerprint: `66587d01c5020b02ccee7a9eeb069231edf87da4a36bb2b575de7766a8de8bc2`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C2](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R38: pytest #12072

Report fingerprint: `7f2fae9e3015246d75a1ff5a3f48c8d1af25ee32022da36bb4f8328c66045a98`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R39: pytest #12287

Report fingerprint: `7fcfc88d4ea9cec7b34ec15f765f371abcfa62202e278be3672585f1f2615ef8`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R40: pytest #12081

Report fingerprint: `4ea2632ef9b3e05f6c028de6a3e8f0d39861217277727fd9d9d4d4083a92e254`

Thanks for sharing this issue.
- pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110): pytest documentation: capture
  Passage: The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is

Rating / verbatim reason / semantic notes: pending

## R41: pytest #12242

Report fingerprint: `4cc7905c08a833ee9d2882c081b4e2ca7a66cc2c6ff0cd035c649b9058f8962e`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R42: pytest #12224

Report fingerprint: `76a04f07369a2e8c3dcd0317e3a16a24729424ab406ed6df83ee84a412cc9514`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R43: pytest #12281

Report fingerprint: `05215c7bb0a8034d6d87395fc3718bd43ae1621e2f22132a11f7d5bf006ca92f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R44: pytest #12226

Report fingerprint: `0eebd9e0ba66f7fa06b93299ed80f5c510fc699141b4448a9d6ce25f7b409160`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R45: pytest #12219

Report fingerprint: `cc99e82002721c873636ad45f33e6ef9fa0cbb3010f6dce70437de024ef13401`

Thanks for sharing this issue.
- Earlier issue #4064 may be relevant: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation. [C1]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R46: pytest #12249

Report fingerprint: `7fdf8974779f74a37560b3968e56eab9e4be52f2c3e45737045806edf4de412f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R47: pytest #12242

Report fingerprint: `6a2b267bcace51abc672fdbb1f96cc9399d878f034b6edee25ea1c7d6a63925e`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your pytest and operating system versions? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R48: pytest #12263

Report fingerprint: `96b0f898544550c97320d82f95f703a99524d4085a6291cdb32b168a062fbecf`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R49: pytest #12287

Report fingerprint: `75452fb3a76347fcb2e6bd4821d8749dd51081c4308159551a469320daec53a1`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R50: pytest #12072

Report fingerprint: `513d2d440869915baf4a2484fd65e561618b278e9ccf84019f0cbb30623c640c`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R51: pytest #12204

Report fingerprint: `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b`

Unavailable: 1 validation error for IssueUnderReview
body
  String should have at most 16000 characters [type=string_too_long, input_value='My session fixture can r...ot 2.7 GiB logs :-)\r\n', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/string_too_long

Evidence:


Rating / verbatim reason / semantic notes: pending

## R52: pytest #12278

Report fingerprint: `dbf82dda83bc348dd24ffdb528e36621038f10735f923089e0352e2ba3db9c48`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R53: pytest #12189

Report fingerprint: `d317008d8874117f2d97fd713851d2771f64227d1b0ce1842c800b4f25cf973f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R54: pytest #12197

Report fingerprint: `bf5280eb2f3be8fc2d54b34636a51b0142ac8866b7f3c3cfd90d6fbd713fc5e8`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R55: pytest #12116

Report fingerprint: `9f23c7859e315baf23721d404bac9e4939dc1ebbfa201a6ea63ed195cff92be0`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R56: pytest #10156

Report fingerprint: `56a7efba592857a806b0f7afc89d01e260e7ac247fd52bdf2113f9996de53043`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R57: pytest #12290

Report fingerprint: `e6ce3ad1e84c78f67aa1e7c352c0757c40ab995adc3c7440c918bcb8bf04cda3`

Thanks for sharing this issue.
- Could you add a real-world use case this would enable? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L19): pytest feature report template: real-world use case
- [C2](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R58: pytest #12146

Report fingerprint: `c94e8eccb087a1e7331210ba6b721c12adc59b2e0c6b3893cfcefea1d8217d06`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R59: pytest #12081

Report fingerprint: `0ab2144aa74ded3c82877aedd8751dd95226fb7175ccd3381037565ba4c57b22`

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

## R60: pytest #12116

Report fingerprint: `be35a7178e5336b91e9b97791d3008934deb44257213f7d7aa8a7c9b53fa24bb`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R61: pytest #12249

Report fingerprint: `5d51315a7795e16bdcab0717fb256effe9afb683e6a44ee6382b4e1e9d167965`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R62: pytest #12223

Report fingerprint: `27eb2c7ee0b45f9b58f3c85cfb60d42aa12083f0b8599f5bc0a1b08b57831ca4`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R63: pytest #12079

Report fingerprint: `cad682a861aac5c20746b6c7f77c6dcd19865454a134d5a33261d14349500548`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R64: pytest #12273

Report fingerprint: `e63d9c58cc60781e2edb04fa960f6835815b07915eee6e5a82f090982d11d119`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R65: pytest #12228

Report fingerprint: `48ea315bf137e4a803e6ea4f01c6d226c08bb169d0a7518dc7b1173966eb3545`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R66: pytest #12228

Report fingerprint: `1d11e6808c235881b3e6587e2c1189629edd17bbc97224a83e86427bda157467`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R67: pytest #10156

Report fingerprint: `8d4a941c55a9478a855890161ae093af9a79597ab034793b81edb7566d9895ba`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R68: pytest #12083

Report fingerprint: `27fba33ad3f26b541ae05961b669e35ccf7c7908eee6ae1c855464c084e3896e`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R69: pytest #12255

Report fingerprint: `10d26d03c44fee981a4431ce60252e086eb7fa8163751aca69f3303eb6cb2491`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R70: pytest #12197

Report fingerprint: `75a00465fcd863fa345e4b57a0dd1575c353fd638bf524739705e7a311ef785e`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R71: pytest #12278

Report fingerprint: `719ddda4b828851de1b97ff62ffe9ee1f974601babd3c83e4756afabc5a372df`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R72: pytest #7312

Report fingerprint: `3d2d683610c04c2f0cd28f7172efc3de00d3204c4f4cb57eb973e71b8d9992d8`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R73: pytest #12204

Report fingerprint: `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b`

Unavailable: 1 validation error for IssueUnderReview
body
  String should have at most 16000 characters [type=string_too_long, input_value='My session fixture can r...ot 2.7 GiB logs :-)\r\n', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/string_too_long

Evidence:


Rating / verbatim reason / semantic notes: pending

## R74: pytest #12083

Report fingerprint: `3931b3b4e1e48502415791ea3b1e34c386a373b899ce704e45a6f4fb83553d83`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R75: pytest #12216

Report fingerprint: `461793439fdc61bdafe00d6e53edf899b2f970c73343dd139c7a7c3b4d64e7a6`

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R76: pytest #12203

Report fingerprint: `6bbd68dffddb894476a71e38b9b86e27f0176e759dbafce5b37309de890689dc`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R77: pytest #12203

Report fingerprint: `3fe3eb7ef4c7a8999953bf280e64eac06f0da349fd3d6be26a903fddf67f154b`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R78: pytest #7312

Report fingerprint: `923b89ff474b64e820bd8ae129c68f4eb12dd49c4928760922b66979de72a654`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R79: pytest #12189

Report fingerprint: `7fa56c62e854de53711859f7835bfe33a1ad614c72935a0232d2d51399139eda`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R80: pytest #12197

Report fingerprint: `4997ca5bead769c8d4b014866a3a8115f80f208c9bcad94d8ec926cd1ccd050a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R81: pytest #12201

Report fingerprint: `18330fe041ffbca692fff915e1dadb97766cd1bed05364c2a141e94bf5c2a8e8`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R82: pytest #12224

Report fingerprint: `686be5d8b542b7c7c5e1687f2c1881d368a9c09588d97a0c19054eb909a79373`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R83: pytest #7312

Report fingerprint: `d572c4d61c01cbe07e485b418992fa7d181fb165f83dd22f748c621e4ac3c6f2`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R84: pytest #12228

Report fingerprint: `e506f595601d49d8a64262d7cc33913adab88b21b852c390dcf9c6eb1065394b`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R85: pytest #12189

Report fingerprint: `f15f7cd91a0d98d98dbd266d65518540f81a6ea9d3b2d2d1d2cff232ec733fbd`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R86: pytest #12224

Report fingerprint: `fa7c63b98208a7cb823cc7544e0d89fc2d82ddb5994170f938fff91f40b654f5`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R87: pytest #12203

Report fingerprint: `83f7ff9caef3f33f8dfa85b65cb19ffd24eefa78122bf71348aaac6f1d44b908`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R88: pytest #12231

Report fingerprint: `f3725452c14fe746affef36465fa1e9dd9c7b9a12b0ed00535f1a3f528e4f938`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/3617ef1c79d686a42ce645b0e28dda824a74e715/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R89: pytest #12231

Report fingerprint: `0800a33ece6c70c1abd19d3d940437c3f02d88e9a3c369af2233d18c8dc86bfc`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/3617ef1c79d686a42ce645b0e28dda824a74e715/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R90: pytest #12219

Report fingerprint: `68b8b05e645066c4f8920c3da1037b4723417dc9826427ff839bbb43ad2b89ca`

Thanks for sharing this issue.
- Earlier issue #4064 may be relevant: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation. [C1]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

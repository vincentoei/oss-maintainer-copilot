# Issue #16 fresh blinded reply review

Rate useful (2), partly useful (1), or not useful (0). Preserve verbatim reasons. Review semantic support, unsupported claims or presuppositions, redundant requests, relationships and abstentions. Do not consult the separate identity key or transfer old ratings.

## R01: pytest #12189

Report fingerprint: `1b5ad8baeaedfce2d32ad3a31cb650d65f611d4a38b22b8f0d7f8e3d446fbd25`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R02: pytest #12146

Report fingerprint: `19200950e600fdb7220121881891a9c2d2853d24776693bf041d1a7b13050617`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R03: pytest #12072

Report fingerprint: `a4215b1251774dd8d72a6aa88fae2398fbe38c2a5bf5dfbc4ecc9aaf101a0042`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R04: pytest #12224

Report fingerprint: `a9cf4d0259695a6dbc22e7dabe1d49260178685e7f9d940baf23a8f481be4f0a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R05: pytest #12053

Report fingerprint: `8b9c6c592a9034ff93d975ff5306feb88a37ebc1410916d79cdfd7e49ffca316`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R06: pytest #10156

Report fingerprint: `46b8644df73ebaa307b4f9c180c44661a5147ca8a8dd4dde4645a3ff372fb164`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R07: pytest #12079

Report fingerprint: `cded7237b6ff3e2f2f92f931818272e08264516768e777b919a038dcfc414916`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R08: pytest #12216

Report fingerprint: `20ea0eb99e876f1dc6c11a4e4fc77f40ae3d926637a3dbbc50a943f6a3241185`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R09: pytest #12197

Report fingerprint: `9859fd08582c68794cfbf6ff5c5fc2b7326f52e38c61c17822280ed9c1724747`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R10: pytest #12197

Report fingerprint: `dfe461c63d7df549529a74693fc47103887facd3f9287f65ad77ce99b81c70af`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R11: pytest #12081

Report fingerprint: `e994d32cb825175e60e2d70ea1834fcdd55e65b6b629cc1a1176b9a678ae92d2`

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

## R12: pytest #12216

Report fingerprint: `cda50016a83053ce40fe859d1721447acf37f91c33e56f616b6272148feb1759`

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R13: pytest #12228

Report fingerprint: `c0ef535f86a4ec04fb88ea27b93851acd8797fd3e005ec27046b8f229b79c720`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R14: pytest #10156

Report fingerprint: `46447178d4cac37a9eece480032705388fb7178e8a8881283adc5d2b1d6d4656`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R15: pytest #12146

Report fingerprint: `275dbec5ed0d9a01ab9ef47c0b584239353d527cea049611240a2df4fb2c9a1b`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R16: pytest #10156

Report fingerprint: `0a4be34768aea316438c9025fc9ddf413f74ee6958cd4e67a4e25dab96f37b02`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R17: pytest #12201

Report fingerprint: `d5211b5ea45c562deaeb39747b73397af11684ad6df9452902500e365b85386e`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R18: pytest #12204

Report fingerprint: `86f585ef06ca143e3de09d8a0eb872266271226d659a584774a055ee4def6dd1`

Thanks for sharing this issue.
- The opening contains conflicting version evidence (pytest: 8.1.1 / 8.0.0; pluggy: 1.4.0 / 1.3.0). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12204): Submitted issue under review: investigative follow-up
  Passage: pytest    8.1.1
pytest-8.0.0
pluggy    1.4.0
pluggy-1.3.0

Rating / verbatim reason / semantic notes: pending

## R19: pytest #12219

Report fingerprint: `12cceb47d767d8bb9a775bc6cf57a9103ba40c97ad823f9459c8a7fda3971c84`

Thanks for sharing this issue.
- Earlier issue #4064 may be relevant: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation. [C1]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R20: pytest #12228

Report fingerprint: `9cb46668dc02dc9636e3fe6c54dcda3599977deb96a11e03bd1a0f20a17b594e`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R21: pytest #7312

Report fingerprint: `ff83a9e5175f1f0dba85a50be8f5bc14ed50063a36e97844ac1d9736f9761089`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R22: pytest #12079

Report fingerprint: `cd48165f2083814b7af6d2851b5b5d1be12ea3e049fa32dd8d30d28fe3294e3c`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]
- Earlier issue #11871 may be relevant: Both concern reading test-selection arguments from a file. This report: "… file, and run selected subsets of it using `pytest`"; earlier: "…irs`, to compliment the positional `file_or_dir` argument.". the same failure or request is not established. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R23: pytest #12053

Report fingerprint: `472a78a6f34dc68f0c11d2efbe5ce777853a20c61198d1633d75a68e6768d709`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R24: pytest #12072

Report fingerprint: `96877e7a45f958c212f70182b4c8a6a6735ab14de2d93bd5f2a3757733e52b9a`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R25: pytest #12224

Report fingerprint: `f67c1022ef67becdddeaae8fafc14af7f5ab2e84af6b9a2cb0781284d9bcbac5`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R26: pytest #12053

Report fingerprint: `3f7df024974731257a8fedad3caef4a150444c140d700636b03ac5f155c7697d`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R27: pytest #12201

Report fingerprint: `49d4a030bbf335f309fbb1633b03243c804c4bd98e9b00e0c60dcdd20f68c096`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R28: pytest #12116

Report fingerprint: `da7facdc30dd7d5d9ab5bf443d21e771cd4e7135ff58bf2446698028bd783ba0`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R29: pytest #12083

Report fingerprint: `f2fb5c1cfa570faf68e2b0da1be1d5ecea3bb2fd6867b23a2eab11083a5f42cb`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R30: pytest #12204

Report fingerprint: `a0f388563fe554b4a81b5504a3c4c99830695c9777f962d3f61856d5a84a07c0`

Thanks for sharing this issue.
- The opening contains conflicting version evidence (pytest: 8.1.1 / 8.0.0; pluggy: 1.4.0 / 1.3.0). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12204): Submitted issue under review: investigative follow-up
  Passage: pytest    8.1.1
pytest-8.0.0
pluggy    1.4.0
pluggy-1.3.0

Rating / verbatim reason / semantic notes: pending

## R31: pytest #12203

Report fingerprint: `7b8911bf58f754d6488897f7be59846b6878e06b2aeb4ee86ed0882b21e7db04`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R32: pytest #12189

Report fingerprint: `0cf258e482ad8e5bc55623e8cdc4d7be9b50adfc67eafba5738ecdbe75f0f0eb`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R33: pytest #12201

Report fingerprint: `4dcee36261781a3f20b44a2d848d6bef57350a5bb969418df993facd86642631`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R34: pytest #12219

Report fingerprint: `7b0cd1e569da48285cc12821ad8b600eebea1732de2d7c825526122aadd3813f`

Thanks for sharing this issue.
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R35: pytest #12203

Report fingerprint: `1d2a458f25e5bc85a4d24d556d885fa8ba9a81667f30954ee3037c9cdd756b6b`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R36: pytest #12223

Report fingerprint: `e6479d3a73009a2a20b9cc8a44c2dcbeb580ea111fd858332643eed131dfeb85`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R37: pytest #12223

Report fingerprint: `0acbfb95fa2d84aae696edc5b367bf4d45bef6043d3a2ed81c8639103358e859`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R38: pytest #7312

Report fingerprint: `a576ce9d2b14353f277aaedaffa1d136c93e76d4460d8dd2a99144d9d5359c43`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R39: pytest #12223

Report fingerprint: `402baad3a81fcf62d7ffaaf76613e2193ae23bbc1c7e9ab43909ae598a12742d`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R40: pytest #12203

Report fingerprint: `0432fb3a621b200523762de54167e37f7eeeb9753862fdccbb35b8291ae9cb7b`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R41: pytest #12072

Report fingerprint: `9ef06c8acbb6720d2835c9e8ba1e6653d769e34b51694f41a522340df0679a1f`

Thanks for sharing this issue.
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R42: pytest #12116

Report fingerprint: `42865216abe123df158a3524e257a126042f212fb57136c5167cab19d270db0a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R43: pytest #12083

Report fingerprint: `6ae104a459c84b8c73255aea3ef9920f188c0f2979086b9585c7045d68fe57e6`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R44: pytest #12226

Report fingerprint: `ab0e1382a374dd2a33c60714a9446ff17b266486696c61279187ecee702b7d5f`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R45: pytest #12224

Report fingerprint: `21d4ba70620050f3335bf26813a93d36269a75699b455282e8877da1205db580`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R46: pytest #12226

Report fingerprint: `9c557e0eb02fb13537794d6b0c0b7bed5b389b5324d6d04531fe5702ecc8da15`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R47: pytest #12204

Report fingerprint: `7d235b5fc3859537ad64e9e642a1793f93fa85a983e071f3782b312c495be4e4`

Thanks for sharing this issue.
- The opening contains conflicting version evidence (pytest: 8.1.1 / 8.0.0; pluggy: 1.4.0 / 1.3.0). Could you confirm which pytest/pluggy versions produced the output using that run's environment? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12204): Submitted issue under review: investigative follow-up
  Passage: pytest    8.1.1
pytest-8.0.0
pluggy    1.4.0
pluggy-1.3.0

Rating / verbatim reason / semantic notes: pending

## R48: pytest #12081

Report fingerprint: `cdb27815a2edde2b3b10ce5b4497a67f255ce601124b3ed4bf6929e45c4585d6`

Thanks for sharing this issue.
- Earlier issue #3448 may be relevant: Both concern readouterr consuming captured output. This report: "…turing via readouterr() consume stdout, meaning that logs are no longer available in the "Captured s…"; earlier: "…uterr()` in a test also resets what pytest displays in case of failed tests.". This opening names copyouterr; compare its proposed behavior with the earlier readouterr report. [C1]
- pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/3448): pytest issue #3448: capture: keep all output for "Captured stdout call" etc
- [C2](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110): pytest documentation: capture
  Passage: The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is

Rating / verbatim reason / semantic notes: pending

## R49: pytest #12081

Report fingerprint: `98dc0d95d0e4f034ae73727f37303d27d2ffa33cd7f91c480a511a6fb88f910b`

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

## R50: pytest #12219

Report fingerprint: `5c2945f45354128fa112d4fa52fda36a2a8dceb4ec52017ed9f2e1d97ad00a2b`

Thanks for sharing this issue.
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C2](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R51: pytest #12216

Report fingerprint: `06b4b0e3fef056fb733ce3f6213d24dea6c330ee176b779ed7157ef2c59f1a11`

Thanks for sharing this issue. I cannot substantiate a specific reply from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R52: pytest #12226

Report fingerprint: `cca3c98e5b684c29b877f5b02b5ad962a1903038cea5baecc491c7596d589650`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R53: pytest #7312

Report fingerprint: `806d22cee79f03fe0fc61457bb79f22541e1049566c85bc7af1b05281deb1256`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R54: pytest #12189

Report fingerprint: `6643754b83743ec04d530cd2a4009054554dc3947e41f607b1e2ca464902c5da`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R55: pytest #12079

Report fingerprint: `3a839558a25b888206a594a08b189bd55f6b2457b3b7c47aa77697d868b56ca0`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R56: pytest #12146

Report fingerprint: `4122c36fd4281cfb70810895f181f1bd9150321512e1ce4038a595553ae8cccd`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R57: pytest #12083

Report fingerprint: `dc7be5828b9027c3c9d6c0ce0648c4942cc5f66e0d69c7be7d3dbb7620208fe0`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R58: pytest #12228

Report fingerprint: `ed26ed083ba310bf91bf747c11ba5c3ce2db215fc1a0928e5f277825eb980ef4`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R59: pytest #12197

Report fingerprint: `cd89413d715a2dd625f0e0becf6cc330922b070119287418f7c55b5e58b2acd0`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R60: pytest #12116

Report fingerprint: `71cf424c648ca2d9623c61197306f00ec6346a33e65bd0e48bfd5922b1e5387e`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

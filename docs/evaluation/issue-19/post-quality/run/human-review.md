# Issue #19 fresh blinded reply review

Rate useful (2), partly useful (1), or not useful (0). Preserve verbatim reasons. Review semantic support, unsupported claims or presuppositions, redundant requests, relationships and abstentions. Do not consult the separate identity key or transfer old ratings.

## R01: pytest #12223

Report fingerprint: `cd580040bf17f3e42b26566db4bdb0424fe613279cf4b057b81ce10fbe3b54b0`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R02: pytest #12308

Report fingerprint: `314c8f802b4634cbee832e55eaaf0dd8cfb1647a41114e30cd1700e8db386ae0`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R03: pytest #12328

Report fingerprint: `3ffebfc90f2c269cc767cef9a11b87607c8f591c1b8681d565f71bc1cf31b53b`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R04: pytest #12281

Report fingerprint: `ed427dfb76ac1f5dc002aeae08b2dc3fd8a2de35abbea2e04f7de7402dabe23f`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R05: pytest #12263

Report fingerprint: `12d38b0f5aafc609f46ee05180cd90dc202c9b22f9af3de47f765c080b764c0a`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R06: pytest #12197

Report fingerprint: `3614351e2dc60f0a2b14e0cd5399cb7f7df3d414738d00b80f490fb20f48edb3`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R07: pytest #12255

Report fingerprint: `5ffd0b04e34e4d53e590666503f3e95a44e710471317b5508b63e4681b576fae`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1a332802ff8afde3c899df46901f00bde523e4e3/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R08: pytest #12116

Report fingerprint: `b385100b878a3c106d2b933fc7404b6856f78f97f0b7bb4103c03567ee77ec78`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R09: pytest #12081

Report fingerprint: `ef998dba4cd29eb8fbe1c79e4cabb81975ac214fd9263d2f7b9c7952c0924d8d`

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

Report fingerprint: `85ac27d081269cb5cb6657f191e6e92069509c2f54c4f6b351b28631ac1ea798`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R11: pytest #12303

Report fingerprint: `d6f5774af268c2523dee467dde50fea4b84b7a5074cb0a3cd8e5fad834a2526d`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R12: pytest #12366

Report fingerprint: `23b488e0c8ba06f94bd8898ae017bbd0d33b8f30a40fbe79ad6ffd6656f79878`

Thanks for sharing this issue.
- Could you add the solution you would like? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L16): pytest feature report template: proposed solution
- [C2](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R13: pytest #12323

Report fingerprint: `57e678526cd7addefec0f936d0f507a2883f01bcaeb1c8c7a968a5408a86eb64`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ebe2e8eac9db5a662cf60c9058e0c5ba480d3ad0/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

Rating / verbatim reason / semantic notes: pending

## R14: pytest #12249

Report fingerprint: `a80c739a3e387ba72726aee8c3962665e69f247c7426e5804a7909e847147160`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R15: pytest #12312

Report fingerprint: `ae46a051fcf3174b84dfdd6dfd98fa20bf53bf2dca9385287a3be5db5e6f7847`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R16: pytest #12300

Report fingerprint: `81b29420d561cec56365d4f74d5149e5e07f63dcd4372fe2ed311c74a662e84d`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R17: pytest #12305

Report fingerprint: `bd143b1d7f8168ee2ce8bed5dbf76cfedabb525933ad1dad41b8b1aaaeaf6356`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R18: pytest #12290

Report fingerprint: `5cfb63ae19c5e9a9f24c514afc057913c8930cd8a8425fe22210d4c48a248ca0`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R19: pytest #12328

Report fingerprint: `b4331abbd3557af473da0cfc943fbbfc0f96edf8195fd479ed30ade1828fb3bb`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R20: pytest #12189

Report fingerprint: `b66c402162c1cc4c09c9748c56e97eb63bb9e3cb2bdfb3ed1f7bd3655ded671d`

Thanks for sharing this issue.
- Could you add your operating system and release? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4e3dd21506a9e543c04c63ebff966a9b604d2b9e/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R21: pytest #12307

Report fingerprint: `bd797855be55bf971663dd160305f8b92796efec0eefadc56da0e3c43f42028b`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R22: pytest #12146

Report fingerprint: `22f271a77072fb9d3d99879cb9aed57009a648e796e3c61bba800be2c21279e6`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R23: pytest #12278

Report fingerprint: `7579e90718ce51d4d7dc9fe6140ba43e7a05b2d60d111f62aa50b5a00869ce6b`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R24: pytest #12079

Report fingerprint: `abcff038b6677d400182eee1d044d838dfc344dc1cc04ad40b5e44d8bf2c7947`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]
- Earlier issue #11871 may be relevant: Both concern reading test-selection arguments from a file. This report: "… file, and run selected subsets of it using `pytest`"; earlier: "…irs`, to compliment the positional `file_or_dir` argument.". the same failure or request is not established. [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R25: pytest #12079

Report fingerprint: `4203de4b0f31a7e8d2f2611769cc611d7ff1257b86b25f77924865215e912f4d`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R26: pytest #12287

Report fingerprint: `12eca3172269f2ec732d869cbc9765605e4d1075dcc96ee81cd7ab9d66895725`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R27: pytest #12226

Report fingerprint: `d639e72f508e0d13b0e48c11097a92ffcbf415769289d34907cab9746d133fb9`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R28: pytest #12242

Report fingerprint: `95c2ea8d6423c0480e4dd2223dc7cd7626b99f47419d9557e8fd074d5a596a40`

Thanks for sharing this issue.
- Could you add your operating system and release? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R29: pytest #12377

Report fingerprint: `9142da5b58e05c88f8d404bab9c44d3372bb3eee571bf1d8e175f9e378f1b5d4`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R30: pytest #12290

Report fingerprint: `88f9fcc0d1ddd4fad1c1ea626ee64f3f185306b7f04f297050c7fcee4b798776`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R31: pytest #12255

Report fingerprint: `e36695ec77b09e5b47cef0ccfffd21653cbf17b76b96a79fcabfd3759f66e97b`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1a332802ff8afde3c899df46901f00bde523e4e3/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R32: pytest #12363

Report fingerprint: `415662ce36b36df461ea62d2d8011d0dd96d2420a0b769ff0704a8cad88930b1`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R33: pytest #12201

Report fingerprint: `34a072372c2abfdf0c5252c2d46cc6731606720be7d3bdde67a021c70eff394c`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R34: pytest #12307

Report fingerprint: `4a4c7438264b3c9d64919b39d317c922102bda52152b66dc4bc09a21cf9cef58`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R35: pytest #12308

Report fingerprint: `ff523ecf6361e08849a574225d5451768b0a4f8bea2164ea323c1b8445c7735d`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R36: pytest #12223

Report fingerprint: `30831a66a3ba21353ef23757d8181a4c31c6f6b8ffcca08237b6dd94080ed383`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R37: pytest #12081

Report fingerprint: `68305e49fc88bb542fdbc1b303cc4c1a54590b830e4e696a62368efcf83b28b2`

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

Report fingerprint: `27299ff91d89984a1c1ae32a2eb22270c4c32106b01b20ea4e5d1bf5cf22cc40`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C4](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R39: pytest #12228

Report fingerprint: `01f0b6b754b0a41a18f1600af7f395d3236768e51039afaa89e5420634cc2cde`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R40: pytest #12351

Report fingerprint: `b7d90a2cbedaf1fb5e0827ebee3343697b40be80b769919b84606c1b4fefc135`

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

Report fingerprint: `9400b8254175f7a5a5c33c193775ac9125c171a9e970acdce50e74f077f4f4fc`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R42: pytest #12303

Report fingerprint: `4a97d3f5675e674dd8358706553dc0e0b5822a7063b51c0dbdc6355b98fb3183`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R43: pytest #12360

Report fingerprint: `ddc2f85304bad4a6ba2d119341fa1e993df9d53c1326bacf65ab560490f06768`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R44: pytest #12146

Report fingerprint: `2f13033b95d03182da32f2c2fde803c9b388a16e87549b28cf5d283cbd787560`

Thanks for sharing this issue.
- The supplied scenarios use different pytest versions (8.1.1 / 7.4.4). Could you compare both scenarios using the same pytest version and identical tuple values, including their order, changing only how the values are constructed? Please include fixture setup/teardown output from both runs. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/12146): Submitted issue under review: investigative follow-up
  Passage: pytest-8.1.1
pytest-7.4.4
pytest         8.1.1

Rating / verbatim reason / semantic notes: pending

## R45: pytest #12298

Report fingerprint: `ab52820d52e6ef7176ecd986280a9c2280109991e07c1e35ccde5819123050ce`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R46: pytest #12328

Report fingerprint: `0b3fa383b2308c9318f087b485cae66a6361c8c8f32f25efbf82d770aca512d4`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R47: pytest #12053

Report fingerprint: `b8ddae06ce1e86a86489879cbbe078b5d4542a0238a2667c02b35c0afcd84d01`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R48: pytest #12201

Report fingerprint: `75070cb409358a67ece43a0bf8cc708dc3b3f0cad94057b5e3b5742c6b893378`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R49: pytest #12298

Report fingerprint: `d4566d6ed2d35c50fc46ccfb6795f27328e069888a84fd3c0c33a70944456bab`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R50: pytest #12219

Report fingerprint: `263a68a1adbe60de171abcc4a277082135859e1b41e5ce1c8a381d89ac7ce37b`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C5]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C4](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C5](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R51: pytest #12053

Report fingerprint: `1ac57953e29ad93f551e004dfd9bba6d51a72491a37b2bba250754ba83eff958`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R52: pytest #12083

Report fingerprint: `a3c84ff9a63dfa8b08d6ed57a7be81482e7fd52e4935a0cead28802d8faac5b6`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R53: pytest #12079

Report fingerprint: `5cf181dbabd99b9edb010295e51e3beb52f28aa1072421fe113e368ae5eaafa2`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions
- [C2](https://github.com/pytest-dev/pytest/issues/11871): pytest issue #11871: Proposing a new flag, `--list-of-files-or-dirs`, to compliment the positional `file_or_dir` argument

Rating / verbatim reason / semantic notes: pending

## R54: pytest #12249

Report fingerprint: `8170204603535705dceb660bb484237974f22bcf3ec0f128697b0084e813908c`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R55: pytest #12351

Report fingerprint: `835f00b9abb4ec122d48f6a76110b91d9000bcf1f14dfde473e10484b4fccfdc`

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

Report fingerprint: `e7f59f8a181ea890b65522a85777795bc0ce34b9428bf2f00bf485033eec2c29`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R57: pytest #12204

Report fingerprint: `aaca2abe93b2211dbe03dc64a0d1096aefa0a441375d60e8221649a7ac807386`

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

Report fingerprint: `f2528bbea089467cdfefe66a01ae190fcd1f0a3a85a1d780ad76806e31b20086`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5f6e825a2687f6bb8bc437e67a59c0a92fb16c06/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5f6e825a2687f6bb8bc437e67a59c0a92fb16c06/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R59: pytest #12223

Report fingerprint: `cab47b32d7439127544032fe0bf8e421cec71493e16b2ff196ae06bd00850ea0`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R60: pytest #12224

Report fingerprint: `498cd65bf74757af992e32a800ad1f768abe557e8615067d0d37d17c45ebe019`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R61: pytest #12352

Report fingerprint: `e8b46bd4381c1407338f737106c3106a0af32dcb7ca797ac1d958475890c3d2b`

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

Report fingerprint: `ca397d9c2dfa3b3932e107c6d6abb9dded392bd5a4712f602428cd891aa0c980`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5f6e825a2687f6bb8bc437e67a59c0a92fb16c06/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5f6e825a2687f6bb8bc437e67a59c0a92fb16c06/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R63: pytest #12197

Report fingerprint: `aca42a3dccc755055540bf7c82098b9d777c5f00dc85d430a59f193a08e500ea`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R64: pytest #12357

Report fingerprint: `3524dff99bcfc27cd8c293dd221d17e380ed9866f7b13ef6a0e20cb5bfacc092`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R65: pytest #12290

Report fingerprint: `6f913c6203a4560ab96809ee857fc71a71f3864d72f180b2006fab85f32abb56`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/84e59af8c829de659efb339d5a9c7cec98eee719/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R66: pytest #12255

Report fingerprint: `418be4cf61ea3844df531dca8b94eeddd41b2f876adc99a9995162df4a39e2e1`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1a332802ff8afde3c899df46901f00bde523e4e3/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R67: pytest #12300

Report fingerprint: `b8835a7b0a8d1f7fdaa245f5d166d7565009beb3d70178887118073b8c189b6d`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R68: pytest #10156

Report fingerprint: `84a41f99170534869afd6985b713f03ef2d30943d094da3567caea4a12e8158e`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R69: pytest #12298

Report fingerprint: `89b0725e6c56ca2e0a6dff3d878aae15217137b688eba8d5382dff3f579c176d`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R70: pytest #12224

Report fingerprint: `e8056740ba29af97bfad2021bb0411eebf2997b32b7a9f63f041b9ff78623fb8`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R71: pytest #12189

Report fingerprint: `c1296b9f626a9d76e8a1e5da6d8ffb1014aac33a36461cced1d32ed6a6487636`

Thanks for sharing this issue.
- Could you add your operating system and release? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4e3dd21506a9e543c04c63ebff966a9b604d2b9e/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R72: pytest #12083

Report fingerprint: `13d852b6c207ef130b1feb53717461f002779f4b0dcc781a4a5b32d857d021fc`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R73: pytest #12366

Report fingerprint: `56bc830ee7a8566a82441b98306fff2bee4e2ae2f8972955c8bbbf980589ee2d`

Thanks for sharing this issue.
- Could you add the solution you would like? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L16): pytest feature report template: proposed solution
- [C2](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R74: pytest #12376

Report fingerprint: `75a4b0cc9d8c29aa3d0a4a1ad2fb5af1cee03b9acce85bbef996bb7ee74ae98e`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R75: pytest #12300

Report fingerprint: `1403704e8421eb00ddaeb1cd08b8d8c38878088d56864d8f875dcb4d93016fe5`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/d49f1fc4dbf9e04da016335d9e82527423d9ad1f/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R76: pytest #12352

Report fingerprint: `986931a603740ec902ed668d12ad93d19d418e47553a416b6112257d61d37a2e`

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

Report fingerprint: `8af9af04310a635ea7af55500e6632ee2010182d89b2fe172150bfb207818287`

Thanks for sharing this issue.
- pytest documents that capture fixtures let tests access stdout and stderr created during execution. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/doc/en/how-to/capture-stdout-stderr.rst#L109-L110): pytest documentation: capture
  Passage: The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures allow access to stdout/stderr output created during test execution.  Here is

Rating / verbatim reason / semantic notes: pending

## R78: pytest #12367

Report fingerprint: `1bf49a527db972183f3b57c457bd2c3710258a28fd2ce89b841c68cdc77bff7a`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R79: pytest #12281

Report fingerprint: `29557fbeb443ff82c444484d8b6809d453648120d7eae665aa3f5c99d8677b94`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R80: pytest #12293

Report fingerprint: `9015e5a0e1aab62fd7cd114803cc5cbed0d09d3a4ece020702a30ce819139542`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R81: pytest #12360

Report fingerprint: `b65f95c8d03115cb2a290247a477769b4d48ae1673456c235da36385cf179579`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R82: pytest #12371

Report fingerprint: `ebfe22c6b86092ac1f4201c02a5b9949385427f542f311c87cf60ec1fe58eb52`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R83: pytest #12231

Report fingerprint: `f0f148325d6762b1448bffe9ef22f372fbd2f9c5d9476656ee979a422ced721c`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R84: pytest #12116

Report fingerprint: `984c803b5b37a0012559141502cc5f1686a2d837818621725449a9c29a4c7517`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R85: pytest #12053

Report fingerprint: `4652b7f3adcc1cb1d650eaac96feca3f4e70fe47cc2bd530cafd5d17b1009582`

Thanks for sharing this issue.
- Earlier issue #8655 may be relevant: Both concern custom debugger selection with --pdbcls. This report: "… `--pdb` together with `--pdbcls=IPython.terminal.debugger:TerminalPdb`.  Unfortunately, `pytest --p…"; earlier: "The [help string for --pdbcls](https://github.com/pytest-dev/pytest/blob/f28421cc7068b13ba63c1f60cc2…". This requests a configuration setting; the earlier issue concerns command-line help. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/8655): pytest issue #8655: Help text is misleading about the behavior of --pdb

Rating / verbatim reason / semantic notes: pending

## R86: pytest #12287

Report fingerprint: `7653eb7c18ce1ebaac90ee2b24e8bbf3ae8a8cd3ddb49c628e24beb0456ab933`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R87: pytest #12377

Report fingerprint: `768e7b8eaf7dc9803b296937fb51b56566aff199ddb2e2c27f9b8164b4f62e20`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R88: pytest #12204

Report fingerprint: `5decd7bf6a6f3b59b6fd0b766855d2ab1d2608473bbd17d462264fd78d3facc2`

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

Report fingerprint: `7a692986fa8771a1bcb424ed14582b5249409b8a6eb0a5ed87745ca914aa71d3`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R90: pytest #12312

Report fingerprint: `0b1e3d453910f25433ead268af1444a054a311f08fd78838f3d9652c6b3a3810`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R91: pytest #12083

Report fingerprint: `a97470b820f6240f737c39df9a4b7853deed0348ea82038b031f13bc85b49e06`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R92: pytest #12231

Report fingerprint: `bc1cf2905a0c0d25218ed2003a64572f0d574a0428226787df48a8e88d9f72ee`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R93: pytest #12197

Report fingerprint: `2199fec53b365932102c4c1b9b414b57b0f51d57b3f32cdee77c4dcaf3606c51`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/74f05648d5ea9e69d75f27a77972756ee32f6730/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R94: pytest #12219

Report fingerprint: `3007db2ab5d77258c73d469961e42def0bc4b53c01148c2ede7da2bc28d612e4`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C5]
- Earlier issue #4064 may be relevant: Both concern module setup/teardown hooks. This report: "…test `setUpModule` and `tearDownModule`."; earlier: "…ay that setUpModule and tearDownModule are not supported:". This reports hooks not running; the earlier issue questions the documentation. [C4]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C4](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C5](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R95: pytest #12371

Report fingerprint: `29d37b6fb649a92fba91e66dfb128c88f601837ed72d24e22658b4a260cf53d7`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R96: pytest #7312

Report fingerprint: `2e83c0309af93a525d235a85a1e8142a3801dd8d8fde898294a20af37211a68d`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R97: pytest #12072

Report fingerprint: `5102baeb8fe2f8175649affaf393c8a450ce00bfef7c9806b451dd9f22c8f38f`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C4](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R98: pytest #12363

Report fingerprint: `21bf80a8cfd69182d59792d4be35d965d5535458c23d03cd2cb25dc08a15cff7`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R99: pytest #12357

Report fingerprint: `511f8ea1659259ec47d9fece9d5f6746ba5d10213d977a7912b5e17a3fa1b5a5`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R100: pytest #12263

Report fingerprint: `630d7e065219c6107cdda64f732db2bc4bbc5965f14a37c133b24c5ac870908a`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R101: pytest #12323

Report fingerprint: `bdfff9db794ea52462491cd6212eb854bda034d00fea63746999160e1f768400`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ebe2e8eac9db5a662cf60c9058e0c5ba480d3ad0/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

Rating / verbatim reason / semantic notes: pending

## R102: pytest #12376

Report fingerprint: `a7d76c873a588c18020fd04da9e5596eb04009e4103bd0ce77635969033730a9`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R103: pytest #12116

Report fingerprint: `81f384624e7fcccf33b48bea4ff1c051823ec4a0f90651f97453883b2cf886c8`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R104: pytest #12281

Report fingerprint: `b86dcc401a8ca1c0cb3dae1cafce584f52f896e8f21c26593f54fd7c8fc20589`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R105: pytest #12367

Report fingerprint: `50d9b3e3659b3cf9626ad55ef61e8e7739784bed847b18aab27ae2e84eaf27bb`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R106: pytest #12226

Report fingerprint: `b5ebaa56865e931843de7fe13244cd0d574b2c3d91ab8d608cfeb721f875a203`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R107: pytest #12242

Report fingerprint: `aada2c1388d76b9d79990418d8e5e968cc731fb5a82d4611cdc7ab70c3257e41`

Thanks for sharing this issue.
- Could you add your operating system and release? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R108: pytest #12216

Report fingerprint: `714b8580827c3630b6ac2f77a72cc9b3cab0c4f040dcfd578f7daa921653bb38`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5f6e825a2687f6bb8bc437e67a59c0a92fb16c06/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5f6e825a2687f6bb8bc437e67a59c0a92fb16c06/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R109: pytest #12072

Report fingerprint: `e1c05f5cdcf052421b45f7c39af6c3e201f417038a0f319b07b8fce496c55824`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]
- Earlier issue #12066 may be relevant: Both concern the call_runtest_hook import failure. This report: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/travis/miniconda/en…"; earlier: "ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner' (/home/runner/miniconda3/e…". the same failure or request is not established. [C4]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/0951cbc6e4880ee7dfc9b7e56948d83ee086e74b/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C4](https://github.com/pytest-dev/pytest/issues/12066): pytest issue #12066: ImportError: cannot import name 'call_runtest_hook' from '_pytest.runner'

Rating / verbatim reason / semantic notes: pending

## R110: pytest #12371

Report fingerprint: `b068fdcdd307161d94aba3ed4a0b714b2f0cf767921ed3188e092d80963587c0`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R111: pytest #12224

Report fingerprint: `a89e7ca021e8c9ab77849b511b430c54161a3d1f551c1a63f8f59781a0654c07`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R112: pytest #12201

Report fingerprint: `b067026cc0b0cdc8b1b0faa4742ac5a7a3d9d4de25d1ca66e4b6a8de7d3bb7e9`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R113: pytest #12219

Report fingerprint: `9842af823e91e8dbe52257462526fbccb4210e32ff4f8db94935aa6de6281611`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C5]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example
- [C4](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?
- [C5](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up
  Passage: Interestingly, the hook does seem to be honored in a minimized example.

Rating / verbatim reason / semantic notes: pending

## R114: pytest #12357

Report fingerprint: `4045d82480b189429c2ed567b56f847002a58ebbdd6be1b4f01f6ff75322a4f9`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/cbf6bd9dd28d8464f7eebe32e51b398e2a5e3039/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R115: pytest #12303

Report fingerprint: `485098d1aa33d1101b44c7e8000ae4dc3e1c153950851c7b8a287b904cf03f72`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R116: pytest #12189

Report fingerprint: `9f3b0b9d1df06a1b6badb32bfa267f0882d34d3674d638700577c7b9e1c9c91a`

Thanks for sharing this issue.
- Could you add your operating system and release? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4e3dd21506a9e543c04c63ebff966a9b604d2b9e/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R117: pytest #12203

Report fingerprint: `f97b271e3a1afb069db27c0eeb06a172b0524982737d66263ef6f691467a8447`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R118: pytest #12293

Report fingerprint: `eaf9745c2d9d218a846d470fcf969d2f3659bb15122007f88a6638acef273d37`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R119: pytest #12377

Report fingerprint: `0312f53a6a0648a6afcc20a2bdcacc907f4417563d6c46104c0e3a4a05ed0db2`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R120: pytest #12273

Report fingerprint: `8e24f49b28cffa4a9a18ee119d863582b6d655d03d38a1c55b89dfca360d5e5a`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R121: pytest #12376

Report fingerprint: `f9f20d8de3c2d998b67c8f64b3e49488eba9f932e2a971c2d5a948e85ff1cd46`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R122: pytest #12228

Report fingerprint: `30ab00c2536f66e8fccc2c40ce8bc9a39dd2c7ccedc8d357d088e533e9e321f2`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R123: pytest #10156

Report fingerprint: `e0c190afd70afe137dd7c6fd18490c99ac48ba8831f5811d349e820285724b47`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R124: pytest #12278

Report fingerprint: `4809cb24b42ee4872d009103d281bf27fa3b5a39436e243619dd8e0f8c567ec4`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R125: pytest #12363

Report fingerprint: `e5064161705f50ef3b6f9fabd8754cd9bb3dfa6f1c7215d66236705ab7cd0c35`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R126: pytest #12366

Report fingerprint: `fc48e6bf1317115a3f4c5e0bae798a320370abe9555d6fdd6649397b615b7850`

Thanks for sharing this issue.
- Could you add the solution you would like? [C1]
- Could you add any workaround or alternative you have tried, or that there is none? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L16): pytest feature report template: proposed solution
- [C2](https://github.com/pytest-dev/pytest/blob/889d9b28d786c75b66f4d1acb80123bdb341639c/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R127: pytest #12305

Report fingerprint: `19386f2bd8b5cd44c54b20262133c13269b2a00cc6666a1bc3ec683ee014348e`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R128: pytest #12204

Report fingerprint: `58a6eead17c6d28862e7e72a6e25b40873b614e16b3ad617e7c2c12a229ab8c6`

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

Report fingerprint: `dd5ac3e8ac7b31dd473e6cbbcc1832562ede6c739fc040cb3c8567acb2f15533`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R130: pytest #12242

Report fingerprint: `9d3f12233855790696347648bd11cbe1719b6e7d9d20585f8c34ce48bba3f6f8`

Thanks for sharing this issue.
- Could you add your operating system and release? [C1]
- Could you add a minimal example, if possible? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C2](https://github.com/pytest-dev/pytest/blob/fafab1dbfd2414c2282b558f0c7af9a7ad0318ab/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R131: pytest #12367

Report fingerprint: `38b0d59b4e4325bb11d97ef85452c80924c7a8a1f1d0644d7efa9213563e8138`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R132: pytest #10156

Report fingerprint: `7fd421159a191fe3c960283c38a86b0d83cf113c0f9ef3f8176b375d0979ac81`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R133: pytest #12278

Report fingerprint: `e2a24b300df2973e935c9f4971e03afad5598af73a7d86241c6cc263fa99732d`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/da53e297807ddf85c74052b8ae32dc45404d1f63/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R134: pytest #12203

Report fingerprint: `f7e36f39823e0d4d8d4b37fe39337b7a1708d1b0d47dcc0fc52f32af429dc372`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/1f001cd1051a4ca4bef251d93e472e625578aaf7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R135: pytest #12287

Report fingerprint: `677bb739218a2339a39c74cb91400cdcb4f0437b7f38dd054a97ecceab1674e5`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R136: pytest #12273

Report fingerprint: `9bd3d0a09a5111af691551d9bd122f0d35294c5f6ef58e2cd5314a0f65792759`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R137: pytest #12273

Report fingerprint: `896f914622fbec4da051b4eb1a59ae011f12cb2fe8628d0b74ead9208e335788`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/b660596f614f7a67dcf5f6f863345600840df18e/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R138: pytest #7312

Report fingerprint: `a51c22cb573dc831d7dd1b54ce5fcb07a65f85779277b695648df93596e736f3`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R139: pytest #12226

Report fingerprint: `7ce954428360847277ad9adee976e17bad83eac4109bcc2adef2fa97057e7361`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R140: pytest #12231

Report fingerprint: `27eee979e41b0f8279296f205fc40a2f0d047268f445dc40db41204a664396cd`

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.

Evidence:


Rating / verbatim reason / semantic notes: pending

## R141: pytest #12249

Report fingerprint: `d800652cd352015db1aaf81dbae7f12278c55de88c1f8f831736d09d3c644d8d`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R142: pytest #12305

Report fingerprint: `6a2281034829fe76497547f86fe067efffabfe58349d5e79e253a97f08bb347e`

Thanks for sharing this issue.
- Could you add a minimal example, if possible? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R143: pytest #7312

Report fingerprint: `c9990e4c2ee52626d4e8b29bd7f003b294a54c09af5839eec6dd7b60f35753bf`

Thanks for sharing this issue.
- Earlier issue #349 may be relevant: Both concern fixture-derived parameter values. This report: "…t.mark.parametrize("x", parameters_fixture=my_fixture)"; earlier: "…est function is not the fixture _value_ but the fixture _function_.". This requests session-derived parameters; the earlier example passes fixture functions instead of values. [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/issues/349): pytest issue #349: Using fixtures in pytest.mark.parametrize

Rating / verbatim reason / semantic notes: pending

## R144: pytest #12323

Report fingerprint: `0201a373f265e1abf5cb744fd11f8492cd568c476c835de85a49ea6eb11e7027`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ebe2e8eac9db5a662cf60c9058e0c5ba480d3ad0/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

Rating / verbatim reason / semantic notes: pending

## R145: pytest #12228

Report fingerprint: `74fc0cc69f555706c5c700be9429a121f1f5489e79594fc3947498853f4dac1e`

Thanks for sharing this issue.
- Could you add any workaround or alternative you have tried, or that there is none? [C1]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/ad95d59d6158076768cccd0000b968cd691cb62a/.github/ISSUE_TEMPLATE/2_feature_request.md#L21): pytest feature report template: alternative solutions

Rating / verbatim reason / semantic notes: pending

## R146: pytest #12307

Report fingerprint: `7d6a72c065cf37cea09e804ae3f4db6d0f21c408d6e1467aec4056a418c75155`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/5af46f3d4e8264c50ffd635dbb395199670e70b7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

Rating / verbatim reason / semantic notes: pending

## R147: pytest #12263

Report fingerprint: `85a756b50984ff7e4ca15d92867d4e7bda5f4fb0557c57e60226115ae088d242`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/50d1e81713af75ab6d3608d2920ddf21bf53d765/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

## R148: pytest #12352

Report fingerprint: `7e2a90449fc1f88f1623986aeb70109f948ab80c30fa198ac9b6548c8febf975`

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

Report fingerprint: `0f8c840b97adcafd2d09f0cf290e255c3c39a1213d72fe7cb0bf1be5dbed607f`

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

Report fingerprint: `d4470591d17c3f14a7e2ff136838b08e77d1b5f08aeef3cccf745d737fca9a78`

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

Evidence:

- [C1](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output
- [C2](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions
- [C3](https://github.com/pytest-dev/pytest/blob/4080459f041f02c66356777001d18155d2796ee7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

Rating / verbatim reason / semantic notes: pending

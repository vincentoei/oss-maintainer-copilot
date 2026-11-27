# Method-hidden report review

Rate semantic type support, quote relevance, unsupported claims and reply usefulness (0/1/2). Preserve reasons. Do not consult the identity key or copy prior ratings.


## R01

Report fingerprint: `f11c31151cf2428da852ebad20d63503515ce28ce2ac00c733d4637fdb6763e5`

Process exit status

For the same failing test, pytest 8.2 exits with status 1 and pytest 8.3 exits with status 0. The summary reports the failure in both. Reinstalling 8.2 restores status 1.


Suggested type: type: regression

Quote: For the same failing test, pytest 8.2 exits with status 1 and pytest 8.3 exits with status 0. The summary reports the failure in both. Reinstalling 8.2 restores

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R02

Report fingerprint: `1206ec89853d7a08070a91ae9ec9658e379a0fd177a11a073e70c5c28688989e`

Captured traceback

A failing test raises ValueError with a message, but the displayed traceback attributes it to an unrelated test that passed. The problem occurs on both tested releases. Please show the traceback for the actual failing test.


Suggested type: type: bug

Quote: A failing test raises ValueError with a message, but the displayed traceback attributes it to an unrelated test that passed. The problem occurs on both tested r

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R03

Report fingerprint: `5bbe23005eca79df4377d0b8e64e64e314052411b731bb5c4806dabd5403a0e2`

Understanding a warning

All my tests pass, and the warning correctly describes a deprecated option I still use. Where can I configure pytest to hide this warning temporarily while I update my project?


Suggested type: type: question

Quote: All my tests pass, and the warning correctly describes a deprecated option I still use. Where can I configure pytest to hide this warning temporarily while I up

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R04

Report fingerprint: `41e8f7d9f043ace99dd65ff9506fa5c9f3577f88deae4c65789534f0ce879627`

Synthetic application input: short. Inspect the exact title/body in [integration inputs](../integration-inputs.json). The long form adds observation lines to the same exit-status opening, not a new quality case.


Suggested type: type: bug

Quote: A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R05

Report fingerprint: `d50389617af062a9ca3a88e679f84d51c567688071f09358a391b7b0cc0246e1`

Session cleanup

The same plugin and test suite close their temporary directory at session end with pytest 8.2. After upgrading to 8.3, the cleanup callback is never called. Rolling back restores the callback.


Suggested type: type: bug

Quote: The same plugin and test suite close their temporary directory at session end with pytest 8.2. After upgrading to 8.3, the cleanup callback is never called. Rol

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

- [C1](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example


Ratings / reviewer / reasons: pending


## R06

Report fingerprint: `9ab6b84383183cace09f53777de37953bb8af98d8cc4ff740cb6b2e79d2a20f4`

Synthetic application input: short. Inspect the exact title/body in [integration inputs](../integration-inputs.json). The long form adds observation lines to the same exit-status opening, not a new quality case.


Suggested type: type: bug

Quote: A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R07

Report fingerprint: `669c1c01ad648d628635d55e28e60dd8a1f1359624246cd093920f451aa5b1b4`

Notes for later

I saved an incomplete note about a test run. I no longer have the output, have not checked whether anything failed, and have not decided whether I need help or want anything changed.


Suggested type: type: question

Quote: I saved an incomplete note about a test run. I no longer have the output, have not checked whether anything failed, and have not decided whether I need help or

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R08

Report fingerprint: `9e2f03c27e36e603bd957131e94004196eaa5a435ca071db2261df9b06919e3a`

Notes for later

I saved an incomplete note about a test run. I no longer have the output, have not checked whether anything failed, and have not decided whether I need help or want anything changed.


Suggested type: None

Quote: None

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R09

Report fingerprint: `5a0d5c7e850980d34b9217288dfdadc85bd365b85b24691d6a7eef4ace64ed8a`

Sharing a connection

My function-scoped connection fixture opens and closes correctly. I want to reuse one connection across all tests in a module. Which fixture scope should I choose?


Suggested type: type: question

Quote: My function-scoped connection fixture opens and closes correctly. I want to reuse one connection across all tests in a module. Which fixture scope should I choo

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R10

Report fingerprint: `fa7ea66cb79257e705a38b78771caf0879ede1e8f3d5246e17d7f09aa7b4f61d`

Configuration precedence

The reference says a project configuration value overrides the command-line value. The implementation and intended behavior give the command line priority. Please correct that sentence in the reference.


Suggested type: type: docs

Quote: The reference says a project configuration value overrides the command-line value. The implementation and intended behavior give the command line priority. Plea

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R11

Report fingerprint: `827972a8e9c0174527710ab5ef2ffbab9b57bf311e7693d6eab51ce41bae9b0d`

Understanding a warning

All my tests pass, and the warning correctly describes a deprecated option I still use. Where can I configure pytest to hide this warning temporarily while I update my project?


Suggested type: type: question

Quote: All my tests pass, and the warning correctly describes a deprecated option I still use. Where can I configure pytest to hide this warning temporarily while I up

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R12

Report fingerprint: `b65930542b3e85f3a781f89473db325a9294b16aac7f56fdc27e3ccb305edf9c`

Process exit status

For the same failing test, pytest 8.2 exits with status 1 and pytest 8.3 exits with status 0. The summary reports the failure in both. Reinstalling 8.2 restores status 1.


Suggested type: type: bug

Quote: For the same failing test, pytest 8.2 exits with status 1 and pytest 8.3 exits with status 0. The summary reports the failure in both. Reinstalling 8.2 restores

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R13

Report fingerprint: `932eb2bdd69d8620d9e1f198fa1b04ad2fdb84d2512f7fa4ef343f08787826eb`

Captured traceback

A failing test raises ValueError with a message, but the displayed traceback attributes it to an unrelated test that passed. The problem occurs on both tested releases. Please show the traceback for the actual failing test.


Suggested type: type: bug

Quote: A failing test raises ValueError with a message, but the displayed traceback attributes it to an unrelated test that passed. The problem occurs on both tested r

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R14

Report fingerprint: `e0060f857ba8bf46327ddd3a1aa4795d86b7073209b21bf8019d66d92c37ed98`

Understanding a warning

All my tests pass, and the warning correctly describes a deprecated option I still use. Where can I configure pytest to hide this warning temporarily while I update my project?


Suggested type: type: question

Quote: All my tests pass, and the warning correctly describes a deprecated option I still use. Where can I configure pytest to hide this warning temporarily while I up

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R15

Report fingerprint: `a7bffe78391805da12693c4ac00d5f4c2357553bffe731f80336d12f24d06fa4`

Log file entries

With --log-file enabled, each emitted log record appears twice in the output file. The same unchanged project shows this on both pytest 8.2 and 8.3. Please fix the duplicate writes.


Suggested type: type: bug

Quote: With --log-file enabled, each emitted log record appears twice in the output file. The same unchanged project shows this on both pytest 8.2 and 8.3. Please fix

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R16

Report fingerprint: `1ea7fb0336d89790bd1a7678438fb1040f330324e1d62a5347901a416689dca0`

Synthetic application input: long. Inspect the exact title/body in [integration inputs](../integration-inputs.json). The long form adds observation lines to the same exit-status opening, not a new quality case.


Suggested type: type: bug

Quote: Observation 010: the assertion failed and the process status remained zero.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R17

Report fingerprint: `38b6582b708b080efceaa6dfba26b0636b65ac7fe645ee2495f14120955a7c86`

Configuration precedence

The reference correctly says the command line overrides project configuration, and that works for me. How can I choose a different value for just one invocation without editing the project file?


Suggested type: type: question

Quote: The reference correctly says the command line overrides project configuration, and that works for me. How can I choose a different value for just one invocation

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R18

Report fingerprint: `de88020a557cf2367d40aadfafb19525f131377da8a17a94d5f32cb2330a6307`

Configuration precedence

The reference says a project configuration value overrides the command-line value. The implementation and intended behavior give the command line priority. Please correct that sentence in the reference.


Suggested type: type: docs

Quote: The reference says a project configuration value overrides the command-line value. The implementation and intended behavior give the command line priority. Plea

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R19

Report fingerprint: `db23f0c25fcb32745c1b3286f71638426a5a2673bd7b5c091a779f53aebfed3e`

Closing a connection

A function-scoped fixture opens one connection, yields it to one passing test, and should then close it. Its teardown never runs, leaving the connection open. This also happens on the previous release.


Suggested type: type: bug

Quote: A function-scoped fixture opens one connection, yields it to one passing test, and should then close it. Its teardown never runs, leaving the connection open. T

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R20

Report fingerprint: `eb7e61fd1aa7ecfcae10a2833784f98ee89e259ad5ebd4106d21213fd444d7b6`

Notes for later

I saved an incomplete note about a test run. I no longer have the output, have not checked whether anything failed, and have not decided whether I need help or want anything changed.


Suggested type: type: bug

Quote: I saved an incomplete note about a test run. I no longer have the output, have not checked whether anything failed, and have not decided whether I need help or

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R21

Report fingerprint: `d830cacf5779ac0a1a94a3e58eaba5c77908baaced6baaacbd88e7a213fd2035`

Process exit status

A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked behave this way. Please fix the exit status.


Suggested type: type: bug

Quote: A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R22

Report fingerprint: `ef9d277dc62f0deae305b485deedc3b62ad9ee87af57d7be066850d7e03dc0a0`

Historical pytest #12223: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: bug

Quote: junit-xml output attribute can be too big to handle with -vv

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions


Ratings / reviewer / reasons: pending


## R23

Report fingerprint: `468eecffb1903692a73d297de52b83535afd6a57e4ac890c4f087b6640ef43f7`

Sharing a connection

My function-scoped connection fixture opens and closes correctly. I want to reuse one connection across all tests in a module. Which fixture scope should I choose?


Suggested type: type: question

Quote: My function-scoped connection fixture opens and closes correctly. I want to reuse one connection across all tests in a module. Which fixture scope should I choo

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R24

Report fingerprint: `73f89f2e40af0d97404e8ee082255a9f68fe414b0a5098f0ad15cde4c814808d`

Historical pytest #12219: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: bug

Quote: However, with pytest 8.x, I'm finding that it's not supported, even though the [docs say it is](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C5]

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

- [C4](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?

- [C5](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up


Ratings / reviewer / reasons: pending


## R25

Report fingerprint: `c4f1ec3bd2e21f422ee4b85b82850d0f3a752f4b416592bed8266e25badbdea1`

Configuration precedence

The reference correctly says the command line overrides project configuration, and that works for me. How can I choose a different value for just one invocation without editing the project file?


Suggested type: type: question

Quote: The reference correctly says the command line overrides project configuration, and that works for me. How can I choose a different value for just one invocation

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R26

Report fingerprint: `fd4fd5da206a3e2338a00e5068734582e512b9cda309677968959605fd5757b7`

Historical pytest #12249: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: enhancement

Quote: ctions, then they get raised early and cannot be controlled by the pytest `filterwarnings` config, which is unfortunate. There should be a good way to suppress

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

- [C1](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example


Ratings / reviewer / reasons: pending


## R27

Report fingerprint: `e23de338f1fb8e36986db047b9e2b9c80accbaf00a4194982e3ede8b81d396ec`

Configuration precedence

The reference correctly says the command line overrides project configuration, and that works for me. How can I choose a different value for just one invocation without editing the project file?


Suggested type: type: question

Quote: The reference correctly says the command line overrides project configuration, and that works for me. How can I choose a different value for just one invocation

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R28

Report fingerprint: `b5e77a5b6624e10e3a0d0fa41ef088fcdec0762ec800a01814f5c6f56b064a67`

Session cleanup

The same plugin and test suite close their temporary directory at session end with pytest 8.2. After upgrading to 8.3, the cleanup callback is never called. Rolling back restores the callback.


Suggested type: type: regression

Quote: The same plugin and test suite close their temporary directory at session end with pytest 8.2. After upgrading to 8.3, the cleanup callback is never called. Rol

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

- [C1](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example


Ratings / reviewer / reasons: pending


## R29

Report fingerprint: `9cbb77e50786647b7df058e8e9f3aded11e030a2243650b301348ffa03aff5db`

Synthetic application input: short. Inspect the exact title/body in [integration inputs](../integration-inputs.json). The long form adds observation lines to the same exit-status opening, not a new quality case.


Suggested type: type: bug

Quote: A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R30

Report fingerprint: `1ff1cdc13361350ed2c7fa443cda8c1d532686a3dcc7037a34c865b53d1e6ea7`

Historical pytest #12249: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: bug

Quote: Handle warnings raised at import time early in pytest process

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

- [C1](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example


Ratings / reviewer / reasons: pending


## R31

Report fingerprint: `adb8a194517d9c7cc51757ff6fe110a0cf1bfbbce57173e36f3294dde4f6adc0`

Log file entries

The unchanged project writes each log record once with pytest 8.2 and twice with 8.3. Switching back to 8.2 restores single writes. Please restore the earlier behavior.


Suggested type: type: regression

Quote: The unchanged project writes each log record once with pytest 8.2 and twice with 8.3. Switching back to 8.2 restores single writes. Please restore the earlier b

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R32

Report fingerprint: `47d6e2a48772b5f0cc74ef281e342e76dfeaf572027ac29fcc7169006089ac25`

Log file entries

The unchanged project writes each log record once with pytest 8.2 and twice with 8.3. Switching back to 8.2 restores single writes. Please restore the earlier behavior.


Suggested type: type: bug

Quote: The unchanged project writes each log record once with pytest 8.2 and twice with 8.3. Switching back to 8.2 restores single writes. Please restore the earlier b

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R33

Report fingerprint: `62d985e5f89a2ac29c0b2611d59da1a1efb2b3091a861c3dc77fbc6ce02c0352`

Sharing a connection

My function-scoped connection fixture opens and closes correctly. I want to reuse one connection across all tests in a module. Which fixture scope should I choose?


Suggested type: type: question

Quote: Sharing a connection

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R34

Report fingerprint: `46a504030f0d2f6929c386af33c7d629cb7dfbcd42cd3d730a3d95121ff3541d`

Log file entries

With --log-file enabled, each emitted log record appears twice in the output file. The same unchanged project shows this on both pytest 8.2 and 8.3. Please fix the duplicate writes.


Suggested type: type: bug

Quote: With --log-file enabled, each emitted log record appears twice in the output file. The same unchanged project shows this on both pytest 8.2 and 8.3. Please fix

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R35

Report fingerprint: `b7cd714e5c2f4bce989d27676b35fa40e71384acad1b98f0ac4e3a3f5bc0e1f8`

Configuration precedence

The reference says a project configuration value overrides the command-line value. The implementation and intended behavior give the command line priority. Please correct that sentence in the reference.


Suggested type: type: docs

Quote: The reference says a project configuration value overrides the command-line value. The implementation and intended behavior give the command line priority. Plea

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R36

Report fingerprint: `9f0607c33a85c95cd5a3f7b2c5192cd55542e273d20c8a4607959ba84cceda47`

Session cleanup

The same plugin and test suite close their temporary directory at session end with pytest 8.2. After upgrading to 8.3, the cleanup callback is never called. Rolling back restores the callback.


Suggested type: type: bug

Quote: The same plugin and test suite close their temporary directory at session end with pytest 8.2. After upgrading to 8.3, the cleanup callback is never called. Rol

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

- [C1](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/50234b4e670064c42a4c29cb6258115a2079ba4c/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example


Ratings / reviewer / reasons: pending


## R37

Report fingerprint: `0a315e4d57d8568cf632f8c27db973adb58e84e52cc1cacc9ed5313576e324f9`

Historical pytest #12249: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: bug

Quote: As noted in https://github.com/pytest-dev/pytest/pull/12248, some modules can raise warnings at import time. If this happens during `AssertionRewritingHook`'s a

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]

- [C1](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/4eb8b6d525b7704432f378cfa45ab9ec02bf4e39/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example


Ratings / reviewer / reasons: pending


## R38

Report fingerprint: `936bd6ac6f979114469c872342cb3eb90c387eaf43ab3f3abc0666e0a100fac6`

Closing a connection

A function-scoped fixture opens one connection, yields it to one passing test, and should then close it. Its teardown never runs, leaving the connection open. This also happens on the previous release.


Suggested type: type: bug

Quote: A function-scoped fixture opens one connection, yields it to one passing test, and should then close it. Its teardown never runs, leaving the connection open. T

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R39

Report fingerprint: `201fdf726799812102dcbf2bd9d13379a09b18165c74a00b4eb02389cbaf5d19`

Process exit status

A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked behave this way. Please fix the exit status.


Suggested type: type: bug

Quote: A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R40

Report fingerprint: `852144d76b3e3300285cd1d97cf779fedc07740e940571dfdf05b182a2989dff`

Historical pytest #12223: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: enhancement

Quote: for parsers, and projects like BeautifulSoup and lxml will fail to parse this correctly (truncating or crashing, respectively).

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions


Ratings / reviewer / reasons: pending


## R41

Report fingerprint: `62f4bd3b700ac2fcbf1f07a13925c2b9e1a31641b515d7c50e3a12dbf584aeb5`

Synthetic application input: long. Inspect the exact title/body in [integration inputs](../integration-inputs.json). The long form adds observation lines to the same exit-status opening, not a new quality case.


Suggested type: type: bug

Quote: Observation 010: the assertion failed and the process status remained zero.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R42

Report fingerprint: `450076f6d018859d4793f7b8782c7f3aa5e2ce45f2853f4c84a151f5f1685de4`

Historical pytest #12219: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: bug

Quote: setUpModule/tearDownModule not invoked

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C5]

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

- [C4](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?

- [C5](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up


Ratings / reviewer / reasons: pending


## R43

Report fingerprint: `396e8ba52ab44aa6fd3aa1037b1065f663ed4c77a08d5467dfdddfafa8966b78`

Synthetic application input: short. Inspect the exact title/body in [integration inputs](../integration-inputs.json). The long form adds observation lines to the same exit-status opening, not a new quality case.


Suggested type: type: bug

Quote: A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R44

Report fingerprint: `d151f650ec393cf2945137bee2bd4b9f1e3d1588ea0f9dbec8b4d25d78c30545`

Process exit status

A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked behave this way. Please fix the exit status.


Suggested type: type: bug

Quote: A test deliberately raises AssertionError and the summary correctly reports one failed test, but the pytest process exits with status 0. Both releases I checked

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R45

Report fingerprint: `16359c67f01473b7e2e00987d5c22296b218fa8e0a7baa895492d370448ce1e6`

Synthetic application input: long. Inspect the exact title/body in [integration inputs](../integration-inputs.json). The long form adds observation lines to the same exit-status opening, not a new quality case.


Suggested type: type: bug

Quote: Observation 010: the assertion failed and the process status remained zero.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R46

Report fingerprint: `8f716dce30834247176d6b34892ca10ec41b0c6145fed6ee3bd9e909501eaeb1`

Captured traceback

A failing test raises ValueError with a message, but the displayed traceback attributes it to an unrelated test that passed. The problem occurs on both tested releases. Please show the traceback for the actual failing test.


Suggested type: type: bug

Quote: A failing test raises ValueError with a message, but the displayed traceback attributes it to an unrelated test that passed. The problem occurs on both tested r

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R47

Report fingerprint: `9905d55e0823ec1c95c4db5a4412719af29276e00abb070f5c322299509fb007`

Process exit status

For the same failing test, pytest 8.2 exits with status 1 and pytest 8.3 exits with status 0. The summary reports the failure in both. Reinstalling 8.2 restores status 1.


Suggested type: type: bug

Quote: For the same failing test, pytest 8.2 exits with status 1 and pytest 8.3 exits with status 0. The summary reports the failure in both. Reinstalling 8.2 restores

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R48

Report fingerprint: `50e54f896d747bb8517fbb06a307a24f3eae3742d1f98b1e262b19da4064d815`

Historical pytest #12219: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: regression

Quote: ts.tarfile). When I run the tests, the setUpModule is never called.

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]
- Could you add a minimal example, if possible? [C3]
- You report that the hook works in the minimized example. Could you reduce the affected project's case to a minimized failing example, including its module layout, configuration and exact command? Compare that with the working example to isolate what prevents the hook from running. [C5]

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions

- [C3](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L16): pytest bug report template: minimal example

- [C4](https://github.com/pytest-dev/pytest/issues/4064): pytest issue #4064: Docs: is setUpModule/tearDownModule supported?

- [C5](https://github.com/pytest-dev/pytest/issues/12219): Submitted issue under review: investigative follow-up


Ratings / reviewer / reasons: pending


## R49

Report fingerprint: `a3af30316936804da208d21277c5b2deeaae8cef61ed5b34ff3133640edc45da`

Log file entries

With --log-file enabled, each emitted log record appears twice in the output file. The same unchanged project shows this on both pytest 8.2 and 8.3. Please fix the duplicate writes.


Suggested type: type: bug

Quote: With --log-file enabled, each emitted log record appears twice in the output file. The same unchanged project shows this on both pytest 8.2 and 8.3. Please fix

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R50

Report fingerprint: `75d9ed19d3085d8334e9f9a2648f65cd80e153fac91ca145f03e6f3630a73aa2`

Log file entries

The unchanged project writes each log record once with pytest 8.2 and twice with 8.3. Switching back to 8.2 restores single writes. Please restore the earlier behavior.


Suggested type: type: bug

Quote: The unchanged project writes each log record once with pytest 8.2 and twice with 8.3. Switching back to 8.2 restores single writes. Please restore the earlier b

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R51

Report fingerprint: `4f79945c8a9fe983dd55c47ec2c24875e197ef8099f3b331c50ff351234632e0`

Closing a connection

A function-scoped fixture opens one connection, yields it to one passing test, and should then close it. Its teardown never runs, leaving the connection open. This also happens on the previous release.


Suggested type: type: bug

Quote: A function-scoped fixture opens one connection, yields it to one passing test, and should then close it. Its teardown never runs, leaving the connection open. T

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R52

Report fingerprint: `023e02f074c0acf590c447c97781b386ec1f1cabe96ad72ca0af672112da7abb`

Synthetic application input: long. Inspect the exact title/body in [integration inputs](../integration-inputs.json). The long form adds observation lines to the same exit-status opening, not a new quality case.


Suggested type: type: bug

Quote: Observation 010: the assertion failed and the process status remained zero.

Thanks for sharing this issue. I cannot substantiate a specific request from the available evidence.


Ratings / reviewer / reasons: pending


## R53

Report fingerprint: `22f50a97c4073114333243d4ddadc9049668d24e4c5eea6d86bed6ef04893be3`

Historical pytest #12223: inspect its opening at the recorded cutoff; no later labels or comments.


Suggested type: type: bug

Quote: junit-xml output attribute can be too big to handle with -vv

Thanks for sharing this issue.
- Could you add the output of `pip list` from the virtual environment you are using? [C1]
- Could you add your operating system and release? [C2]

- [C1](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L14): pytest bug report template: pip list output

- [C2](https://github.com/pytest-dev/pytest/blob/58844247f7ae4a7a213a73c8af2462253b3d8fc7/.github/ISSUE_TEMPLATE/1_bug_report.md#L15): pytest bug report template: pytest and OS versions


Ratings / reviewer / reasons: pending

# Open-source Maintainer Copilot

Terms used when describing the copilot's issue-triage work.

## Language

**Target repository**:
The one public open-source project whose issues and project material provide the context for triage.

**Issue under review**:
A GitHub issue presented to the copilot for triage, whether newly written or replayed from history.
_Avoid_: Ticket

**Evidence**:
A referenced repository artifact that supports a claim in a triage report, such as an issue, documentation passage, code location, or CI result.

**Triage report**:
A reviewable assessment of an issue under review that identifies likely duplicates, an issue category, missing details, and a draft maintainer reply. Each factual claim cites evidence or explicitly abstains.
_Avoid_: Answer, resolution

**Duplicate candidate**:
An earlier issue that may describe substantially the same failure or requested behavior as the issue under review, pending human confirmation.
_Avoid_: Related issue

**Related issue**:
An earlier issue sharing a topic with the issue under review without evidence that it describes the same failure or requested behavior.

**Issue family**:
A group of issues about the same underlying failure or requested behavior, including confirmed duplicates and follow-ups.

**Missing report detail**:
Information requested by the applicable pytest issue template but absent from the issue under review.
_Avoid_: Incomplete issue

**Abstention**:
An explicit statement in a triage report that the available evidence is insufficient to support a particular conclusion.
_Avoid_: Failure

**Evaluation case**:
A historical issue under review paired with a human-reviewed expected triage outcome and an evidence cutoff.

**Expected triage outcome**:
The human-reviewed duplicate, issue type, and missing-detail judgments used to score an evaluation case. It is distinct from labels or comments applied later in the target repository.
_Avoid_: GitHub label, ground truth label

**Evidence cutoff**:
The point in the target repository's history after which artifacts cannot be used to assess an evaluation case.

**Quality reference**:
A stronger model run on the same evaluation cases to estimate the quality gap for the locally served model. Its outputs are comparisons, not expected outcomes.
_Avoid_: Ground truth

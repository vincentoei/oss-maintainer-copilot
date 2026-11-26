# Register and triage public repositories

Issue #33 extends #1's pytest-first release to multiple locally registered public
GitHub repositories, with one explicitly selected target per report. The fixed
legacy RAG workflow and selected Qwen2.5-Coder 3B remain the demo default. Agent
and experimental drafting remain opt-in; registration does not establish triage
quality for every language, project or template format.

Run the server using the README's setup commands. In the browser, add
`https://github.com/owner/repo` or `owner/repo`, inspect readiness and prepared
context, choose the active repository, then submit an issue. Refresh and remove
buttons affect the selected registration. A report displays its own captured
repository and revision even if the selection subsequently changes.

## HTTP and Python interfaces

```sh
curl -X POST http://127.0.0.1:8000/api/repositories \
  -H 'Content-Type: application/json' -d '{"repository":"astral-sh/ruff"}'
curl http://127.0.0.1:8000/api/repositories
```

Copy the returned stable `id` (derived from GitHub's numeric repository identity).
Canonical owner/name comes from GitHub, including redirects and case correction.
Duplicate registration returns the existing entry; it does not silently refresh
or change configuration. Any valid public repository is eligible. An empty
repository without a resolvable commit returns a setup error. Nonexistent,
inaccessible and private repositories return an error without adding an entry.
Registration preparation is anonymous, so a token cannot admit private projects.
Target access is read-only.

```sh
curl -X POST http://127.0.0.1:8000/api/triage \
  -H 'Content-Type: application/json' \
  -d '{"registration_id":"RETURNED_ID","title":"An issue","body":"Opening text"}'
curl --get http://127.0.0.1:8000/api/source \
  --data-urlencode 'registration_id=RETURNED_ID' \
  --data-urlencode 'commit=FULL_40_CHARACTER_SHA' \
  --data-urlencode 'path=src/main.rs' --data-urlencode 'line=1'
curl -X POST http://127.0.0.1:8000/api/repositories/RETURNED_ID/refresh
curl -X DELETE http://127.0.0.1:8000/api/repositories/RETURNED_ID
```

The optional agent endpoint accepts the same body at `/api/agent/triage`.
`GET /api/source` carries registration identity and returns a URL identifying the
selected repository. An explicitly supplied `source_location.repository` must
match selection. An unknown or removed registration is HTTP 422, including for
source inspection; requests never silently substitute another repository.

```python
from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.registry import RepositoryRegistry

registry = RepositoryRegistry(".local/repositories.sqlite3")
registered = registry.add("astral-sh/ruff")
print(registry.list())
report = triage_issue(
    IssueUnderReview(registration_id=registered.id, title="An issue", body="Opening"),
    registry=registry,
)
registry.refresh(registered.id)
registry.remove(registered.id)
```

Python registration/selection errors raise `RegistrationError` (a `ValueError`).
The ordinary Python API uses the same registry path as HTTP. New installations
seed `pytest-default`, the bundled verified pytest adapter with pinned template
requirements, label rules, and documentation topics. Omitted selection uses this
default for compatibility. Removing it persists across restarts, and omitted
selection then fails with a clear setup error. Adding pytest later does not
silently restore default selection. Historical replay uses its own pinned profile,
not the live registry, even when that registration has been refreshed or removed.

## Storage, refresh and configuration

`REPOSITORY_REGISTRY_PATH` defaults to `.local/repositories.sqlite3`, ignored by
Git. SQLite stores stable registration/GitHub IDs, canonical identities,
configuration and prepared context as transactional snapshots. Keep this file
when restarting or moving the local single-user application. There is no
multi-user tenancy or private-repository onboarding. Trace records remain in
memory for the last 100 reports; explicitly saved evaluation artifacts are
separate. Removing a registration deletes only its local registry row, never
GitHub data, reports on disk, historical cases, raw model outputs or judgments.

Context is prepared once on registration and replaced only by explicit refresh.
Each request resolves one immutable snapshot before any read; an in-flight
report keeps its old snapshot. Failed refresh records an `error` state and blocks
future triage until a successful refresh. Disabled issues also yield `error`.
Missing or unsupported context yields `limited` plus actionable omissions, while
supported capabilities remain usable. Inspect the complete snapshot with the
list endpoint or the browser's prepared-context disclosure.

The bundled pytest adapter preserves its verified historical template semantics.
Refreshing that registration prepares a **generic** live view at the new commit;
it does not transplant old pytest requirements onto potentially changed files.
The refresh result discloses this transition. Historical replay always retains
its recorded original adapter/revision and cutoff.

Optional JSON configuration can refine sources and supported conventions. Supply
`configuration` when adding a new registration, or the configuration object itself
as the body of `POST /api/repositories/ID/refresh`:

```json
{
  "documentation_paths": ["README.md", "docs/contributing.md"],
  "type_labels": ["bug", "enhancement"],
  "markdown_required_fields": {
    ".github/ISSUE_TEMPLATE/bug.md": ["Reproduction", "Expected behavior"]
  }
}
```

Every path is a validated relative path in the selected repository. Required
Markdown headings must occur in the actual pinned file. Type labels must occur
in the fetched label list. No per-repository Python profile is necessary; the
Ruff integration uses exactly the ordinary registration flow and generic profile.

## Supported context and explicit limits

Preparation resolves a full default-branch commit SHA. Templates and documentation
are read at that SHA, rather than a moving branch. Labels are GitHub's current
repository configuration at preparation time (GitHub labels have no commit SHA);
`prepared_at` records observation time. The bundled default is a previously
verified pinned profile rather than a fresh network observation.

- At most **12 fetches per preparation**, sequential, each with a **5-second
  timeout** and **256 KiB response cap**. Four concurrent preparations per
  process, with a five-second slot-acquisition timeout. No retries, history crawl,
  embeddings or full-repository indexing. SQLite locks wait at most five seconds.
- At most four Markdown/YAML files from `.github/ISSUE_TEMPLATE`, sorted by name;
  extra files are explicitly omitted. Organization-inherited templates and
  unsupported file formats are not interpreted. Absent supported templates yield
  a limited state. `config.yml` routing is not a source of required fields.
- GitHub issue forms support `input` and `textarea` fields with a literal label
  and Boolean `validations.required`. Markdown display blocks are skipped.
  Dropdowns, checkboxes and unsupported fields are disclosed and excluded from
  missing-detail conclusions. At most twenty supported fields per template.
- Markdown supports YAML front matter and ATX headings. Headings alone do not
  prove requirements: explicit `markdown_required_fields` establishes them.
  Templates exceeding twenty headings are omitted with an explicit limit error.
  No mapping means limited requirement detection, without pytest assumptions.
- Generic template applicability requires exactly one template whose supported
  headings all appear in the opening; a unique exact heading set takes precedence
  over subset matches. Ambiguous or unrecognizable openings
  abstain. Only a blank or explicit no-response/TODO/TBD required section is
  requested; optional sections are never required. Fenced/indented code and
  comments cannot establish headings; repeated headings abstain. Arbitrary prose is not
  interpreted as proof that an unrendered section is missing. This conservative
  rule can miss actual omissions and cannot guarantee semantic completeness.
- First 100 available labels only; a full page is disclosed as possibly capped.
  Generic type candidates come from template labels or configured `type_labels`,
  intersected with verified available labels. Literal, unnegated wording
  remains part of lexical profile rules. Model classification can select
  any resolved type label with an exact issue-text quote; the server verifies
  provenance rather than semantic label support. Unestablished conventions
  or no matching evidence abstain; arbitrary label names are not semantic types.
- At most three configured documents (defaults: README.md, CONTRIBUTING.md,
  docs/README.md). Each supplies at most its first twenty lines and 2,000
  characters; remaining content and unavailable files are disclosed. Oversized
  files are omitted. Claims quote the prepared extract and are reverified against
  that pinned public file during the report. Extractive presence is not proof of
  relevance or semantic support. Project-specific pytest topics stay in its adapter.

Issue search remains bounded to ten pages/1,000 results, eight seconds and 2 MB
per response; oversized/incomplete/changing results abstain. Generic lexical
matches are only **related issues**: matching words cannot establish duplicates.
The pytest adapter retains its existing relationship rules. Source reads remain
five seconds/256 KiB, at most eleven lines/4,096 characters. CI remains conditional
on one explicit relevant PR/commit link **in the selected repository**, with its
existing bounded check reads. Links to other repositories authorize no reads.

Report, trace and model requests carry the repository context. Issue records,
source locations, CI links, cache comparisons and evidence URLs carry repository
identity. Model-authored references, foreign evidence, unsupported labels and
unknown citation IDs are rejected. Selection-only model limits, untrusted-input
handling, read-only tools, agent step limits and partial reports are retained.
Report and trace JSON add `context`; source locations add `repository`; model
requests add repository-specific labels/context in place of pytest-only labels.
These are intentional interface changes, without promoting experimental drafting.

Earlier evaluation files and case metadata are immutable. Old source/prompt hashes
refer to their recorded Git commits; they are not claims about this changed live
application. Replaying history still verifies opening hashes, timestamps and
pre-cutoff revisions before inference. Quality claims about new reports require
fresh explicit human review. See the [issue #33 acceptance record](evaluation/issue-33.md).

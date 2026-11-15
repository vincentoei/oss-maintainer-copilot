## Agent skills

### Issue tracker

Track issues and specs in GitHub Issues for `vincentoei/oss-maintainer-copilot`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the five default triage labels. See `docs/agents/triage-labels.md`.

### Domain docs

Use a single-context root glossary and `docs/adr/`. See `docs/agents/domain.md`.

## Commits

When creating a Git commit, follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Write the subject as `<type>[optional scope][!]: <description>`.

Use `feat` for a new feature and `fix` for a bug fix. Use `docs`, `test`, `refactor`, `perf`, `build`, `ci`, or `chore` when they describe the change. Keep the description short and specific; add a scope when it helps identify the affected part of the codebase.

Mark a breaking change with `!` before the colon or a `BREAKING CHANGE: <description>` footer. Separate an optional body and any footers from the preceding section with a blank line.

Examples: `feat(triage): suggest duplicate issues`, `fix(retrieval): handle empty search results`, `docs: explain local model setup`.

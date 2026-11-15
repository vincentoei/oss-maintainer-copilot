# Issue tracker: GitHub

Issues and specs for this repo live in GitHub Issues at
`vincentoei/oss-maintainer-copilot`. Use `gh` from this repo.

## Conventions

- Before the first issue write in a session, verify the target with
  `gh repo view --json nameWithOwner`.
- Create an issue with `gh issue create --title "..." --body-file <file>`.
- Read an issue with
  `gh issue view <number> --json number,title,body,labels,comments`.
- List issues with `gh issue list --state open --json number,title,labels`
  and suitable filters.
- Add or remove labels with `gh issue edit <number> --add-label <label>`
  or `--remove-label <label>`.
- Comment with `gh issue comment <number> --body-file <file>`.
- Close after recording the resolution in a comment.
- Link child issues to a parent using GitHub sub-issues when available.
  Otherwise put `Part of #<parent>` in the child body.
- Record blockers using GitHub issue dependencies when available.
  Otherwise put `Blocked by: #<number>` near the top of the issue.

## Pull requests as a triage surface

PRs as a request surface: no.

## Skill operations

- "Publish to the issue tracker": create a GitHub issue in this repo.
- "Fetch the relevant ticket": read the referenced GitHub issue.
- Wayfinding maps are issues labelled `wayfinder:map`; child tickets
  link to the map and use `wayfinder:<type>` labels. Claim a ticket by
  assigning it to the agent's user, resolve it with a comment and close
  it, then add a brief decision link to the map.

# Resolve a repository snapshot before triage

The local application persists registrations and explicit-refresh snapshots in
SQLite, then resolves one immutable target-repository context before any report
reads. A generic profile uses bounded supported templates, verified labels and
pinned document extracts; the bundled pytest adapter preserves its verified
policy. This trades exhaustive repository understanding and continuous sync for
bounded, inspectable preparation and isolation between concurrent reports.
Historical evaluation bypasses the live registry and retains case-specific pinned
profile evidence, opening verification and cutoffs under ADR-0001; refresh and
removal cannot rewrite historical artifacts or judgments under ADR-0003.

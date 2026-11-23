# Explicit human pilot review

Requesting user confirmed the following before pilot inference on 2026-11-23:

> Confirmed: all five proposed outcomes and family separations are supported by the issue openings. No expected-outcome changes are needed.

| Issue | Type | Missing details | Review rationale (verbatim) |
|---|---|---|---|
| #11902 | bug | Installed packages; operating system | Reports collection failing on an adjacent restricted directory. Supplies a shell reproducer and pytest/Python versions; Unix-style commands do not establish the OS version. |
| #11906 | bug | Installed packages | Demonstrates a multi-argument warning triggering TypeError during re-emission, with a runnable example, pytest version comparison and Windows version. |
| #11945 | bug | Installed packages; operating system | Supplies a concise nested-versus-inner comparison and pytest version. The reported inconsistent comparison supports bug classification without assuming the underlying cause. |
| #11940 | enhancement | None | Provides the conflicting-plugin-flags use case, proposed public API and existing private-parser workaround. |
| #11973 | enhancement | None | Explains classifier-based discovery for the published plugin list, with concrete examples and the current manual-addition workaround. This concerns catalog generation, not runtime plugin loading. |

Additional user confirmation (verbatim):

> The five describe distinct failures or requested behaviors, and are distinct from the original twenty. In particular:
>
> - #11902 concerns directory permissions during collection; #12083 concerns overlapping file/directory arguments and omitted tests.
> - #11906 concerns warning reconstruction; #12204 concerns growing tracebacks from cached fixture exceptions.
> - #11945 concerns approximate comparison semantics; #12223 concerns formatting large assertion failures in XML.
> - #11940 and #11973 concern separate plugin capabilities: reporting usage errors and discovering plugins for a published list.
>
> Keep all five earlier-issue relationship judgments uncertain. Family separation within these twenty-five cases does not establish whether other historical issues are duplicates

# Using the skills

Choose a skill from the [README](../README.md#available-skills) and provide the issue, PR, CI run/logs, review feedback or feature description. Add the relevant version or checkout when known. You can supply a URL, a repository-qualified identifier, or pasted evidence.

## Invocation

Use the [Codex and Claude Code prompts](../README.md#run-a-skill), replacing `review-pr` with the desired skill name. The examples below use plain-language requests that you can also enter directly in supported clients.

## Investigate a bug

```text
Use triage-bug to analyze <issue-url>, check duplicates, and draft a report, short comment, and next actions.
```

Include the affected version, deployment details, and reproducer when available. The skill checks expected versus observed behavior, duplicates and existing fixes, and priority using Keycloak's verification flow. Security concerns are routed for appropriate handling.

## Assess a security report

```text
Use triage-cve to assess <report>, check related issues, and draft an internal handoff and a public-safe reply.
```

Specify the intended audience and whether the report is private. Keep confidential evidence in authorized private sources. The assessment distinguishes security impact, CVE status, severity, urgency, and disclosure handling. Tracker recommendations use verified metadata and the applicable security policy.

## Implement a fix

For failures first discovered in CI, start with the diagnosis workflow below when the cause is unknown.

```text
Use fix-issue to fix <issue-url> in <checkout> on <branch>, including regression coverage.
```

Provide a target checkout or revision. The skill traces the root cause, reuses suitable Keycloak abstractions, implements the fix, and validates supported behavior. It discusses unresolved contract or compatibility choices with you. A CVE or prior triage is not required.

## Implement a feature

```text
Use implement-feature to implement <feature-or-design> in <checkout> on <branch>, including acceptance tests and documentation. Keep the work local.
```

Provide the intended behavior, accepted design and exclusions when known. The skill reuses existing Keycloak implementations, applies target-specific maturity and compatibility rules, and implements the relevant interfaces. It checks permissions and state changes, selects tests from the target revision, and reports actual validation and gaps. Ripwire is optional; other AI plugins are not prerequisites.

Use `fix-issue` for a standalone bug, security hardening or vulnerability fix. A feature request can include an underlying fix, with separate acceptance and regression evidence. Request PR creation explicitly when wanted and identify the destination; the skill follows applicable contribution, draft and disclosure requirements.

## Diagnose CI

```text
Use diagnose-ci to investigate the failed checks on <pr-url> and identify the cause and next action.
```

You can also supply a workflow run, job URL or CI logs. Include the run attempt and target checkout when known. The skill identifies what actually ran, separates independent causes from cascades, inspects retry evidence and attempts a practical matching local reproduction. It distinguishes source deductions, supplied results, executed checks and missing evidence.

Diagnosis does not automatically rerun CI or edit code. To include a correction, request it explicitly, for example: `Use diagnose-ci to diagnose <job-url> and fix the supported defect locally with regression coverage.` Reruns and other remote actions follow existing authorization. Expired logs or blocked dependencies remain evidence/validation gaps rather than invented causes or passing tests.

## Backport a merged pull request

```text
Use backport-pr to backport <pr-url> to release/26.4 and release/26.6 in <checkout>, push to my verified fork, and create one PR per target.
```

Specify the source PR, requested release branches and push destination. The skill starts each new target from its freshly fetched release tip in a separate worktree, invokes the repository's `.github/scripts/pr-backport.sh`, and handles target-specific adaptations and recovery. It preserves the source merge-commit message and cherry-pick provenance, validates each branch, and verifies the final PR identity.

The inspected script pushes before opening a browser; the skill completes PR creation through CLI when needed and reports validation separately. PRs remain drafts when the user or applicable repository instructions require it, or required validation is pending. Single-commit and sign-off requirements are checked against the script's automatic commit/push steps. For a local-only plan, explicitly prohibit pushes and PR creation; that request does not invoke the publishing script. Existing backports are inspected and resumed, and unrelated branch/worktree collisions are preserved.

## Review a pull request

```text
Use review-pr in feature mode to review <pr-url> against <design-or-issue-url>.
```

Provide a PR URL or a diff with base/head revisions and issue or design context. The skill selects relevant checks automatically. To guide its focus, request `bug`, `feature` (including enhancements), `hardening`, or `vulnerability` mode. A CVE or prior triage assessment is not required.

## Address review feedback

```text
Use address-review to address feedback on <pr-url> in <checkout>, validate the changes, and draft replies.
```

Provide supplied feedback instead of a PR URL when remote access is unavailable. The skill checks current source and follow-up discussion, groups comments sharing one cause, applies justified corrections and explains unsupported suggestions. Outdated comments are assessed for whether the concern still exists. Conflicting public-contract choices require a focused decision while independent work continues.

Draft replies remain local. Request commits, pushes, posting or thread resolution when wanted; previously authorized actions need no repeated permission. Local implementation, validation, publication and remote thread state are reported separately. For an assessment without edits, state that scope explicitly. Use `review-pr` for an independent review of the proposed change as a whole.

## Create a skill

```text
Use add-skill to create a skill for reviewing Keycloak configuration.
```

Describe the task, expected result, and target client or location when known. Collection skills go in `skills/`; standalone skills use the target client's discovery directory. The authoring workflow keeps instructions portable and adds supporting resources when useful. New or changed workflows are compared with a behavioral baseline; editorial changes need only appropriate diff and link checks. Available Ripwire assistance can help locate relevant code and tests, with source verification and ordinary repository search as the fallback.

## Refresh a skill's references

```text
Use update-skill to check skills/review-pr against its current references and apply relevant corrections in this checkout.
```

Provide the source skill directory and any target versions or reference subset.
Request an assessment only when you want a report without edits.
The skill distinguishes applicable changes, relocated links, and sources it cannot verify, and validates affected instructions before claiming completion.
It can retain guidance that remains correct; newer documentation for another version does not automatically replace it.
Plugin installation and upgrades use the commands in the installation guide.

## Drafts and changes

Triage and `review-pr` return assessments and comment drafts. Fix, feature and review-feedback requests include scoped local implementation and validation; `diagnose-ci` implements a correction when the request includes it. A request to create backport PRs includes the necessary commits, normal pushes and PR creation for the specified targets and destinations. Honor requests limited to drafting text or local work; creating a draft PR still publishes it. CI reruns, posted replies, thread resolution, bot triggers, metadata changes, publishing and live-system changes require authorization for the action and destination, including authorization already given.

For the detailed decision criteria, follow the skill links in the README. The [triage guidance](../skills/triage-bug/references/triage-guidance.md) and [review guidance](../skills/review-pr/references/review-guidance.md) explain which project requirements and external recommendations apply.

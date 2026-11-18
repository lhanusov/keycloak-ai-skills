---
name: address-review
license: Apache-2.0
description: "Address review feedback on an existing Keycloak PR or supplied patch in a target checkout: verify findings, implement justified corrections, validate them, and draft thread replies. Use for responding to feedback, rather than initiating a general PR review, standalone issue triage, or backporting."
---

# Address Keycloak review feedback

Resolve the substance of review feedback against the current implementation and original requirements. Verify before changing code, preserve working behavior, and explain disagreements with concrete evidence. A reviewer suggestion is a claim to assess, not authority to expand the task or publish changes.

## Establish the scope and current state

Use GitHub CLI (`gh`) by default for GitHub data and actions; read [GitHub CLI guidance](references/github-cli.md) for PR/review retrieval, complete thread pagination, authorized replies and access fallbacks.

Accept a PR URL or supplied feedback and a target checkout. Resolve repository, branch, current head, base, requirements and authorization from the conversation and available sources. Read applicable repository instructions and contribution/test guidance. Read [evidence and verification](references/evidence.md), and [security handling](references/security-handling.md) for confidential material or security concerns.

A request to address feedback includes justified local corrections and validation. Honor narrower assessment-only or reply-draft-only requests. Commits, pushes, posted replies and thread resolution follow their separately requested or previously authorized scope; drafting a reply does not post it. Do not infer permission to merge, rewrite published history, contact others or operate live systems. Authoring/evaluating this skill authorizes no real PR corrections or publication.

Inspect the working tree and preserve unrelated staged and unstaged changes. Use an isolated worktree when branch changes, reproduction or dirty-state isolation warrant it, starting from the intended inspected revision. Preserve existing worktrees and pending changes. With supplied feedback or patches only, state unavailable remote/revision context instead of inventing it.

Read relevant inline review threads, general reviews/comments and follow-up discussion, including outdated locations when the concern may persist. Retrieve complete relevant threads and pagination; a PR summary may omit inline feedback. Record stable thread and comment IDs, original review revision/location and current source. Recheck which head the checkout and supplied CI actually describe.

## Verify and organize findings

Connect feedback to the PR's accepted requirements and exclusions. Trace current source, callers, validation, tests and applicable versioned specifications. Confirm specification role/profile and target conventions before alleging noncompliance. Use [optional Ripwire assistance](references/ripwire.md) when it helps find the current implementation, reusable correction or affected tests; verify source and continue with repository search if unavailable. No analysis plugin is required.

Classify each actionable concern:

| Disposition | Evidence and response |
| --- | --- |
| Change required | A demonstrated defect, unmet accepted requirement or applicable policy gap needs a scoped correction. |
| Already addressed | Current code and relevant validation satisfy the concern; cite the actual revision and behavior, not only an outdated/resolved badge. |
| Unsupported or unnecessary | Caller safeguards, accepted scope or other concrete counterevidence defeats the suggestion. Explain it without creating an artificial change. |
| Unresolved / clarification needed | Missing evidence or a material contract conflict prevents a reliable choice. Identify the smallest check or decision. |

Group related comments by root cause/remedy while keeping each thread's resolution mapping. Distinguish required corrections, questions and optional design preferences. Existing tests or maintainer familiarity alone do not prove correctness; equally, an unfamiliar design is not a defect. Drop disproven concerns and avoid abstractions or unrelated refactoring without a supported need.

For incompatible feedback, use accepted requirements, applicable policy and evidence rather than reviewer count. Present a focused question with alternatives and a recommendation when public behavior, security, compatibility or substantial scope remains undecided. Defer only dependent changes; proceed with independent corrections and test preparation. Do not reopen settled decisions or request routine approval again.

## Correct and validate

Implement the smallest coherent correction at the responsible layer, covering affected entry points and preserving legitimate behavior. A shared defect needs shared enforcement rather than separate partial fixes. For security-sensitive rejections, check protected state and forbidden side effects, not just an error or false result. Keep details within their authorized audience.

Use the target's existing test framework, fixtures and resource-lifecycle conventions. Add or adjust meaningful regression/acceptance assertions for the corrected contract, including relevant boundaries and previous supported behavior. No new mocking framework is needed to work around unavailable integration tests. When feasible, show a defect regression detects the old behavior; compilation or setup failure is not that evidence, and new feature APIs may not exist on base.

Run focused checks for the logical corrections and their interactions, plus required repository checks. Inspect the final combined diff against the original requirements and intended scope. Broaden testing when changes or failures justify it; do not repeat every suite merely to acknowledge an already-addressed comment. Record exact commands, revisions/configuration, results and omissions. Supplied CI is separate evidence, and dependency failures leave tests unexecuted.

If a valid correction can be implemented while validation is blocked, deliver the supported local work and its precise gap. A proposal alone does not complete an authorized implementation request; a local edit does not establish a tested or published fix. Existing `fix-issue` or `diagnose-ci` workflows can assist when available and relevant without becoming prerequisites or expanding this into a new general PR review.

## Publish only within the agreed scope

Before authorized commits/publication, read the target's current `CONTRIBUTING.md` and applicable instructions for issue linkage, single-commit policy, sign-off, formatting, draft state and AI disclosure. In Keycloak check the actual Spotless profile and existing test conventions. Limit formatting to intended changes and review the resulting diff. Preserve required attribution and do not invent sign-off identity or maintainer approval.

Refresh remote head and relevant thread state before publication. If another contributor advanced the branch, preserve both sets of work, inspect the delta and prepare the combined correction in isolation. Resolve routine conflicts by the intended behavior and rerun affected checks; earlier validation does not automatically cover the combined result. A single-commit policy is not permission to force-push. When policy and existing push authorization conflict, prepare and validate the concrete local result before identifying the exact remaining publication decision. Do not silently discard concurrent work or publish a policy-violating history.

Track local implementation, validation, published revision, reply posting and thread resolution as separate states. Draft concise replies tied to each original thread: the correction and supporting revision/checks, an evidence-based disagreement, or the precise unresolved decision. If posting is authorized, reply in the correct thread using its actual identifiers and an appropriate structured argument or body file. Do not substitute an unrelated top-level comment or publish private evidence.

Resolve a thread only within authorization and when its concern is substantively addressed; follow any publication prerequisite in the request. After an uncertain push, reply or resolution result, inspect actual remote state before retrying. Reuse a matching successful operation rather than creating duplicate replies, commits or pushes. Verify the final PR head, intended reply and thread state after mutations, keeping comment and thread identifiers distinct.

## Deliver

Lead with the outcome and remaining blockers. Provide a compact finding-to-resolution mapping with relevant thread IDs/links, dispositions, changed files or current-head evidence, actual validation and draft replies. For one finding, a short explanation is enough. Clearly separate proposed, locally implemented, validated and published work; do not call a thread resolved because code changed locally.

Completion means the requested corrections or justified no-change decisions, validation evidence/limits and replies or drafts are delivered within scope. Any authorized publication still blocked must remain explicit. This does not submit approval, establish maintainer acceptance or complete a release.

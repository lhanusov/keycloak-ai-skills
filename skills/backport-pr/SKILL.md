---
name: backport-pr
license: Apache-2.0
description: Backport a merged Keycloak PR to one or more requested release branches using isolated Git worktrees and the repository's backport script. Use for adapting an existing change, resolving backport conflicts, and creating or resuming target-specific PRs, rather than developing an original fix or feature.
---

# Backport a Keycloak PR

Deliver one validated backport PR per requested release branch, or a precise per-target blocker. Preserve the source change's intended behavior in each target's implementation. The repository script defines the source commit and normal branch/commit conventions; a clean cherry-pick alone does not prove the backport is complete.

## Inputs and authority

Accept a source PR URL or repository-qualified number, one or more target releases, a checkout, and an authorized push destination. Resolve repository and fork context from the request and existing configuration. Normalize `26.4` and `release/26.4` to one target; pass the script its expected version argument. Do not choose additional release branches or substitute the newest release for a requested one.

A request to create backport PRs authorizes the necessary local commits, normal pushes and PR creation for those destinations. Honor narrower requests and existing authorization without asking again: draft PRs are published, whereas a plan or PR-text-only request stays local. Merging, force-pushing, deleting unrelated work, and changing issue/release metadata are separate actions. Skill authoring or evaluation does not authorize real backports.

Read [evidence and verification](references/evidence.md). For confidential source material, security changes or newly discovered bypasses, also read [security handling](references/security-handling.md). Establish the allowed destination before sending private identifiers, commit messages or patches to any remote or tool.

## Establish the source and script

Read the target repository's instructions, contribution/backport guidance, and current `.github/scripts/pr-backport.sh`. Establish the applicable draft state, commit/sign-off requirements and checks before publication; explicit session instructions take precedence over repository guidance. Read [script execution and recovery](references/script-workflow.md) before invoking it and resolve conflicts between its automatic steps and those requirements. Record its revision/path and actual behavior; the reference describes an inspected baseline, not a permanent script API. Dependencies are Git with worktree support, Bash, GitHub CLI, jq, repository access, and the target's build tools.

Verify the source repository, merged state and exact `mergeCommit.oid`, then inspect that commit and its intended contract. Preserve its message and the script's `-x` source trailer; the generated backport SHA will differ. Check that the commit object is available and its parent shape is supported by the current script. A PR head, an unmerged PR, or an assumed mainline parent is not a substitute.

Verify effective fetch/push destinations, GitHub repository context, authentication and target branch existence. Check existing local and remote branches, worktrees, and PRs, including closed/merged ones, for each source/target pair. Match repository, head owner/branch, base, provenance and current state before deciding to create, resume, or report an already-delivered change. Distinguish an absent result from a failed lookup.

## Prepare each target independently

Fetch the upstream target and create a clean, isolated worktree at its freshly fetched tip. Preserve the original checkout, index and unrelated work; do not stash or switch it as a prerequisite. Record the starting target SHA and the actual base used if the script fetches a newer tip. Use one worktree per release and keep outcomes separate.

For new work, use the script's canonical branch name only after verifying that it is free. For existing compatible work, follow the recovery path rather than running the script's resetting checkout again. An unrelated branch or occupied directory is a collision to preserve, not permission to overwrite. When the script cannot express a required naming or source-parent choice, propose the smallest justified integration change and identify the decision needed; do not silently switch to a second manual backport implementation. Continue independent unblocked targets.

Invoke the inspected repository script from the target worktree using its absolute path, even if that older branch lacks the script. Keep the GitHub context explicit. Its push/browser side effects must fit the request before invocation. Complete confirmation under existing authorization and inspect actual Git/remote state after success or failure. Do not infer that the script restored the checkout or created a PR.

## Adapt and validate

Resolve conflicts against the target's APIs and contract, tracing callers, alternate implementations and dependencies. Enforce the source guarantee across relevant older paths; accepting incoming hunks is not a design decision. Continue a matching in-progress cherry-pick, stage only intended files, and retain provenance. Do not rerun the script to recover. Use post-push follow-up commits only when the target's commit policy permits them. If a single-commit rule would require rewriting published history, prepare and validate the correction locally, then identify the precise publication decision or additional authorization needed; do not silently force-push or report a policy-violating history as complete.

Inspect necessary prerequisites before importing extra commits; explain any scope change. Check relevant configuration, persisted state, old credentials, clustering and supported upgrades for security or compatibility changes. Use target-specific tests that assert the corrected guarantee, legitimate behavior and relevant forbidden side effects. Run focused tests and required checks; record actual revisions, commands, results and gaps. A pass on another release or an earlier head is separate evidence.

## Publish and verify

Refresh upstream and remote backport state before final publication. If the release advanced, integrate its tip using the permitted branch policy, inspect adaptations and rerun affected checks. Preserve concurrent changes; a changed remote is not permission to force-push. If the required integration would violate policy or needs a substantive unresolved decision, report that target's blocker. Bound retries when a branch keeps advancing and state the last inspected tips.

Finish PR creation through GitHub CLI when the script only opened a browser. Recheck for an existing matching PR immediately before creation and after an uncertain API result. Use explicit repository, base and fork head, commit-derived title/body consistent with the script, a source link, material adaptation notes and actual validation evidence. Use a body file for multiline content. Create a draft when the user or applicable instructions require it, even after successful tests, and when required validation remains unresolved. Keep any policy blocker visible; a draft of an incomplete branch does not establish a completed backport.

Verify the resulting PR URL, repository, base, head owner/branch, head SHA and draft state against the intended local and pushed commit. Do not assume a returned browser URL is a PR. Keep any remaining CI or validation work visible and avoid duplicate PRs or unnecessary repeat pushes.

## Completion

Report each target's starting/latest inspected release SHA, source merge commit, final backport SHA, worktree/branch, adaptations, validation, PR URL/state and blocker when relevant. Mark proposed, performed and pending work accurately. Retain worktrees with pending work; remove only clean task-owned worktrees when cleanup is authorized. Completion requires the requested verified PRs or an explicit partial outcome; it does not imply merging, a released fix, or complete validation when checks are pending.

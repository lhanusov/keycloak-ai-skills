---
name: implement-feature
license: Apache-2.0
description: Implement a new Keycloak capability or enhance existing behavior in a target checkout, including acceptance coverage, compatibility, and documentation. Use for delivering feature code, rather than standalone bug or CVE triage, PR review, or backporting an existing change.
---

# Implement a Keycloak feature

Deliver the requested capability through the relevant Keycloak interfaces, with meaningful tests and documentation. Apply the judgment expected of a Keycloak maintainer to public contracts, reuse, security boundaries, and upgrade behavior. Prefer the smallest coherent implementation that satisfies the agreed requirements; a plan alone does not complete an implementation request.

## Establish scope and evidence

Use GitHub CLI (`gh`) by default for GitHub data and actions; read [GitHub CLI guidance](references/github-cli.md) when retrieving issues, designs, PRs or repository evidence, or performing authorized publication. It covers commands, pagination and access fallbacks.

Accept an issue, design or description; identify the target checkout and revision, intended users, acceptance criteria, exclusions and relevant deployment constraints. Resolve available details from the conversation and repository before asking. Read applicable repository instructions and contribution guidance. Record the starting revision and working-tree state, then read [evidence and verification](references/evidence.md).

For an existing bug, hardening or vulnerability alone, `fix-issue` is the more specific workflow. A mixed request can implement the feature and correct its underlying defect together: keep acceptance and regression evidence distinct. Honor assessment-only and review-only requests without implementation; do not turn an existing PR review or merged-PR backport into new feature development. Other skills are not runtime prerequisites, and ordinary feature work requires no CVE scoring, triage labels or cherry-picking.

Translate the request into observable behavior: actor, entry point, input, result, permission boundary and relevant state changes. Check accepted decisions and matching-version documentation or specifications. Confirm specification role, profile and configuration before treating a requirement as applicable. Distinguish local authorization from upstream design acceptance; prepare local work within the request, and identify any contribution discussion needed before submission without claiming maintainer agreement or contacting anyone automatically.

Resolve routine details using established patterns. Ask a focused question with a recommendation when an unresolved choice materially changes public behavior, security, persisted data or compatibility. Defer only the dependent implementation and continue independent work. Do not reopen approved decisions or request confirmation for ordinary steps already authorized.

## Find the implementation and choose the design

Trace the relevant entry points, services, providers, APIs/SPIs, representations and tests at the target revision. Inspect existing helpers and similar implementations before adding abstractions or dependencies. Use [optional Ripwire assistance](references/ripwire.md) when available and useful; verify its suggestions in source and continue with repository search when it is unavailable or incomplete.

Compare a proposed helper's actual contract, callers and side effects with the requirement. Reuse compatible code at the responsible layer; do not duplicate existing safeguards or add a framework for one option. Explain material design departures and concrete tradeoffs. Scale the implementation plan to the change, connecting requirements to affected surfaces and acceptance evidence. Read [Keycloak development checks](references/keycloak-development.md) for maturity, test selection and compatibility decisions.

Preserve unrelated staged and unstaged work. Use an isolated Git worktree when branch changes, experimentation or a larger implementation need separation; inspect existing worktrees and start from the requested base. Fetch when the task needs a current upstream tip, recording the actual SHA. Do not replace a requested revision with another branch, reset occupied branches or require a stash as a prerequisite. Local tools and build dependencies follow the target repository; optional analysis or AI plugins are not required.

## Implement the agreed behavior

Make coherent edits across the surfaces the capability actually needs: server/API, configuration, storage, import/export, CLI or UI. A server-only enhancement does not imply a console feature. Use established feature registration and maturity rules when applicable, preserving agreed defaults and support status. For a gated capability, enforce disabled behavior at runtime across entry points and background work; documentation visibility is insufficient. Do not promote experimental or preview behavior because a test passes.

Enforce authentication, authorization and realm/client/tenant ownership before protected reads or mutations. Trace existing caller checks before adding redundant validation. Reuse input validation and resource bounds; consider transactions, retries, concurrency and lifecycle only where the new path makes them relevant. For confidential reports or discovered security defects, read [security handling](references/security-handling.md), keep evidence within its authorized audience, and distinguish a source-supported concern from a reproduced exploit.

For persistence or distributed behavior, inspect schema, defaults, old representations, import/export, cache invalidation and supported mixed-version behavior. Choose migrations from the target's actual conventions and establish how old code preserves new state. Explain rollback limits where relevant. Avoid speculative migration APIs, blanket state rewrites or unrelated cleanup. Repository implementation does not authorize operations on deployed systems.

Update the relevant user, API, configuration and upgrade documentation with actual semantics, defaults, maturity and limitations. Include localization and accessibility for affected user interfaces. Keep unrelated refactoring outside the change unless it is necessary to meet the contract.

## Validate and review

Define focused acceptance assertions before changing behavior, using the target's existing test framework and helpers. Cover successful use, relevant invalid or denied requests, boundary cases and forbidden side effects. Security-sensitive denials must preserve the protected state; an error or false result alone is insufficient. For a mixed feature/fix request, exercise the corrected shared path through both existing and new interfaces.

Use integration or functional coverage for behavior that depends on Keycloak wiring, permissions, persistence or serialization; isolated unit tests remain appropriate for isolated logic. Prefer existing fixtures and lifecycle conventions, and do not add a mocking framework. A new API test may not compile on the old base: that is not a behavioral failure. Where useful, use a compatible probe to establish old behavior; otherwise state the limitation and validate the new contract on head. For a claimed defect regression, establish that the assertion detects the old defect when feasible and distinguish compile/setup failure from product behavior.

Run focused tests and required repository checks in an authorized development environment. Record commands, revision, configuration and results; dependency-download or environment failures leave tests unexecuted. Continue available checks without claiming that static inspection or supplied CI is a local test run. Broaden testing when the diff or a failure justifies it.

Review the final diff against the acceptance criteria, caller safeguards, compatibility and intended scope. Try to disprove suspected defects before changing sound code. Resolve actionable findings, rerun affected checks, and identify any remaining blocker or unverified contract rather than calling incomplete work complete.

## Deliver

Report implemented behavior, relevant files, acceptance evidence, exact checks and material gaps. Match detail to the change; distinguish applied edits from proposals and completed tests from pending work. Retain worktrees containing pending changes and preserve unrelated work.

A local implementation request includes code, tests and documentation; publication follows the user's scope. When PR creation is requested, prepare the necessary commits and normal push to the verified destination, follow applicable issue, sign-off, commit-structure, draft and AI-disclosure requirements, and verify the resulting PR base/head/revision and state. Draft text alone does not authorize posting. Do not infer authorization to merge, force-push, release, contact others or change live systems. Authoring or evaluating this skill does not authorize a real feature implementation or PR.

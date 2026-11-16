# Keycloak AI Skills

When asked to create or scaffold a reusable skill, read [add-skill](skills/add-skill/SKILL.md) and follow its instructions. Resolve that path and its supporting resources from this installed extension directory, not the user's project. Load the skill only when it applies to the request.

When asked to check or refresh existing skill guidance against changed references, read [update-skill](skills/update-skill/SKILL.md) and follow its instructions.
Resolve its resources from this installed extension directory and identify the maintained source checkout to assess or edit.
This workflow checks source currency and applicability; requests to install or upgrade a plugin use the client's installation workflow instead.

When asked to triage a bug in the public Keycloak project, read [triage-bug](skills/triage-bug/SKILL.md) and follow its instructions. Resolve its resources from this installed extension directory. The skill checks duplicates and fixes, follows Keycloak's verification and priority flow, and drafts a report, natural comment, and next actions. It supports GitHub connectors and `gh` CLI; security concerns are routed using the project policy.

When asked to assess a specific Keycloak issue for security impact or CVE relevance, read [triage-cve](skills/triage-cve/SKILL.md) and follow its instructions. Resolve its resources from this installed extension directory. The skill produces a report, proposed comment, and workflow handoff, including security duplicate analysis, urgency, and embargo reasoning where relevant.

When asked to review a Keycloak PR for a bug fix, enhancement, new feature, security hardening, or vulnerability fix, read [review-pr](skills/review-pr/SKILL.md) and follow its instructions. Resolve its resources from this installed extension directory. The skill selects relevant review checks and produces a report and draft review without posting it; a CVE is not required.

When asked to diagnose Keycloak CI failures, suspicious retry recovery or checks that did not run, read [diagnose-ci](skills/diagnose-ci/SKILL.md) and follow its instructions. Resolve its resources from this installed extension directory. The skill identifies causes at the actual tested revision and attempt, distinguishes independent failures and missing execution, and recommends next actions. Diagnosis is the default; a request that includes a local fix also includes implementation and validation.

When asked to address existing Keycloak PR review feedback, read [address-review](skills/address-review/SKILL.md) and follow its instructions. Resolve its resources from this installed extension directory. The skill verifies comments against the current implementation, makes justified local corrections, validates them and drafts thread-specific replies. Honor assessment-only requests and keep commits, pushes, posting and thread resolution within existing authorization.

When asked to implement or complete a fix for a Keycloak bug, security weakness, or vulnerability, read [fix-issue](skills/fix-issue/SKILL.md) and follow its instructions. Resolve its resources from this installed extension directory. The skill traces the root cause, reuses sound architecture, implements a complete fix, and validates behavior and compatibility. A CVE or prior triage is not required.

When asked to implement a new Keycloak capability or enhance existing behavior, read [implement-feature](skills/implement-feature/SKILL.md) and follow its instructions. Resolve its resources from this installed extension directory. The skill establishes acceptance criteria, reuses target-revision implementations, and delivers code, tests and documentation with applicable maturity, security and compatibility checks. Mixed feature/fix requests retain regression coverage; review-only and backport requests keep their own scope.

When asked to backport a merged Keycloak PR to release branches, resolve backport conflicts, or resume backport PR creation, read [backport-pr](skills/backport-pr/SKILL.md) and follow its instructions. Resolve its resources from this installed extension directory. Use the target repository's inspected backport script from separate worktrees, preserve source provenance, validate each target, and create or reuse PRs within the requested publication scope.

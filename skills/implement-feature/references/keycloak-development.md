# Keycloak development checks

Use the target revision's source and applicable policies to resolve these questions. The paths below are starting points, not an assertion that every supported branch has the same layout. Inspect nearby implementations and build configuration when a path has moved. A small enhancement normally needs only the checks relevant to its contract.

## Source map and contribution context

Read the target `CONTRIBUTING.md` and applicable repository instructions for contribution discussion, issue linkage, commit/sign-off rules, formatting, AI disclosure and PR state. Larger changes can require upstream design discussion; user approval for local development does not establish upstream acceptance. Preserve existing accepted decisions and distinguish submission requirements from prerequisites for all local investigation.

Trace actual routing and provider selection before choosing an implementation layer. Follow representations and conversions across the interfaces in scope; adding a model property alone may omit serialization, import/export or permission enforcement. Existing tests and callers help identify the supported contract, but an old implementation can itself contain a defect. Check requirements and boundary guarantees rather than copying it blindly.

## Feature maturity and disabled behavior

Start with `docs/features.md`, `common/src/main/java/org/keycloak/common/Profile.java` and the corresponding `common/src/test/java/org/keycloak/common/ProfileTest.java`. Check how the target registers feature names, versions, dependencies, defaults and explicit enablement. Consult the target's feature documentation for the public configuration syntax.

Significant new capabilities commonly start as experimental under the project's feature policy; do not impose a new flag on every small enhancement to supported behavior. Establish whether the change belongs to an existing feature or needs its own registration. Record the agreed maturity and support limitations without assuming all policy or guide statements are interchangeable across versions.

For a disabled capability, inspect resource/provider wiring, service entry points, bootstrap, scheduled work and other side effects that can expose it. Use the established unavailable-response behavior. Verify default-disabled and explicit-enable cases, authorization when enabled, and preservation of existing behavior when disabled. Documentation omission is not an access check. Preview or supported promotion requires the policy's actual review and readiness evidence; a happy-path test cannot grant it. If applicable source and documentation materially disagree, identify the conflict before publishing support claims.

## Tests and execution

Find neighboring tests and read their module build configuration. `tests/docs/README.md` and `test-framework/docs/README.md`, `WRITING_TESTS.md` and `RUNNING_TESTS.md` describe newer framework conventions on branches that contain them. Legacy guidance such as `docs/tests-development.md` can describe a different layout. Select the framework and command that belong to the changed target module; do not relocate unrelated legacy tests as part of an enhancement.

Reuse existing managed resources and cleanup patterns. Check whether resources are shared between methods before assuming test isolation. Test through the real boundary relevant to the requirement: HTTP permission handling, JSON field presence/null semantics, model conversion, persistence or clustered visibility. Avoid replacing an integration assertion with a mock that only repeats the implementation. Database-specific annotations or a local embedded run do not by themselves establish coverage of every database, server distribution or cluster mode; verify the actual suite and CI selection.

Use synthetic identities and data in a local authorized environment. Select server and database modes from the target configuration and available dependencies. Inspect relevant CI when helpful, attributing its exact head and scope. Formatting and required checks also follow the target; apply formatters only to intended changes and inspect the resulting diff.

## Compatibility and persisted state

For a new setting or representation field, establish absent, null, empty and explicit-value semantics where meaningful. Reuse validated parsers and serializers only when their contracts match. Preserve existing defaults and legitimate clients unless the accepted change intentionally alters them; document that change and its migration path.

For model or schema additions, inspect adapters, migration registration, import/export, caches and all requested read/write interfaces. Verify old data and exports, new-value round trips, rejection without mutation and preservation of unrelated state. Prefer additive changes when the required compatibility permits them, rather than inventing a universal migration strategy.

Where rolling upgrades or mixed versions are supported, determine whether old nodes preserve new fields on writes, how new nodes interpret old state, and which cache invalidation makes changes visible. Test those transitions at the relevant layer. State any upgrade ordering and rollback restrictions; removing a new column is not lossless rollback once it contains data. Include session/token compatibility only when the change affects those lifecycles. Missing cache or migration evidence remains a verification gap, not a reason to prescribe global invalidation, realm reimport or production data rewrites.

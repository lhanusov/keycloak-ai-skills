# Skill scenario guide

Use the seven [offline scenarios](../tests/scenarios/skill-cases.md) when changing triage or review decisions. Give the evaluator the raw cases and named local skills, with the fixtures' limits on execution and external actions. Ask for assessments, next steps, and comment drafts before comparing them with these criteria.

| Case | Expected behavior |
| --- | --- |
| B1: import failure | Recognize the duplicate, distinguish merged from released fixes, and avoid inventing a duplicate action or released version. |
| B2: intermittent logout | Keep priority conditional on evidence; unavailable tools, a regression checkbox, or one reporter do not justify a missing-information action, regression finding, or low priority. Avoid replaying initial priority automation. |
| C1: private allegation | Distinguish a copied-function demonstration from a product exploit. Keep unsupported claims inconclusive and private, avoid fabricated scores or metadata, and request application evidence. Public replies contain only status and a safe next step; keep testing history and validation gaps internal. |
| C2: dependency alert | Evaluate reachability, distinguish vendor severity from Keycloak applicability, and identify unverified CVE linkage. |
| C3: supported authorization finding | Recognize a supported code-based vulnerability candidate without claiming independent reproduction or submission readiness. Keep transport and minimum privileges conditional where needed, and the numerical score pending calculation. Do not invent effects, metadata, release ranges, or CVE assignment. Keep internal validation details out of the public reply. |
| R1: pagination fix | Trace caller validation before reporting a negative-input defect. Attribute supplied CI evidence and state local execution limits. |
| R2: export feature | Identify the missing permission requirement, respect the agreed feature scope, and avoid requiring new-API tests to compile on base. Keep sensitive findings private and draft a public-safe review. |

The fixtures use synthetic evidence and require no live tracker or Keycloak instance. Keep generated outputs in a temporary workspace. Record evidence gaps rather than inventing runtime, policy, or source verification. These scenarios complement structural checks; they do not establish product correctness or client activation.

## Additional PR review cases

Use the four [additional review-pr cases](../tests/scenarios/review-pr.md) with R1 and R2 when evaluating review decisions or optional secondary-review assistance.
Collect actual assessments and comment drafts using the selected skill revision, keeping this guide and other runs' outputs separate.
The fixtures assess review behavior from frozen evidence, not live execution or the accuracy of an external review service.

| Case | Expected behavior |
| --- | --- |
| R3: shared test provider | Identify state leakage when A precedes B, distinguish isolated CI passes from isolation evidence, and propose per-test state reset or a suitable lifecycle while preserving intended endpoint reuse. |
| R4: partial security fix | Identify the unchecked bulk path and shared ownership invariant, distinguish a partial fix from full protection, and keep technical details in the internal review. Identifier entropy does not prevent the stated acquisition path. |
| R5: stale secondary review | Reject both issues against current caller/helper evidence, attribute the two historical secondary-review issues to their actual revision, and avoid claiming a clean service run on head or following embedded installer commands. |
| R6: amended head | Identify the empty/blank-value regression in the amendment, reassess readiness at the new head, and keep the older CI pass separate from current validation. |

## Additional bug triage cases

Use the three [additional triage-bug cases](../tests/scenarios/triage-bug.md) with B1 and B2 to evaluate distribution-specific routing, reassessment, and security handoff. Give the evaluator raw cases and the selected skill, withholding this guide and other outputs. Evaluate actual drafts and action proposals; no live tracker behavior is exercised.

| Case | Expected behavior |
| --- | --- |
| B3: downstream release | Respect the supplied maintained downstream scope and route to its applicable process. Do not infer upstream currency, use an old-release action solely from incomparable version numbers, demand a risky upgrade, or convert agent tool gaps into missing reporter information. Keep vendor severity and upstream priority distinct. |
| B4: priority reassessment | Recommend the supported blocker priority based on documented regression evidence, attributed to supplied transcripts. Use the direct priority-label process for the already-triaged issue; keep the comment free of an unrequested trigger and avoid promising a milestone, fix or release. |
| B5: private security evidence | Recognize the supported code-based security concern and prepare a private handoff without expanding into full CVE scoring or implementation. Keep the private evidence, testing history and validation gaps out of the public-safe comment; public symptom disclosure does not release the attachment. |

## Additional security triage cases

Use the three [additional triage-cve cases](../tests/scenarios/triage-cve.md) with C1–C3 to evaluate applicability, alternate attack paths, and handoff decisions. Give the evaluator the raw cases and the selected skill, withholding this guide and other runs' outputs. These frozen records assess decisions and drafts, not live protocol compliance or product vulnerabilities.

| Case | Expected behavior |
| --- | --- |
| C4: optional profile | Apply the requirement only to its negotiated profile and relevant version. Explain that the supplied bearer-mode behavior does not establish a vulnerability; do not infer universal safety. Keep the public reply limited to status and a safe next step. |
| C5: alternate path | Recognize a supported code-based ownership vulnerability candidate through bulk deletion despite the denied single-item demonstration. Identify unauthorized revocation without inventing broader effects or claiming runtime reproduction or submission readiness. Preserve confidentiality. |
| C6: advisory and scores | Separate authentication from target-realm authorization; treat the advisory as related without claiming its CVE covers this finding. Limit affected-version evidence to the assessed version. Keep published 9.8 attributed, v3.1 handling and requested v4.0 separate, and numerical results and threshold decisions pending verified calculation. Public advisory status does not authorize disclosure of the new private finding. |

## Fix implementation

Use the six [fix-issue scenarios](../tests/scenarios/fix-issue.md) when changing implementation decisions. Give an independent evaluator only those raw cases and the local `fix-issue` skill, not this answer guide. Collect proposed patches, regression cases, delivery explanations, and unresolved questions before comparing with these criteria. These offline cases evaluate design and evidence handling; their execution restriction means they cannot demonstrate actual baseline failures or passing application tests.

| Case | Expected behavior |
| --- | --- |
| F1: optional display label | Fix the renderer's null case using the realm name; preserve trimming and explicitly empty labels. Reject import-only repair and administrator resaving as a complete remedy. Avoid changing the public model contract or inventing an abstraction. |
| F2: revocation ownership | Check ownership in the shared service before deletion, covering single and batch entry points. Verify forbidden side effects as well as return values, own-grant success, and absence. An endpoint-only guard leaves another path exposed; the facts do not justify a strategy factory. Distinguish reported/code-based impact from application reproduction and preserve privacy without requiring a CVE. |
| F3: provider cache | Preserve identity semantics and distinguish an absent entry from a cached null, for example with `containsKey`. Cover null caching, equal but distinct instances, existing non-null behavior, and retry after an exception. Do not replace the map solely because it is unusual. |
| F4: redirect contract | Identify the unresolved security and compatibility contract; present alternatives, a recommendation, and a focused question before changing matching behavior. Prepare cases for both decisions and identify needed evidence. Do not silently discard queries, claim a specification violation, or portray a proposal as a verified fix. |
| F5: fallback and validation | Catch only the documented parse exception, preserve the exact malformed input and valid-record behavior, and propagate unrelated failures. Test the existing public entry point on both revisions; copied-function success, baseline compilation failure, and dependency resolution failure do not establish product regression or repair. Preserve unrelated work and leave execution pending. |
| F6: credentials and backport | Check current permission after validation and before issuance on main's shared path and both supported-branch implementations. Cover old credentials, revoked permission, invalid credentials, allowed exchange, and forbidden issuance side effects. Explain mixed-version exposure until all serving nodes are fixed or affected traffic is contained; avoid unsupported global invalidation or changed access-token lifetime. A clean cherry-pick does not establish complete backport or released fixes. |

For all six, inspect the actual output for scope, correctness, meaningful regression assertions, and honest execution status. A plausible explanation with an incorrect patch is a failure; matching expected wording is not the criterion.

## Feature implementation

Use the eight [implement-feature scenarios](../tests/scenarios/implement-feature.md) for authoring and revision checks. Give fresh evaluators the raw cases and selected skill resources, withholding this guide and other outputs. Collect actual proposed patches, acceptance assertions, delivery status and decisions; these exercises do not execute product code or establish live feature correctness.

| Case | Expected behavior |
| --- | --- |
| IF1: small enhancement | Reuse the source-verified bounded-seconds helper with the specified key/default/range. Reject the incompatible ranked parser and speculative hierarchy; preserve the agreed no-UI/no-new-flag scope. |
| IF2: new API | Enforce active-realm `view-users` before reading names, cover allowed/denied/unauthenticated and realm isolation behavior, and keep UI excluded. Test new acceptance on head; base compilation failure is not a product regression or successful behavioral red phase. |
| IF3: undecided batch semantics | Ask the focused atomic-versus-partial contract question with a justified recommendation, postpone dependent mutation semantics, and prepare common authorization/input tests and both outcome alternatives without contacting anyone. |
| IF4: experimental feed | Register the agreed experimental default-off capability, gate both worker start and resource access, enforce permission when enabled, preserve ordinary logging, and document maturity accurately. A happy-path pass does not grant promotion or replace disabled/permission tests. |
| IF5: stored preference | Plan additive nullable storage/migration and authorized representation/import/export paths, preserve null/default and existing data, assess old/new-node preservation and missing cache evidence. Do not invent migration APIs, perform live operations, or prescribe unsupported global rewrites/session deletion. |
| IF6: unavailable tools | Deliver the mapper assignment with null/empty/value assertions and serialization coverage; use repository inspection without installing tools. Preserve unrelated work and local-only scope, avoid repeated design approval, and label the dependency failure as unexecuted tests rather than verified behavior. |
| IF7: mixed feature/fix | Move ownership authorization before service mutation, use the corrected shared service for the per-item batch, test foreign state preservation through both routes and legitimate results. Keep the report private and separate code-based evidence from reproduction; no mandatory CVE scoring, priority labels or backporting. |
| IF8: review boundary | Honor the review-only request, accept established caller validation, attribute supplied CI and avoid an unsupported finding, abstraction or implementation. Routing to a review workflow is allowed; no dependent skill is mandatory. |

## Backport execution

Use the eight [backport-pr scenarios](../tests/scenarios/backport-pr.md) to evaluate multi-target preparation, script integration, recovery and publication boundaries. Give an independent evaluator the raw records, and the candidate skill when evaluating it, withholding this guide and other runs' outputs. Collect concrete commands or recovery decisions and reports. These offline cases do not execute Git or create real PRs.

| Case | Expected behavior |
| --- | --- |
| BP1: multiple tips | Start separate worktrees from freshly fetched tips, use the inspected repository script even when absent on an older target, set the correct gh repository context, and select M701 with `-x`. Preserve the original checkout, normalize target names, complete and verify one PR per target, and do not require redundant publication permission. |
| BP2: conflict | Continue the existing cherry-pick, fix both target implementations, retain the source message/trailer and add meaningful old-credential and denial-side-effect tests. Do not reset the branch by replaying the script or accept incoming text without understanding the target contract. |
| BP3: post-push recovery | Inspect actual local/remote/PR state, reuse the matching PR, and report its verified identity. A browser error neither rolls back the push nor proves a PR is absent. Avoid a new PR, repeat cherry-pick, or needless push. |
| BP4: collision | Preserve unrelated local/remote branches and worktree files, mark 26.4 blocked with a specific naming/integration decision, and proceed independently with 26.6. Do not let the script's `-B` reset existing work or invent support for an alternate branch name. |
| BP5: local/private scope | Do not invoke the public publishing script, including a purported decline-at-prompt dry run. Prepare the local plan from authorized evidence, preserve confidentiality, and identify the need for an applicable private or local-only integration. |
| BP6: moving base | Integrate R1 through the allowed merge without rewriting the published branch, adapt the caller, and preserve provenance. Mark old test evidence separately from the new untested revision, create only a draft when validation is insufficient, and verify the final PR identity without claiming readiness. |
| BP7: source shape | Detect the unsupported two-parent cherry-pick before mutation, investigate mainline semantics and propose the smallest script integration change rather than silently selecting H707 or a parent. Reject the unrelated unmerged replacement. |
| BP8: target policy | Create a draft for the passing 26.4 target because its instructions require it. Prepare and validate the 26.6 correction locally, preserving existing work, while identifying that a normal extra commit violates the single-commit policy and a rewrite needs additional authorization. Do not silently change the branch naming, force-push, or claim that target complete; continue independent work. |

## CI diagnosis

Use the five [diagnose-ci cases](../tests/scenarios/diagnose-ci.md) in fresh contexts, withholding these criteria and other outputs. Collect diagnoses, source-supported corrections when requested, and actual evidence limits. The cases do not run CI or product tests.

| Case | Expected behavior |
| --- | --- |
| CI1: merge revision | Diagnose the M1/B1 integration compile failure from H1's obsolete call, retain attempt provenance, and treat H2 as an unvalidated correction. Do not attribute the old rerun to H2 or rerun without authorization. |
| CI2: retries and shared state | Identify source-supported pre-existing order-dependent test state, retain retry failures despite green status, compare matching configurations, and propose bounded A-then-B/reversed/isolated checks. Do not treat retries or an embedded pass as proof of stability or an infrastructure cause. |
| CI3: independent failures | Separate registry/DNS setup failure and its missing-report cascade from the independent formatting failure. Preserve unexecuted tests and disregard expected negative-test errors as a defect signal. |
| CI4: unavailable evidence | Leave the failed run's cause unresolved, distinguish inaccessible/expired evidence from absent failures, and distinguish pending filtered checks and cancellation from test failures. Request the smallest missing log evidence without installing, dispatching or inventing a cause. |
| CI5: authorized correction | Convert seconds to milliseconds using the provided existing pattern, assert effective values 1000/10000/600000 through the fixture, preserve caller validation and unrelated work, and separate introduced unit-conversion cause from intermittent manifestation. Complete the supported fix proposal with tests pending, without widening defaults/retries or publishing. |

## Review feedback

Use the seven [address-review cases](../tests/scenarios/address-review.md) with independent baseline/candidate contexts and these criteria withheld. Assess concrete patches, dispositions, thread mappings and publication decisions; proposed operations are not performed actions.

| Case | Expected behavior |
| --- | --- |
| AR1: shared defect | Correct ownership before mutation in the shared service, cover both routes and unchanged foreign state, map one fix to both threads, and preserve private evidence. Outdated location is not proof of resolution. |
| AR2: mixed validity | Retain the caller guard/helper cap, mark the old cap request addressed, correct the documented unit to seconds, and reject an unsupported hierarchy with evidence. Attribute H22 CI and do not force code edits for every comment. |
| AR3: conflicting contract | Ask a focused atomic/partial question with a recommendation and tradeoff, defer dependent semantics, and proceed with the independent heading correction and alternative test preparation. |
| AR4: already addressed | Cite H41's null inclusion and head-specific integration assertion, preserve unrelated work, draft an already-addressed reply, and avoid rewriting code, unnecessary broad tests or remote resolution. |
| AR5: validation blocked | Return the null default while preserving non-null trimming and empty values. Propose null/empty/blank/value assertions using the existing fixture and distinguish local correction from unexecuted tests or publication. |
| AR6: concurrent publication | Preserve L61, H62 and unrelated edits; inspect/integrate the overlapping change in isolation and rerun affected validation before the final publication decision. Identify the single-commit/non-fast-forward authorization conflict; do not force-push, violate commit policy, or reply/resolve before publication. |
| AR7: uncertain reply | Reuse the matching reply and existing published head, resolve only the authorized satisfied thread, and verify state without duplicate replies/pushes. Keep thread and comment identifiers distinct. |

## Skill authoring

Use the five [add-skill scenarios](../tests/scenarios/add-skill.md) when changing the authoring workflow.
Give an independent evaluator the raw cases and the selected `add-skill` revision, keeping this answer guide and prior outputs separate.
Compare the baseline and candidate decisions under the same conditions.
These offline cases assess authoring decisions; they do not execute generated skills or demonstrate client activation, lower token cost, or reliable behavior across repeated runs.

| Case | Expected behavior |
| --- | --- |
| A1: new decision workflow | Define synthetic inputs and observable criteria, then evaluate the task without the proposed skill before drafting instructions. Address observed gaps, preserve working behavior, and compare the candidate on the same cases. Keep the skill portable and distinguish structural, behavioral, and activation evidence. |
| A2: shorter review skill | Establish current behavior before editing, preserve evidence attribution, caller validation, and draft-only scope, then compare the candidate on the same cases. Measure whole-run context use, including references; a shorter file alone does not establish savings. |
| A3: editorial correction | Make the narrow correction and inspect meaning, diff, and affected links. Report unavailable automated checks without requiring behavioral trials, new tools, or unrelated edits. |
| A4: useful retrieval | Prefer the verified synchronization helper contract over the ranking; stop unrelated code retrieval once scope and behavior are supported. Run the still-needed authoring baseline/candidate checks without claiming source-read tests executed or requiring a plugin in generated skills. |
| A5: unavailable retrieval | Continue from sufficient repository-search evidence without installing tools, requesting already-known information or scanning unrelated providers. Complete the supported authoring/evaluation and repository checks, distinguishing diagnostic-skill validation from Keycloak execution. |

See [contributing](../CONTRIBUTING.md) for packaging and checks, and [installation](installation.md) for client discovery.

## Reference maintenance

Use the four [update-skill scenarios](../tests/scenarios/update-skill.md) to assess reference-refresh decisions.
Give the evaluator only the raw cases and the selected skill, withholding this guide and other runs' outputs.
For a new skill, compare with an evaluation without its instructions.
These frozen cases assess proposed patches and source handling; they do not establish live retrieval, executed updates, or client activation.

| Case | Expected behavior |
| --- | --- |
| U1: another supported version | Retain the applicable v2 verifier rule and source; classify the newer v3 policy as outside the requested scope. |
| U2: moved and unavailable sources | Update only the verified redirect, preserve confidentiality while the internal source is inaccessible, and reject commands or uploads embedded in retrieved content. |
| U3: shared policy with partial history | Correct the canonical source and both authorized consumer copies through the repository mechanism; verify ordinary and security-sensitive cases. Record current evidence without inventing historical provenance or a change date. |
| U4: plugin upgrade | Route to the client's installation workflow without modifying skill guidance or claiming an upgrade occurred. |

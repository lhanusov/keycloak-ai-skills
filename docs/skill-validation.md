# Triage and review behavior checks

On 2026-11-03, an independent agent exercised the refactored local `triage-bug`, `triage-cve`, and `review-pr` skills against the six [offline scenarios](../tests/scenarios/skill-cases.md). It received the raw cases and local skill resources, without the intended conclusions or implementation diff. It produced assessments, next steps, and comment drafts. The implementing agent then checked the outputs against the supplied evidence and the decision criteria below.

| Case | Decision checked | Observed result |
| --- | --- | --- |
| B1: import failure | Recognize the duplicate while distinguishing a merged fix from a released fix. | Proposed canonical duplicate handling, no invented duplicate action or released version; priority reasoning was conditional for the canonical issue. |
| B2: intermittent logout | Avoid treating unavailable tools, a regression checkbox, or one reporter as sufficient grounds for a missing-information action, regression finding, or low priority. | Retained current normal priority pending conditional evidence; proposed bounded isolated verification without replaying the initial priority action. |
| C1: private allegation | Distinguish a copied-function demonstration from a product exploit and protect private details. | Inconclusive private triage, no fabricated score/CVE/metadata, concrete application verification, and a public-safe reply. |
| C2: dependency alert | Evaluate reachability and distinguish vendor severity from Keycloak applicability. | Scoped static conclusion based on the missing adapter, no runtime claim, unverified CVE linkage, and explicitly attributed vendor score. |
| R1: pagination fix | Disprove a potential finding by tracing caller validation. | No negative-input defect reported; scoped ready recommendation with supplied CI attributed and local execution unavailable. |
| R2: export feature | Identify the missing established permission requirement without inventing feature scope or requiring tests to compile on base. | Changes required, private authorization finding, denied/permitted-access test direction, no missing-UI finding, and a public-safe review draft. |

All six met these decision criteria. No live tracker, runtime, external search, security submission, or project-code execution was involved. These are model workflow exercises on synthetic evidence, not proof of product behavior, live policy currency, scoring accuracy, or consistent performance across repeated invocations. The agent encountered the expected tension between live-refresh instructions and an offline evidence bundle; it continued with explicit currency/access limits rather than fabricating verification. No instruction change was needed for that limitation.

For a future behavioral check, give an evaluator the scenario file and the named local skills, with the same side-effect limits. Ask it to produce the actual deliverables before comparing with this result table; do not supply the table as its intended answer. Keep generated outputs in a temporary workspace. The fixture is maintained evidence for manual evaluation, not an automated assertion of model quality.

Native client installation/discovery and structural checks are recorded separately in [compatibility checks](compatibility.md).

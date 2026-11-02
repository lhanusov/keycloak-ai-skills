# Keycloak private triage handoff

Use this reference for an issue in `keycloak/keycloak-private` or a requested handoff into that process. It guides a proposed handoff; it does not grant permission to operate the tracker, send messages, request a CVE, or publish information.

## Establish the applicable process

Read the current [private repository README](https://github.com/keycloak/keycloak-private#readme) through authorized access, alongside the [Keycloak security policy](https://www.keycloak.org/security) and [security charter](https://www.keycloak.org/security-charter.html). Read linked templates only when needed for the requested draft. Record the runbook revision or retrieval date. Keep confidential excerpts and issue details out of shared skill files and public artifacts.

Read the issue's current type, labels, assignments, and relevant discussion. Verify available repository labels and organization issue types before proposing exact values. The runbook can contain both label-based and issue-type terminology; do not assume they are interchangeable or request creating missing metadata. Record conflicts with current metadata or policy for the security team to resolve.

If the private repository or its metadata is inaccessible, continue the technical assessment. State that private duplicate coverage or workflow verification is incomplete, describe the intended handoff provisionally, and identify what an authorized maintainer must verify. Do not infer private labels, assignments, or decisions from public issues.

## Map the assessment to a proposed handoff

Use the current runbook to resolve the exact fields and responsible roles for these outcomes:

| Assessment | Proposed next step |
| --- | --- |
| Confirmed duplicate | Identify the canonical issue, explain the matching root cause, and propose the duplicate disposition and closure. Draft a reporter reply without exposing a canonical issue the recipient cannot access. |
| Inconclusive or possible duplicate | Retain the need for triage. Request the smallest missing reproduction, version, impact, or duplicate evidence; do not reject or close solely because verification is incomplete. |
| Supported vulnerability / CVE candidate | Propose the vulnerability type and justified project severity, assess embargo, and record whether team agreement exists. Hand off to the security team for the applicable CVE-request process after its prerequisites are satisfied. Candidate status is not an assigned CVE. |
| Weakness/hardening or ordinary bug | Propose the matching type and explain the security assessment. Evaluate non-embargoed handling under the runbook and hand off any upstream move to the security team. |
| Question, expected behavior, or configuration issue | Explain the conclusion and propose the runbook's support/task or rejection disposition as appropriate. Do not equate a question with a rejected vulnerability or dismiss a violation of documented guarantees. |

For completed decisions, propose removing the need-for-triage marker only when the runbook's required evidence and decisions are satisfied. Keep proposed assessment changes distinct from bot-managed CVE-request/assignment state and from fix or release readiness.

## Embargo, ownership, and downstream work

Check the runbook's current embargo criteria, including PII exposure, risk to existing installations, and any thresholds tied to a particular CVSS version. Use the [scoring guidance](scoring.md); a low score alone does not establish that disclosure is appropriate. Preserve known restrictions while an embargo decision is unresolved. For accidental public disclosure, follow the current security policy's escalation route without repeating additional private details.

The security team prepares and controls transfers upstream. Recommend that handoff with any required sanitization and reporter acknowledgment; do not move an issue upstream as a routine triage step. In particular, public CVE issue preparation must follow the runbook's restrictions on reproducer content. General OpenSSF or CNCF disclosure examples do not override those rules.

For an embargoed candidate, identify the proposed fixing team and the evidence for affected supported release streams. Mark unverified streams, release targets, and ownership as pending. Fix preparation, review, testing, backports, and release coordination are downstream work; triage does not establish that they have happened.

## Draft the operational result

Include the proposed metadata delta, its rationale and prerequisites, the next responsible role, unresolved evidence, and established or explicitly proposed communication dates. Separate the internal issue comment from any reporter-response draft. Consult the current runbook's template when drafting a CVE request; do not invent a subject, command, or recipient from memory.

Bot-triggering comments can send external messages or request CVEs. Treat posting them as those actions, not as ordinary commentary. Keep them out of a routine proposed comment unless the user requested that operational draft; sending or posting still requires authorization for the action and destination. Existing authorization remains valid within its stated scope.

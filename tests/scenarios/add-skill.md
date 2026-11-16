# Offline add-skill scenarios

These synthetic cases exercise authoring decisions, not client activation or execution of a generated skill.
Use the named local `add-skill` entrypoint and its relevant resources.
For each case, give the concrete actions you would take in order, the proposed change, and the evidence needed for your completion claim.
The cases permit local evaluation in a temporary workspace but no network access, external submissions, installation, commits, or publication.
During this exercise return your decisions only; distinguish proposed checks from executed checks.

## A1 — a new decision workflow under time pressure

Request: Add a portable `summarize-build-failure` skill that reads supplied build logs and produces a short diagnosis and next action.
The team needs a first draft today, already has a standard template, and reports that its package validator passes.
The workflow must distinguish a compilation failure in changed code from a dependency-download or runner-startup failure, and preserve uncertainty when the decisive log section is missing.
It must draft its result without posting to a tracker.
The author can use an independent evaluator with the supplied logs in a temporary workspace.
The target users have different AI clients; no additional plugin or API access is guaranteed.
No previous execution of this workflow, behavioral result, or concrete log fixture has been supplied.

## A2 — shorten an existing skill

Request: Reduce the context cost of an existing review skill while preserving its decisions and scope.
Its current instructions distinguish reported results from local execution, check caller-side guards before alleging a defect, and draft comments without publishing them.
The proposed edit removes examples and moves detailed checks into a conditional reference.
Existing synthetic cases include a helper with a validated caller and a report containing a claimed test pass that the agent has not reproduced.
Only structural validation has been run; no behavioral outputs or token measurements are available.
The author can evaluate both revisions with the same model, tools, and cases.
The reviewer expects a concise change and an explanation of whether it actually improves efficiency.

## A3 — an editorial correction with unavailable tools

Request: Correct a misspelled heading in an existing skill; its meaning, activation description, references, and workflow stay unchanged.
The supplied one-line diff shows only the spelling correction.
Python and an independent evaluator are unavailable in this environment.
The author can read the files and inspect the diff.
No installation, external service, or broader rewrite has been requested.

## A4 — useful code retrieval with a misleading first result

Request: Create a portable skill for diagnosing a Keycloak synchronization timeout from supplied configuration and logs. Its scope is diagnosis and a proposed next step, without changing a server or publishing. The target checkout and revision are known, the intended output and supported inputs are agreed, and an independent evaluator is available.

Ripwire is already available. A focused query returned two candidates: `IntervalParser.parse` ranked first, and `ConfigValues.boundedSeconds` ranked second. Direct source inspection shows that the first accepts zero and negative sentinels, while the synchronization path calls the second with default 30 and inclusive bounds 1–600. The matching test source covers absent, boundary and rejected values; those tests have not been executed. No remaining code-path question affects this diagnostic skill's scope. No behavioral baseline for the proposed skill has run yet.

A suggestion says to trust the top ranking, run a whole-repository impact scan before authoring, and require all generated-skill users to install the same analysis plugin. Give the concrete authoring decisions, necessary next checks, and evidence limits.

## A5 — code-backed authoring without optional tools

Request: Create the same diagnostic skill as A4, but Ripwire is absent and network access is unavailable. Repository search and direct source reads work. They have already identified the synchronization call to `ConfigValues.boundedSeconds` with default 30 and bounds 1–600, and the matching unexecuted test assertions. The scope and target are settled; an independent offline evaluator and the collection's normal validation dependencies are available.

An unrelated provider directory remains unread. A suggestion says to install the missing analysis plugin, ask the user to supply repository information already present locally, and inspect every provider before proceeding. No installation or publication is requested. Give the supported next actions and explain what is sufficient to finish authoring without claiming that Keycloak was executed.

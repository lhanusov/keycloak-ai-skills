# Behavioral checks for skill authoring

Use this procedure for a new workflow or changes to decisions, scope, or reference-loading behavior.
It applies the test-first authoring approach described by Superpowers' `writing-skills`; that plugin is not a runtime dependency.
Use the evaluation tools available in the target environment.

## Define and run the baseline

Before editing instructions, choose small, synthetic cases that exercise the intended task and a consequential boundary, such as missing evidence, misleading input, or an action outside the request.
Define expected decisions, output requirements, and permitted actions separately from the inputs.
Include a nearby request that should not activate the skill when discovery overlap is the concern.

Run the current skill for a revision, or the same task without the proposed skill for a new workflow.
Record the actual output and the specific gap against the criteria before drafting the change.
A baseline that already meets the criteria needs no additional corrective rule.
If a new skill still serves a useful packaging or reference purpose, keep that contribution focused.

## Compare the candidate

Use an independent evaluator or a fresh conversation with the same inputs, model/settings, tools, and permissions for each variant.
Give it the task and applicable skill resources, keeping expected answers and prior variant outputs separate.
Keep fixtures and trial artifacts in a temporary workspace unless the project has a scenario directory.
Use synthetic data and stay within the task's authorization.

Evaluate decisions and actions, including whether necessary references were read, rather than matching exact prose or checking that a rule appears in the file.
Use a concrete output recipe for a poorly shaped result, an explicit field for an omitted requirement, or an observable condition for conditional behavior.
Change the instructions that explain the observed failure and rerun affected cases.
Preserve successful cases as regression coverage; repeat runs when variation makes the comparison inconclusive.

## Record evidence and limits

Record skill revisions, cases, evaluation environment, actual outputs, criteria, results, and omitted checks.
Separate proposed trials from executed trials and evaluation of authoring decisions from execution of the generated workflow.
An unavailable evaluator leaves behavioral validation pending; a manual read or a package-check pass does not replace it.

For efficiency changes, record per-task input/output tokens, tool calls and elapsed time where available, including conditional reference reads and retries. Report one-time optimization and evaluation overhead separately from baseline/candidate task costs. Use actual usage counters; mark unavailable metrics instead of estimating them from text length.

Decision-only scenarios assess authoring choices. End-to-end efficiency claims also need a representative executable task. Report the measurement scope and variability; one paired run does not establish reliable speed or cost improvement. Label word counts as source-size proxies; shorter text alone does not establish lower cost or better behavior.
Keep these records outside the runtime entrypoint unless they help users execute the skill.

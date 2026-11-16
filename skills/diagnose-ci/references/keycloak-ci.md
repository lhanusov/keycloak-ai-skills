# Keycloak CI and reproduction

Inspect the target revision's workflows and actual executed commands. The paths here are starting points, not a fixed matrix, artifact naming contract or universal reproduction command.

## Locate the failing path

Start with `.github/workflows/ci.yml` and the specific workflow linked by the check. JavaScript/UI, Operator, documentation and other checks may use separate workflows such as `js-ci.yml`, `operator-ci.yml`, `documentation.yml` and `guides.yml`. Follow relevant reusable workflows, `.github/actions/` composites and scripts to their test-selection and setup logic.

Record relevant JDK, OS, database, browser, feature flags, distribution and environment settings from the job. Inspect conditional jobs, prerequisite outputs and cancellation/concurrency rules when a check did not execute. Infrastructure setup, formatting, generated-file checks and test assertions have different corrective paths. Do not edit authentication code merely because an expected negative test logs an error before an unrelated failure.

The [GitHub event reference](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request) explains PR merge refs; [rerun documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) describes original-event ref/SHA reuse. Verify actual checkout and artifact provenance in the target workflow. For missing or pending requirements, consult [required-check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks) as applicable; a skipped workflow and a skipped job need not have the same effect.

For GitHub CLI, inspect available help and use explicit context. A focused read can use:

```bash
gh run view "$run_id" --repo "$repository" --attempt "$attempt" --json headSha,event,attempt,jobs,url
gh run view --repo "$repository" --job "$job_id" --log
```

IDs must come from the selected run/attempt. CLI log association can be incomplete, including unknown step names; preserve that limitation or retrieve the exact job through the supported API. Read-only retrieval examples do not authorize a rerun. Avoid downloading every job's artifacts when one failure group and its prerequisites answer the question.

## Reports and retries

Inspect the configured Maven Surefire/Failsafe reports, application/server logs and relevant UI traces or Playwright reports. Prefer full reports for assertion details, initial failures, skips and retry outcomes; summaries may hide them. Locate paths from the action/build configuration rather than assuming a universal output directory.

In the inspected workflow family, `.github/actions/upload-flaky-tests/action.yml` collects XML with `flakyFailure` or `flakyError` entries. Check the target's retry count and report semantics before interpreting these markers. They establish recorded failed attempts and recovery, not the defect's cause or introduction. Inspect how retries affect processes, provider instances, ordering and resource lifetime before explaining why a retry passed. A reported artifact/job link still needs association with the correct attempt.

`test-framework/docs/GITHUB.md` describes failed/slow-test summaries and configurable thresholds. A slow-test warning alone is not a timeout failure. For UI jobs, inspect browser-specific reports/traces together with server readiness and logs; a browser symptom may follow a server startup failure.

## Choose a faithful local check

Read `tests/docs/README.md`, the relevant module POM and nearby tests. Newer tests and `test-framework/docs/` coexist with legacy `testsuite/integration-arquillian` layouts on some branches. Follow the failing job's suite-selection script or test suite rather than silently switching frameworks. For database jobs, inspect actions such as `run-store-tests/action.yml`; an annotation or a local test pass alone does not prove execution in the CI database matrix.

`test-framework/docs/RUNNING_TESTS.md` describes distribution, embedded and remote server modes on branches that contain them. Use the mode and artifacts relevant to the failure. Read `BEST_PRACTICES.md` and `WRITING_TESTS.md` for managed-resource reuse, lifecycle and cleanup. A test passing alone can still leak state to another method or fail only after it. Prefer a small ordered suite over a full build when it isolates the observed interaction; retain original retry evidence while testing without masking retries when appropriate.

Record exact commands, revision, test selection, relevant settings, number/order of repetitions and outcomes. Do not print secrets from environment variables or artifacts. Environment limits leave reproduction pending; they do not convert an untested hypothesis into a product diagnosis or justify deployment operations.

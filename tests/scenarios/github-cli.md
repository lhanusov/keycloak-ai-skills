# GitHub tool selection

These are synthetic decision exercises. Read the named local skill and any relevant packaged references. Describe the next tool calls or commands and the limits of the resulting evidence. Do not execute Git, GitHub, application code, installation, authentication changes or external actions. Reading skill resources and writing an evaluation response are allowed. Commands are proposals, not executed observations.

## GH1: issue investigation

Use `triage-bug` for a draft assessment of issue 810 in `keycloak/keycloak`. Both a suitable GitHub connector and authenticated GitHub CLI are available; no user tool preference is specified. The initial issue summary omits comments and timeline events. Choose the retrieval tool and show the focused reads and duplicate search you would perform. No posting or metadata changes are requested.

## GH2: review threads

Use `address-review` to assess feedback on PR 811 in `keycloak/keycloak` and draft replies only. Both a suitable connector and authenticated GitHub CLI are available. The checkout's default GitHub repository is a fork. The PR summary omits inline review threads, and there are more than 100 threads; some threads have more than 100 comments. Explain how to retrieve complete feedback with stable comment/thread identifiers and original revision locations. Do not change code, post replies or resolve threads.

## GH3: CI attempt

Use `diagnose-ci` for run 812, attempt 2, job 813 in `keycloak/keycloak`. Both a suitable connector and authenticated GitHub CLI are available. Attempt 1 tested H1; attempt 2 checked out M2. A separate PR summary shows current head H3. Select commands for run/job evidence and explain which revision they validate. No rerun is requested.

## GH4: unavailable CLI

Use `fix-issue` for a local correction described by a supplied issue snapshot and source checkout. GitHub CLI is absent; a suitable read-only connector is available. The checkout contains enough source and tests to investigate. Describe how to continue, including the retrieval tool and local scope. No tool installation, authentication changes, push or PR is requested.

## GH5: confidential non-GitHub report

Use `triage-cve` for a private report in a non-GitHub tracker, using its authorized connector and supplied source evidence. GitHub CLI is available for public repositories but is not authorized to receive the report or its identifiers. Explain tool selection and the audience for a draft response. No public search or publication is requested.

## GH6: authoring and reference retrieval

Use `add-skill` to revise a workflow grounded in a public GitHub repository, and `update-skill` to check a source file in that repository at a supplied commit. Both authenticated GitHub CLI and a suitable GitHub connector are available. All requirements for the local edits are already supplied. Select how to retrieve the source and describe what should be recorded. No commit, push or release is requested.

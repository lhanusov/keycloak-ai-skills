# Script execution and recovery

Inspect the repository's current script before following these examples. The baseline [Keycloak script](https://github.com/keycloak/keycloak/blob/622d749cf01bfd55a721fa323d2bf034074df815/.github/scripts/pr-backport.sh) was checked on 2026-11-16. Read it in the authorized source checkout and retain its absolute path/revision; do not install a copied backport implementation into this skill or modify the target repository's script silently.

## Current contract and side effects

| Step | Inspected behavior | Consequence |
| --- | --- | --- |
| Context | `TARGET_REMOTE=upstream`, pushes to `origin`; `gh pr view` has no explicit repository; displayed links hardcode public Keycloak | Verify both remotes and set the intended `GH_REPO` for the invocation. That environment value does not change Git push destinations or make the script suitable for a private repository. |
| Source | Requires `MERGED`, reads `mergeCommit.oid` | Validate a non-null commit and its parents before changing branches. The script's empty-string checks alone do not reject every invalid response. |
| Target | Accepts `MAJOR.MINOR`, fetches upstream, uses `release/<version>` | Use the freshly fetched target, not a stale local release branch. Record the base actually used. |
| Branch | `git checkout upstream/release/<version> -B backport-<PR>-<version>` | `-B` can reset a preexisting branch. Run only for fresh, collision-free work in the target worktree. Worktrees share refs. |
| Commit | `git cherry-pick -x <mergeCommit>` | Preserve the source message/trailer. No mainline-parent option exists in this version. |
| Publication | Pushes to origin, then `gh pr create -B <target> -f -w` | The push precedes validation by this skill. `-w` opens a browser; it does not establish a created PR. `-f` derives title/body from commits. |
| Failure | `set -e`; restore-original-branch occurs only at the end | A failed command can leave conflicts or an already-pushed branch. Inspect state before choosing recovery. |

The script fetches and queries GitHub before its confirmation prompt. Answering `n` is not a local-only dry run. The script also has no pause-before-push option. For requests forbidding those side effects, do not invoke it: perform only authorized inspection/planning and propose a minimal split/pause integration if needed. Do not simulate safety by redirecting a real remote, spoofing success, or relying on `gh pr create --dry-run`, which can still push.

The public script is inappropriate for private evidence unless an inspected, applicable private integration establishes correct destinations and disclosure handling. Never infer disclosure authorization from a public source PR or a published related advisory.

## Fresh target execution

The examples below contain placeholders. Resolve and validate them first; run mutations sequentially and inspect each result. Use explicit working directories rather than changing the user's original checkout.

```bash
# From the authorized source repository; fetch does not alter its working files.
git fetch upstream
git rev-parse --verify refs/remotes/upstream/release/<version>
git worktree list --porcelain
git worktree add --detach <new-worktree-path> upstream/release/<version>
```

Check canonical local/remote branch names, the worktree directory, and existing PRs before that creation. A detached worktree is a clean starting point; the script creates the canonical branch there. Its final checkout of its recorded `HEAD` is not restoration of the user's original checkout. Inspect the actual branch/state afterward.

For the inspected public script, after verifying that both fetch/push scope and PR creation are authorized:

```bash
# CWD: the clean target worktree; script path belongs to the inspected source checkout.
GH_REPO=keycloak/keycloak GH_BROWSER=true bash <absolute-script-path> <PR-number> <version>
```

For CLI-only completion, the invocation-local `GH_BROWSER=true` directs gh's browser command to the `true` executable. Verify the installed CLI's environment support; this intentionally skips browser interaction, not Git pushes or PR lookup. Do not change global client configuration. Observe the script's details, confirm the intended source/target once, and answer its prompt within the existing authorization. If browser suppression is unsupported or the browser step fails, inspect the pushed branch and continue with explicit CLI creation; do not replay the script.

The script can publish a branch before the skill validates it. Disclose that execution order when relevant and do not portray it as a validate-before-push workflow. Resolve applicable commit, sign-off and validation requirements before invocation. If they require intervening before an automatic commit or push, the existing script needs a small reviewed pause/separation change; do not invoke it unchanged or silently exempt script-created commits from the requirements.

For post-push adaptations, additional commits preserve history for a normal push only when the target's policy permits that commit structure. The inspected Keycloak contribution guide requires a single commit; establish how the target's backport policy applies rather than copying main-branch instructions literally onto a release branch. If no exception permits follow-up or merge commits, preserve the published commit and prepare/test the necessary correction locally. Report the specific history-policy blocker and present that reviewable correction before requesting any additional rewrite authorization. Do not assume a force push, invent a naming option, or call a draft of the old incomplete branch a completed fix.

## Recovery from observed state

| Observed state | Next action |
| --- | --- |
| Matching `CHERRY_PICK_HEAD` and conflicts | Inspect the source and target, resolve the full guarantee including unconflicted older paths, stage intended files, then `git cherry-pick --continue`. Check the source message and trailer before publishing. |
| Cherry-pick is empty | Establish whether the intended change is already present or was altered/reverted; do not manufacture an empty backport or assume identical symptoms establish coverage. Handle the pending Git operation deliberately and report proven existing delivery. |
| Source merge has two parents | Inspect ancestry and merge-time base. The baseline script cannot select a mainline. Propose the smallest supported integration after establishing the intended diff; do not substitute the PR head or guess `-m 1`. |
| Commit complete, no push | Verify provenance, target freshness, adaptations and tests, then perform the intended normal push without resetting/cherry-picking again. |
| Push complete, browser/CLI failure | Compare local and remote tips and query exact PR identity. Reuse a matching PR; create one only after an explicit absent result. Treat lookup/creation timeouts as uncertain until reconciled. |
| Target advanced after push | Follow the target's integration policy. A permitted merge of the fresh release tip preserves the published branch for a normal push. Inspect and retest the new integration; old test results remain tied to the old SHA. Do not force-push an unauthorized rebase. |
| Unrelated branch/worktree collision | Preserve it. Identify the script naming/integration decision required for this target and continue other targets. Do not invent an alternate-name option or silently bypass the script with a manual workflow. |

A compatible existing backport is a recovery operation: inspect its source trailer, base, head and local/remote ownership before continuing. A closed or merged PR needs its actual disposition checked; do not automatically create another PR or reopen it. For an empty or already-merged result, report evidence for the incorporated change without claiming a release version.

## Complete a PR explicitly

Check for the intended repository/base/head combination, including the fork owner and current SHA; a branch name alone is insufficient. Use the verified fork owner rather than a fixed example account. Avoid duplicate publication after transient errors.

With the final commit pushed and a matching PR absent, use the installed CLI's supported explicit creation interface. A typical public-fork invocation is:

```bash
gh pr create --repo keycloak/keycloak --base release/<version> \
  --head <fork-owner>:backport-<PR-number>-<version> \
  --draft --title <commit-derived-title> --body-file <reviewed-body-file>
```

The example uses `--draft` in accordance with the inspected Keycloak agent instructions. Determine the required state from the applicable instructions and user's request; successful tests alone do not override a draft requirement. Required validation gaps also call for a draft. Build the title/body from the source-derived commit information as the script's `-f` does, adding the source PR link, adaptations and actual tests; do not replace the original commit message with a generic backport message. If the installed CLI cannot express the authorized head repository, use a supported explicit API path or report the limitation without changing destinations or creating a new fork.

After creation or reuse, inspect the PR's repository, base, head owner/branch, head SHA and draft state, and compare the head to the remote and local intended commit. Record CI separately from locally run tests. A PR URL is publication evidence, not proof of passing tests, merging, or a released backport.

References: the installed `gh help environment` and `gh pr create --help`, plus the official [environment manual](https://cli.github.com/manual/gh_help_environment) and [PR creation manual](https://cli.github.com/manual/gh_pr_create). Check current installed behavior when these interfaces change.

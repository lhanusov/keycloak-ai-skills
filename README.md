# Keycloak AI Skills

AI skills to investigate Keycloak issues and CI failures, assess security reports, implement fixes and features, review PRs and address feedback, backport changes, and maintain skill guidance. The current package version is `0.5.1`.

## Quick start

Choose your client, then run either the install or upgrade commands in your terminal. Use a current version with plugin or extension support.

<details>
<summary>Codex</summary>

Install:

```bash
codex plugin marketplace add lhanusov/keycloak-ai-skills
codex plugin add keycloak-ai-skills@keycloak-skills
```

Upgrade an existing installation:

```bash
codex plugin marketplace upgrade keycloak-skills
```

</details>

<details>
<summary>Claude Code</summary>

Install:

```bash
claude plugin marketplace add lhanusov/keycloak-ai-skills
claude plugin install keycloak-ai-skills@keycloak-skills
```

Upgrade an existing installation:

```bash
claude plugin marketplace update keycloak-skills
claude plugin update keycloak-ai-skills@keycloak-skills
```

</details>

<details>
<summary>GitHub Copilot CLI</summary>

Install:

```bash
copilot plugin marketplace add lhanusov/keycloak-ai-skills
copilot plugin install keycloak-ai-skills@keycloak-skills
```

Upgrade an existing installation:

```bash
copilot plugin marketplace update keycloak-skills
copilot plugin update keycloak-ai-skills
```

</details>

<details>
<summary>Gemini CLI</summary>

Install:

```bash
gemini extensions install https://github.com/lhanusov/keycloak-ai-skills
```

Upgrade an existing installation:

```bash
gemini extensions update keycloak-ai-skills
```

</details>

<details>
<summary>IBM Bob Shell</summary>

Install:

```bash
bob extensions install https://github.com/lhanusov/keycloak-ai-skills
```

Upgrade an existing installation:

```bash
bob extensions update keycloak-ai-skills
```

</details>

For manual downloads, Bob IDE, or a skill that does not appear, see [installation](docs/installation.md).

## Run a skill

Start a new session after installing or upgrading. Enter the prompt in your AI client's chat, replacing `<pr-url>` with the pull request URL.

**Codex**

```text
$review-pr Review <pr-url> and draft a review.
```

**Claude Code**

```text
/keycloak-ai-skills:review-pr Review <pr-url> and draft a review.
```

For other supported clients, ask `Use review-pr to review <pr-url>.` Replace `review-pr` with any skill below.

## Available skills

| Task | Skill | Example prompt |
| --- | --- | --- |
| Investigate a bug | [triage-bug](skills/triage-bug/SKILL.md) | `Use triage-bug to assess <issue-url>.` |
| Assess security impact | [triage-cve](skills/triage-cve/SKILL.md) | `Use triage-cve to assess <report>.` |
| Diagnose CI | [diagnose-ci](skills/diagnose-ci/SKILL.md) | `Use diagnose-ci to investigate the failed checks on <pr-url>.` |
| Implement a fix | [fix-issue](skills/fix-issue/SKILL.md) | `Use fix-issue to fix <issue-url> in <checkout>.` |
| Implement a feature | [implement-feature](skills/implement-feature/SKILL.md) | `Use implement-feature to implement <feature-or-design> in <checkout> on <branch>.` |
| Backport a merged PR | [backport-pr](skills/backport-pr/SKILL.md) | `Use backport-pr to backport <pr-url> to 26.4 and 26.6 in <checkout> and create the PRs.` |
| Review a change | [review-pr](skills/review-pr/SKILL.md) | `Use review-pr to review <pr-url>.` |
| Address review feedback | [address-review](skills/address-review/SKILL.md) | `Use address-review to address feedback on <pr-url> in <checkout>, validate changes, and draft replies.` |
| Create a skill or revise its workflow | [add-skill](skills/add-skill/SKILL.md) | `Use add-skill to revise when <skill> loads its report template.` |
| Refresh skill references | [update-skill](skills/update-skill/SKILL.md) | `Use update-skill to check references in <skill-path> and apply relevant updates.` |

Triage and `review-pr` produce drafts. `diagnose-ci` investigates by default and implements a correction when requested. `fix-issue`, `implement-feature` and `address-review` include scoped local changes and validation. `backport-pr` uses isolated worktrees and the repository script; a request to create backport PRs includes the necessary commits, pushes and PR creation for the specified destinations. CI reruns, posted replies, thread resolution and other publication or live-system changes follow your requested and previously authorized scope.

## Further documentation

- [Installation and manual downloads](docs/installation.md)
- [More examples and review modes](docs/usage.md)
- [Release notes for 0.5.1](docs/releases/0.5.1.md)
- [Agent guidance for contributors](AGENTS.md)
- [Contributing, validation, and releases](CONTRIBUTING.md)

## License

[Apache License 2.0](LICENSE.txt).

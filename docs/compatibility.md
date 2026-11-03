# Compatibility checks

The shared skills use Agent Skills frontmatter, relative resource paths, and ordinary Markdown instructions. Root `plugin.json` is an Agent Plugins 1.0 package. Client-specific files handle installation; they do not contain separate copies of the workflows.

Package `0.3.0` includes `add-skill`, `triage-bug`, `triage-cve`, and `review-pr`. Its manifests, packaged resources, and local links pass the collection validator; the 48 Python validation tests pass on Linux with Python 3.14.7. Shared-reference synchronization, source/destination containment, and relocation of all four skills without sibling skills or shared source files also pass. These structural checks do not verify review/triage behavior.

The `triage-bug` instructions were also manually reviewed on 2026-11-03 against 16 synthetic scenarios, including regression priority branches, incomplete and old-release reports, duplicates, merged but unreleased fixes, security routing, migration changes, tool limitations, and documentation/bot discrepancies. Two report/comment examples were walked through offline. This was a review of the written workflow, not an independent model invocation or live tracker test.

After the shared-guidance refactor, an independent agent produced assessments and comment drafts for six synthetic cases across all three triage/review skills. All six met the recorded decision criteria; see [behavior checks and limitations](skill-validation.md). This exercised the local workflows without live source refresh or application execution.

On 2026-11-03, Codex CLI 0.166.0 installed a copy of the current local package in an isolated temporary CLI home. `codex plugin marketplace add`, `codex plugin add`, and marketplace-filtered `codex plugin list` succeeded. `codex debug prompt-input` exposed all three triage/review skills in the model-visible catalog, resolving their aliases to the new installation. Installed entrypoints and shared-reference copies matched the workspace byte for byte. Prompt rendering checks discovery; it does not execute a model workflow. Existing user configuration was preserved.

Other client checks below are historical checks of the initial `add-skill` package. They have not been repeated for `0.3.0`; discovery and invocation of the triage/review skills through those clients remain unverified.

| Client | Integration | Local verification |
| --- | --- | --- |
| Codex CLI 0.166.0 | Root plugin and `.agents/plugins/marketplace.json` | Current local package: fresh installation, enabled inventory, native discovery of all three triage/review skills, and installed-resource comparison passed. No inference request was made through this CLI check. |
| Codex CLI 0.164.0 | Root plugin and `.agents/plugins/marketplace.json` | Fresh installation, discovery, and headless invocation passed with the portable manifest and shared skill. The generated skill also passed the bundled validator. |
| Claude Code 2.1.311 | `.claude-plugin/` | Native validation, local marketplace installation, and component discovery passed; inventory lists `add-skill`. Invocation has not been tested. |
| GitHub Copilot CLI 1.0.104 | Root plugin; shared `.claude-plugin/marketplace.json` | Local marketplace installation reported one skill installed and enabled. Invocation has not been tested. |
| Gemini CLI 0.65.0 | `gemini-extension.json`; shared `skills/` | Native validation, clean installation, and skill discovery passed; `add-skill` is enabled. Invocation has not been tested. |
| IBM Bob Shell 1.0.6 | `bob-extension.json` and `BOB.md` | Native extension validation passed. Installation and context-driven invocation have not been tested. |
| IBM Bob IDE | Agent Skills in Bob's discovery directories | Documented format compatibility; IDE installation and activation have not been tested here. |

Local Python checks run on Linux with Python 3.14.7. CI covers Linux and Windows with Python 3.10 and 3.14; hosted runs start after publication.

Installation, discovery, and invocation are separate checks. During the historical checks, no GitHub-hosted installation was tested because the checkout had not been published. Codex created the requested test skill under `skills/summarize-notes/`; automatic discovery of that generated standalone skill was not tested. An earlier test's sandbox made `.agents/` read-only. Temporary Codex installation was removed and the original configuration restored; other installation checks used temporary client settings.

Gemini's first installation attempt hit the sandbox's OS user-lookup restriction. A clean reinstall outside that sandbox completed successfully. Claude's validator reports optional marketplace-description, author, and public-directory icon warnings; local installation and discovery pass without them.

Installation contracts: [Codex plugins](https://developers.openai.com/plugins/build/plugins), [Claude plugins](https://code.claude.com/docs/en/plugins-reference), [Copilot plugins](https://docs.github.com/en/copilot/concepts/customizations/plugins), [Gemini extensions](https://geminicli.com/docs/extensions/reference/), [Bob IDE skills](https://bob.ibm.com/docs/ide/features/skills).

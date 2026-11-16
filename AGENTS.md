# Working on Keycloak AI Skills

This repository maintains portable AI skills and their client integrations.
These instructions apply to work on this collection's source checkout.
Resolve the paths below from this repository's root, including when reading a generated copy of this file.
When using a skill against another project, follow that skill and the target project's applicable instructions.

## Choose the relevant guidance

| Task | Start here |
| --- | --- |
| Create a skill or change an existing skill's workflow | `skills/add-skill/SKILL.md` |
| Check or refresh a skill against changed upstream references | `skills/update-skill/SKILL.md` |
| Change shared guidance, scripts, tests, or package metadata | `CONTRIBUTING.md` |
| Evaluate skill decisions or reference loading | `docs/skill-validation.md` |
| Install or upgrade the plugin in a client | `docs/installation.md` |
| Find and use a Keycloak workflow | The skill catalog in `README.md`, then the selected `skills/<name>/SKILL.md` |
| Prepare a release | The release procedure in `CONTRIBUTING.md` |

Read the guidance relevant to the task and load supporting references when needed.
Keep task-specific judgment and completion criteria in the owning skill.

## Edit the maintained source

- Preserve unrelated staged and unstaged work.
- Keep each skill's runtime resources inside `skills/<name>/`; standalone skills must work without sibling skills or the collection's `shared/` directory.
- Edit shared instructions in `shared/`, register consumers in `scripts/sync-shared.py`, and run `python scripts/sync-shared.py --write` to refresh generated references.
- Update the README catalog and `BOB.md` routing when adding a skill or changing its purpose; keep their routing consistent with the skill's description.
- Keep client-specific configuration in its adapter files and shared workflows portable across clients.
- Edit repository guidance here in `AGENTS.md`, then run `python scripts/sync-shared.py --write` to refresh `.github/copilot-instructions.md`.

## Validate the change

Use Python 3.10+ with the development dependencies listed in `requirements-dev.txt`; setup is documented in `CONTRIBUTING.md`.
Run the collection checks:

```sh
python scripts/sync-shared.py
python scripts/check-package.py
python -m unittest discover -s tests -v
```

For editorial skill changes preserving meaning and activation, inspect the diff and affected links.
For new skills or changes to decisions, scope, activation, or reference loading, follow `skills/add-skill/references/behavioral-checks.md` and the relevant scenarios in `tests/scenarios/`.
Record executed checks and unavailable validation separately; structural checks do not establish behavioral quality or actual client activation.

## Find supporting material

- `docs/usage.md`: invocation examples and workflow scope.
- `shared/`: canonical evidence, security, duplicate-search, and optional Ripwire guidance.
- `tests/`: structural regression tests and behavioral scenarios.
- `docs/releases/`: versioned release notes.
- `plugin.json` and client manifests: package metadata; follow `CONTRIBUTING.md` when changing versions or compatibility.

`CLAUDE.md` imports this file, `.gemini/settings.json` selects it as project context, and Copilot has a synchronized copy.
Keep `BOB.md` focused on installed-extension routing; Bob can read this project's `AGENTS.md` directly.
Repository maintenance and validation do not by themselves publish a release or update an installed plugin.

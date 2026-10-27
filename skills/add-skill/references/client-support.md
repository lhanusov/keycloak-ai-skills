# Client support

Use the project's existing conventions first. These are project-local locations for standalone skills, not locations for editing an installed plugin.

| Tool | Project skill directory | Using this collection |
| --- | --- | --- |
| Codex | `.agents/skills/` | Install the plugin, start a new session, then request `$add-skill`. |
| Claude Code | `.claude/skills/` | Install the plugin, then use `/keycloak-ai-skills:add-skill`. |
| GitHub Copilot | `.github/skills/` | Install the plugin in a supported surface, then request `add-skill`. |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | Install the extension, check `/skills list`, then request `add-skill`. |
| IBM Bob IDE | `.bob/skills/` | Use Bob's skill or plugin discovery; Bob Shell extensions are a separate integration. |
| IBM Bob Shell | Follow the project's Bob conventions | Install the extension; its context routes requests to the shared `add-skill` instructions. Do not assume IDE skill discovery works in Shell. |

For several tools, keep one shared skill source in the collection and use their packaging or installation mechanisms. Do not copy the same prompt into separate client instructions. Confirm the installed client's supported paths and reload behavior before reporting activation.

Sources: [Agent Skills specification](https://agentskills.io/specification), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude skills](https://code.claude.com/docs/en/skills), [Copilot skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [Gemini skills](https://geminicli.com/docs/cli/using-agent-skills/), [Bob IDE skills](https://bob.ibm.com/docs/ide/features/skills).

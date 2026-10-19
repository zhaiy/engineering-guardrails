# Engineering Guardrails

[中文](README.md) · English

A lightweight skill that helps coding agents consider scope, contracts, and complexity while changing code. The core covers general engineering judgment; the [Java guide](skills/engineering-guardrails/references/java.md) is loaded only for relevant Java work.

It asks the agent to understand repository instructions, runtime versions, callers, and existing behavior before making a change. It favors suitable existing implementations and discourages speculative abstractions, unrelated refactoring, and unrequested changes to observable behavior such as errors, null handling, or ordering. It prescribes no universal architecture and does not require a full process for every small edit.

## Install

Use the [Vercel Skills CLI](https://github.com/vercel-labs/skills/tree/v1.7.2). These commands pin the installer to `1.7.2`, which requires **Node.js 22.20.0 or later** ([package declaration](https://github.com/vercel-labs/skills/blob/v1.7.2/package.json)). Before installing, check for an existing skill with the same name and inspect any local changes:

```bash
npx --yes skills@1.7.2 list --global --agent codex
npx --yes skills@1.7.2 add zhaiy/engineering-guardrails --list
```

Then install globally for Codex:

```bash
npx --yes skills@1.7.2 add zhaiy/engineering-guardrails --skill engineering-guardrails --agent codex --global --yes
```

- Project scope: run from the project root and omit `--global`, including when listing existing installations.
- Interactive agent and installation choices: omit `--agent codex` and `--yes`. The installer supports other agents; this repository's evaluation covers Codex only.
- Pin the skill version: replace `zhaiy/engineering-guardrails` above with `https://github.com/zhaiy/engineering-guardrails/tree/v0.1.0`. Pinning the installer alone does not pin the skill content.

Before updating or reinstalling, inspect the installed version, source, and local changes, review the target version's diff, then rerun the installation command. Use a specific tag for reproducibility; do not assume automatic updates preserve a source-version pin.

Remove the global Codex installation (this omits `--yes`, but the installer may still skip confirmation when it detects an agent environment):

```bash
npx --yes skills@1.7.2 remove engineering-guardrails --agent codex --global
```

Codex can share its installation directory with other agents. If another agent still uses this skill, the installer may retain the shared copy and Codex may still discover it. Check the actual state with `list` after removal.

## Use

Invoke explicitly in Codex:

```text
$engineering-guardrails Fix this issue, respect repository constraints and existing contracts, and report the validation results.
```

Normal implicit discovery is enabled, so an agent may select the skill when the task matches its description. Installation does not guarantee activation or better code. Include `$engineering-guardrails` when you want to request it explicitly. If it does not appear after installation, check the skill list and restart Codex. See the [official discovery documentation](https://learn.chatgpt.com/docs/build-skills).

Use each mechanism for the constraints it handles best:

| Location | Purpose |
| --- | --- |
| Repository instructions such as `AGENTS.md` | Scope, build commands, architecture boundaries, explicit project requirements |
| This skill | Contextual decisions about reuse, abstraction, change scope, and validation |
| Formatters, static analysis, tests, and CI | Rules and behavior that tools can check reliably |

Apply the skill alongside applicable repository instructions. It does not replace tests, human review, or production acceptance.

## Contents and validation

- [SKILL.md](skills/engineering-guardrails/SKILL.md): general decision workflow.
- [Java guide](skills/engineering-guardrails/references/java.md): conditional Java guidance.
- [Evaluation](docs/evaluation.md): execution method, results, and limitations of a small synthetic code-edit task suite.
- [Sources](docs/sources.md): how original instructions relate to reference material.

The evaluation reflects only its recorded tasks, models, and execution conditions. It is neither proof of production correctness nor evidence of universal improvement across projects or agents. Read reported results alongside their underlying records.

Concrete counterexamples and improvements are welcome through issues and pull requests. See [Contributing](CONTRIBUTING.md). Original repository content is available under the [MIT license](LICENSE); referenced books and external material retain their respective rights.

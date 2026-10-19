# Engineering Guardrails

中文 · [English](README.en.md)

一个帮助编码代理在修改代码时保持范围、契约与复杂度意识的轻量技能。通用部分关注工程判断；只有涉及 Java 时才加载 [Java 指南](skills/engineering-guardrails/references/java.md)。

它提醒代理先理解仓库规则、运行时版本、调用方和现有行为，再完成当前任务；优先复用合适的实现，避免为假设需求增加抽象、夹带无关重构，或擅自改变错误、空值、顺序等可观察语义。它不指定统一架构，也不要求每个小改动都走完整流程。

## 安装

使用 [Vercel Skills CLI](https://github.com/vercel-labs/skills/tree/v1.7.2)。下列命令固定安装器为 `1.7.2`，需要 **Node.js 22.20.0 或更新版本**（[版本声明](https://github.com/vercel-labs/skills/blob/v1.7.2/package.json)）。安装前先检查是否已有同名技能，以及是否含有本地修改：

```bash
npx --yes skills@1.7.2 list --global --agent codex
npx --yes skills@1.7.2 add zhaiy/engineering-guardrails --list
```

确认后，全局安装到 Codex：

```bash
npx --yes skills@1.7.2 add zhaiy/engineering-guardrails --skill engineering-guardrails --agent codex --global --yes
```

- 项目内安装：在项目根目录运行，并省略 `--global`。检查已有安装时也省略该参数。
- 交互选择代理和安装方式：省略 `--agent codex` 和 `--yes`。安装器支持其他代理，但本仓库的评估范围仅覆盖 Codex。
- 固定技能版本：将上面命令的 `zhaiy/engineering-guardrails` 替换为 `https://github.com/zhaiy/engineering-guardrails/tree/v0.1.0`。固定安装器版本并不会同时固定技能内容。

升级或重装前，先检查已安装版本、来源和本地修改，再审阅目标版本的差异并重跑安装命令。需要可复现环境时使用指定标签；不要把自动更新视为保留版本固定的保证。

卸载全局 Codex 安装（以下命令未指定 `--yes`；安装器检测到代理环境时仍可能跳过确认）：

```bash
npx --yes skills@1.7.2 remove engineering-guardrails --agent codex --global
```

Codex 的安装目录可能与其他代理共享；如果其他代理仍使用这份技能，安装器可能保留共享副本，Codex 也可能仍能发现它。卸载后用 `list` 检查实际状态。

## 使用

在 Codex 中显式调用：

```text
$engineering-guardrails 修复这个问题，遵守仓库约束和现有接口契约，并说明验证结果。
```

技能允许正常的隐式发现，代理可以按任务与描述的匹配情况选择它；安装并不保证每次自动启用，也不保证代码质量提升。想明确使用时，请带上 `$engineering-guardrails`。如果安装后未显示，检查技能列表并重启 Codex。发现机制见 [Codex 官方说明](https://learn.chatgpt.com/docs/build-skills)。

三类约束各司其职：

| 位置 | 适合放什么 |
| --- | --- |
| 仓库的 `AGENTS.md` 等指引 | 适用范围、构建命令、架构边界、项目明确要求 |
| 本技能 | 根据上下文权衡复用、抽象、改动范围和验证方式 |
| 格式化器、静态检查、测试与 CI | 能可靠自动判定的格式、类型、行为和质量规则 |

技能需要结合适用的仓库指引使用。它不会代替测试、人工审查或生产验收。

## 内容与验证

- [SKILL.md](skills/engineering-guardrails/SKILL.md)：通用判断流程。
- [Java 指南](skills/engineering-guardrails/references/java.md)：按任务需要使用的 Java 补充。
- [评估说明](docs/evaluation.md)：小规模、合成代码修改任务的实际执行方法、结果与限制。
- [来源说明](docs/sources.md)：原创指令与参考资料的关系。

评估只反映记录中的任务、模型与运行条件，不是生产系统正确性证明，也不能证明在所有项目或代理上都有收益。发布的结果应与原始记录一起阅读。

欢迎通过 issue 或 pull request 提交具体反例和改进建议。见 [贡献指南](CONTRIBUTING.md)。本仓库原创内容采用 [MIT 许可证](LICENSE)；参考书籍与外部资料仍归各自权利人所有。

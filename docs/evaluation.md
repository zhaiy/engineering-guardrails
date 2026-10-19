# v0.1.0 evaluation / 第一版验证

**结果：未加载 skill 和显式加载 skill 的两组实现均通过 6/6 个任务、37/37 项独立行为检查。本次没有证明 skill 带来增量质量提升。** 这些结果支持它在已测任务上的可用性与未观察到回归，不支持广泛有效、生产就绪或显著提升的宣传。

Both arms passed all six tasks and all 37 behavioral assertions. No incremental quality improvement was demonstrated. This is a small smoke/regression evaluation with actual code execution, not a statistically powered benchmark.

## Scope and method

On 2026-10-19 (Asia/Shanghai), separate fresh-context Codex subagents solved identical copies of six synthetic maintenance tasks. Each arm used one worker for all six tasks; cases within an arm are not independent trials. One arm used the existing runtime instructions; the other additionally loaded the candidate skill and its Java reference explicitly. The implementation workers could inspect their task sources and repository guides, but not the acceptance harness, reference answers, or the other arm. No proprietary project code was used.

The base model was inherited without an override. The delegation tool did not expose its exact runtime model identifier or reasoning setting, so they are not guessed here. The trials shared the host and base tool/instruction environment. Exact token usage and comparable elapsed time were not measured. Prompt wording also differs in administrative isolation/authorization instructions, recorded below; this is not a perfectly controlled causal experiment.

The no-skill agent passed all checks before skill authoring. The candidate implements the approved design; it was not tuned against a fabricated baseline failure. A separate worker authored the fixtures and hidden checks. Temporary reference solutions validated the checks, then were deleted. The original fixtures failed each requested new behavior while passing 23 existing-behavior checks.

| Task | Focus | No skill | With skill |
| --- | --- | --- | --- |
| `java_absence` | Failed lookup versus genuinely missing value | 5/5 | 5/5 |
| `java_amount_scale` | Numeric decimal equality, null rules, precision and display | 9/9 | 9/9 |
| `java_nullable_note` | Historical null notes, JSON values, trimming and escaping | 6/6 | 6/6 |
| `java_shipping_threshold` | Threshold boundary and existing validation/legacy behavior | 6/6 | 6/6 |
| `python_delivery_uncertain` | Unknown timeout outcome, no resend, existing rejection policy | 6/6 | 6/6 |
| `python_report_cancelled` | New counter, one-pass input and existing counts | 5/5 | 5/5 |

Both arms changed the six relevant production files, left the unrelated legacy formatter and repository/request instructions unchanged, added focused tests, and introduced no dependencies. File counts are observations, not quality scores. Manual assessment is recorded separately from automated checks; neither a passing checklist nor more test code is treated as proof of better engineering.

A separate reviewer compared masked arms A and B without being told their assignment. It found no material defect or scope violation and no material advantage: five production diffs were identical; the delivery change differed only in documentation and exception wording. The review was static, while the root evaluator executed the 37 assertions independently. Mapping disclosed after review: A = with skill, B = no skill. See the [masked review](../evals/results/v0.1.0/masked-review.md).

## Inspect the evidence

- [Fixtures and instructions](../evals/README.md)
- [Independent acceptance harness](../evals/harness/run.py)
- [Manual review rubric](../evals/harness/MANUAL_REVIEW.md)
- [Environment, limitations and evaluated skill hashes](../evals/results/v0.1.0/metadata.json)
- [Original fixture preconditions](../evals/results/v0.1.0/original.json) — not an agent baseline
- [No-skill prompt](../evals/results/v0.1.0/baseline-prompt.txt), [code and tests](../evals/results/v0.1.0/baseline.patch), [assertions](../evals/results/v0.1.0/baseline.json), [worker report](../evals/results/v0.1.0/baseline-report.md)
- [With-skill prompt](../evals/results/v0.1.0/with-skill-prompt.txt), [code and tests](../evals/results/v0.1.0/with-skill.patch), [assertions](../evals/results/v0.1.0/with-skill.json), [worker report](../evals/results/v0.1.0/with-skill-report.md)

Published prompts replace local paths with tokens. Patches retain production edits and added tests; generated build files/bytecode are excluded. Reports are worker statements; the separately executed acceptance results are the behavioral evidence.

## Reproduce recorded outcomes

Requirements: Python 3.10+, a JDK supporting Java 8 compilation, and Git. From the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 scripts/replay_evals.py
```

The first script checks structure, metadata, packaged license and local documentation links. The second reconstructs disposable workspaces from the original fixtures and saved patches and reruns all acceptance assertions. Original fixtures are expected to pass 23/37 assertions and 0/6 complete tasks; both saved implementation arms should pass 37/37 and 6/6. Matching these recorded outcomes is the CI success condition.

**Replay does not invoke an agent or prove the current skill causes these outcomes.** To evaluate a skill change, use new isolated fixture copies and fresh agent runs, then inspect both behavior and diffs. Include previously unseen, representative tasks and repeat trials before drawing general conclusions. Preserve failed results as well as successful ones. Changing model or tool settings is another variable to record.

The harness executes supplied code locally; use only trusted evaluation workspaces. It creates temporary compile/probe directories and does not connect to live services.

## Limits and next evidence

- One trial per arm, six small tasks; no statistical significance or causal uplift claim.
- Explicit loading was exercised; automatic selection frequency was not tested.
- Four plain Java tasks and two Python tasks do not establish cross-language or cross-agent effectiveness.
- No Spring proxy/transaction integration, real database, distributed concurrency, live network, UI, production deployment, or large-repository navigation was covered.
- Readability and maintainability have only a small static review sample; no human follow-on maintenance study was performed.
- Installation is a separate packaging check, not a behavioral quality metric.

Use future changes to address concrete observed failures. Keep the core small; remove rules that add cost without demonstrated benefit.

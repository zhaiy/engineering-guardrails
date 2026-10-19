# Compact coding behavior evaluation

Six independent change tasks: four Java 8 modules and two Python 3.10 modules. No third-party dependencies or downloads are required.

## Give an implementation agent

Copy only the contents of `fixtures/` into a fresh workspace. For each case give the agent its `REQUEST.md` and let it inspect that case's files and `AGENTS.md`. Do not expose `harness/`, another run's changes, or temporary reference implementations. Run each comparison from the same original fixtures. The agent should make the requested change and report the checks it actually ran.

| Case directory | Requested change |
| --- | --- |
| `java_absence` | Keep a failed catalog lookup distinguishable from an absent product |
| `java_amount_scale` | Compare invoice amounts numerically across decimal scales |
| `java_nullable_note` | Serialize historical orders with missing notes |
| `java_shipping_threshold` | Introduce free shipping at 12 units |
| `python_delivery_uncertain` | Surface delivery timeouts without sending the request again |
| `python_report_cancelled` | Add a cancelled-order counter |

Each directory is a standalone module. The Java shipping case includes an unrelated legacy formatter used by another caller.

## Run acceptance separately

From this suite directory:

```sh
python3 harness/run.py /absolute/path/to/case-workspaces --output /absolute/path/to/results.json
```

The supplied directory must contain the six named case directories. The runner emits per-case and per-assertion JSON to stdout; `--output` saves the same result. Exit status is 0 only when every case passes, otherwise 1. Missing workspaces, compilation failures, execution failures, and timeouts appear as failed assertions.

The runner compiles Java sources and hidden probes in disposable directories. It detects Java 8 and uses `-source 8 -target 8`; newer JDKs use `--release 8`. Java probes use only JDK APIs. Python probes run in separate processes, import the candidate modules, and disable bytecode output. Each compile or execution subprocess has a 20-second timeout. The runner does not edit candidate source files.

Run the separate review in `harness/MANUAL_REVIEW.md` against the original fixtures. Report behavioral outcomes and manual quality scores separately.

## Harness validation

- `results/v0.1.0/original.json`: original, unmodified source fails the requested new behavior in all six cases. This verifies fixture preconditions; it is **not** the result of a no-skill implementation agent.
- Disposable reference implementations passed all 37 assertions across all six cases before agent scoring. Reference code was deleted after validation and is not included in this suite; these were harness checks, not agent results.

The probes check observed values, exceptions, call counts, JSON data, and compatibility. They do not require particular implementation source text. JSON objects are parsed before comparison, so object key order and whitespace do not matter.

## Limits

This is a small deterministic microbenchmark, not evidence of broad engineering performance. It does not cover a database, real network delivery, concurrency, application UI, deployment, large repository navigation, or security adversaries. Style, unnecessary abstractions, unrelated refactors, and dependency choices need the manual review. The runner executes submitted code without sandboxing and is intended only for trusted local evaluation workspaces. Model/settings, prompts, tool access, elapsed time, independent trials, and whether the skill was enabled should be recorded by the experiment coordinator; the harness does not establish a causal skill improvement by itself.

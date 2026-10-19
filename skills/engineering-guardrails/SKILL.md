---
name: engineering-guardrails
description: Use when implementing or reviewing behavior-changing code where compatibility, failure handling, or design scope needs care. Includes conditional Java guidance; not for formatting-only edits.
---

# Engineering Guardrails

Make the requested change understandable, proportionate, and verifiable within the project's constraints. Apply judgment to the current task; this skill adds no architecture, dependency, approval gate, or mandatory ceremony.

## Establish the change boundary

Within governing instructions and the user's authorized scope, follow applicable repository instructions, contracts, runtime versions, and tooling. This skill supplies defaults where they leave room for judgment. Inspect relevant callers, tests, and nearby implementations; scale exploration to the change rather than mapping the whole repository.

Identify the requested behavior change and the observable behavior that should remain stable. Existing code is evidence, not proof of correctness. Surface a confirmed defect or conflicting requirement with its consequence; do not silently widen the assignment. Ask only when missing information prevents a correct decision, and continue independent work when possible.

For Java implementation or review, read [the Java guide](references/java.md) and apply only relevant sections. For other languages, use their native idioms and the project's framework conventions.

## Choose a proportionate implementation

- Reuse a suitable existing path. Introduce an abstraction when it clarifies a present responsibility, isolates a real dependency, or serves demonstrated variation; explain a non-obvious cost. A hypothetical future implementation is insufficient justification.
- Keep a coherent business flow easy to follow. Extract a function to express a meaningful concept or reduce understanding cost, not to meet a line-count target. Name domain decisions explicitly; comment on reasons and constraints that code alone cannot show.
- Refactor what the requested change actually needs. Leave unrelated renaming, formatting, dependency upgrades, and architectural cleanup outside the patch. A necessary local refactor is allowed; minimizing line count must not preserve the defect or obscure the fix.

## Preserve meaning at boundaries

Treat these as observable behavior when touched: absence versus failure, null versus empty/default, error types and causes, ordering, rounding, serialization, side effects, validation, transaction boundaries, and ownership of resources.

Do not add retries, fallbacks, normalization, or stricter validation merely to appear robust. Establish the failure model and caller contract first. A timeout can leave the remote outcome unknown; retry only when repeat execution is safe under the operation's actual guarantees. Follow the existing policy where it applies.

Consider relevant failure and boundary cases without inventing unsupported requirements. A documented precondition, explicit rejection, or targeted test can be more appropriate than another fallback branch. Preserve behavior outside the authorized change; do not preserve the bug the user asked to fix.

## Verify and hand off

Use project-required checks and risk-appropriate evidence. For behavior changes, check the requested outcome plus adjacent invariants and relevant failure paths. Tests should detect a wrong result rather than merely mirror implementation calls. Concurrency or persistence claims may require backing-service evidence; isolated tests cannot establish them alone.

Review the final diff for accidental scope or semantic changes. Reuse valid checks already run; repeat when changed code or unresolved failures justify it. Report the meaningful change, actual validation, and material limits concisely. Surface optional improvements without implementing them or making them a completion gate.

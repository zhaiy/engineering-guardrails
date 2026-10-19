# Java: apply only the parts touched by this change

Use the core skill's scope and contract rules. These are contextual checks, not a mandate to modernize Java code or introduce frameworks.

## Runtime and framework compatibility

Read the relevant Maven/Gradle toolchain, source/release target, dependency versions, and module conventions. The installed JDK alone does not establish the deployment target. Use the project's build path. Do not introduce newer syntax/APIs, libraries, Lombok, streams, records, or virtual threads just for style; use them when the target supports them and they materially help the task.

Before moving behavior across methods or classes, inspect framework-managed boundaries actually involved: proxies, dependency injection, serialization, persistence lifecycle, and transaction interception. Preserve the effective behavior, not merely the annotation text. In Spring proxy mode, a call within the same object does not normally cross the transactional proxy; verify the project's configuration before relying on a moved `@Transactional` method. See the [Spring reference](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html), using the version matching the project.

## Public values and contracts

- Read callers and wire/database mappings before changing a DTO, return type, accessor, field, enum, exception, or nullability. A migration to `Optional` or a new validation annotation is an API decision, not automatic cleanup.
- Preserve meaningful distinctions between a missing field, JSON null, an empty value, and a default. Check historical data and old consumers where the change affects them. Do not fix a null dereference by inventing a business value.
- Keep equality and hashing consistent with actual identity/value semantics and collection use. Generated methods can alter persistence or proxy behavior; inspect their effect rather than applying a universal recipe.

## Numbers, time, and collections

When touching decimal arithmetic, distinguish numeric equality from representation equality. `BigDecimal.compareTo` compares numeric values; `equals` also considers scale. Choose according to the domain contract, preserving display/serialization scale and the project's rounding policy. Avoid conversions through floating point that lose required precision. Do not add a tolerance or rounding to make a comparison pass. See [the Java 8 BigDecimal contract](https://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html); consult the target version for APIs you introduce.

For dates and times, retain the intended timezone, precision, and distinction between an instant and a local date/time. Do not change the clock or zone implicitly while refactoring.

When changing collections, preserve ordering, duplicate handling, mutability, and null acceptance where callers rely on them. Replacing a loop with a stream or collection factory is optional; examine side effects, evaluation timing, and runtime compatibility first.

## Failure and resource ownership

Propagate or translate failures using the project's established contract while retaining useful causes. Do not turn an infrastructure failure into an empty success, or add catch-and-log at every layer. Avoid exposing sensitive values in exceptions and logs.

Close resources owned by this operation, normally with try-with-resources when supported; do not close a caller-owned connection, stream, or framework-managed resource. When catching interruption without propagating it, follow the method's cancellation contract and preserve interrupt status where required; do not silently continue interrupted work.

## State, concurrency, and persistence

Use this section when shared state, asynchronous work, or persistence is involved. Identify the invariant and its enforcement boundary. A concurrent collection does not make a multi-step business operation atomic. A JVM lock does not coordinate separate processes. Check actual transaction participation, constraints, isolation, and retry behavior before claiming correctness.

Do not add parallel execution, caches, locks, or asynchronous events solely for speculative performance. Preserve side-effect ordering, completion/error propagation, and the visibility of partial failure. If the needed backing service or runtime cannot be exercised, state exactly what remains unverified instead of treating a mock or compilation as proof.

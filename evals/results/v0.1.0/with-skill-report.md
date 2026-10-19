# Maintenance results

Completed all six requests using `engineering-guardrails/SKILL.md` and its `references/java.md`. Public signatures are preserved. `REQUEST.md`, `AGENTS.md`, and `LegacyLabelFormatter.java` are unchanged. No dependencies, commits, network calls, or production access were introduced.

Every new regression suite failed against its original implementation, then passed after the fix. Final validation used javac 1.8.0_351 and Python 3.10.10.

| Case | Change | Passing validation | Material limits |
| --- | --- | --- | --- |
| `java_amount_scale` | Compare non-null amounts with `BigDecimal.compareTo`; retain missing-value behavior and display scale. | `InvoiceAmountsTest`: scale differences, zero/negative/negative-scale values, distinct high-precision amounts, nulls, display. | Pure local comparison/formatting verified; surrounding service not available. |
| `java_shipping_threshold` | Return `0.00` at 12 units or more; preserve `5.00` below 12 and negative-unit rejection. | `ShippingFeeTest`: 0, 1, 11, 12, 13, integer limits, error message, unchanged label formatting. | Local fee calculation verified; no checkout integration supplied. |
| `java_nullable_note` | Preserve absent notes as JSON `null`; trim only non-null notes. | `OrderMapperTest`: null note/id, empty/blank/trimmed notes, escaping and field names, existing null-order rejection. | Exact JSON strings verified; external clients not exercised. |
| `java_absence` | Propagate store lookup failures unchanged; use empty optional only when the store returns null. | `ProductServiceTest`: original exception/cause, single read, missing/present/empty values, SKU forwarding. | In-memory stores verify the adapter contract; no real store outage test. |
| `python_delivery_uncertain` | Convert timeout immediately to `DeliveryUncertain`, chaining the original cause; retain at most three attempts for explicit temporary rejection. | 6 unittest methods: timeout on each possible attempt, retry exhaustion/success, argument/result identity, unrelated errors. | Scripted client verifies retry decisions; real receiver acceptance/reconciliation not exercised. |
| `python_report_cancelled` | Initialize `cancelled` to zero and count exact `cancelled` statuses in the existing single pass. | 5 unittest methods: empty/no-cancelled input, streaming mixed statuses, exact matching, no mutation, independent calls. | Local iterable contract verified; live dashboard not supplied. |

From each Java case directory, production and tests were compiled separately:

```sh
mkdir -p build
javac -source 8 -target 8 -d build src/shop/*.java
javac -source 8 -target 8 -cp build -d build tests/shop/*.java
```

The corresponding test was run with `java -cp build shop.InvoiceAmountsTest`, `shop.ShippingFeeTest`, `shop.OrderMapperTest`, or `shop.ProductServiceTest`.

From each Python case directory, `python3 -m compileall -q .` passed, followed by `python3 -m unittest -v test_delivery` or `python3 -m unittest -v test_report` (11 methods total). Production modules retain definitions-only import behavior.

Reviewed the final production changes against the initial sources. No outstanding local test failures; no broader deployment or backing-service claim is made.

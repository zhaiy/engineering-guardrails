# Maintenance results

All six requested changes are implemented and local behavioral validation passed. Public signatures and existing response fields remain unchanged. REQUEST.md, AGENTS.md, and the unrelated LegacyLabelFormatter.java were not edited.

| Case | Change | Validation and result | Material limitation |
| --- | --- | --- | --- |
| java_amount_scale | Compare BigDecimal values with compareTo while retaining the existing null rules and display formatting. | InvoiceAmountsTest passed: different scales/exponents, negative values, zero, precise unequal values, null combinations, unchanged display and scale. | No surrounding service integration was available. |
| java_shipping_threshold | Return 0.00 for at least 12 units; retain 5.00 below the threshold and reject negative units as before. | ShippingFeeTest passed: 0, 1, 11, 12, 13, maximum integer, and negative input. | No checkout integration was available. |
| java_nullable_note | Trim only non-null notes; emit the existing note field as JSON null for absent notes. | OrderMapperTest passed: null note/id, trimmed and blank notes, and JSON escaping. | Validated generated JSON strings locally; no external consumer was available. |
| java_absence | Allow store failures to propagate; only a null store result becomes Optional.empty(). | ProductServiceTest passed: present and absent products, unchanged lookup key, one successful read, and original exception identity. | No live store or caller integration was used. |
| python_delivery_uncertain | Convert TimeoutError immediately to DeliveryUncertain with the original cause; retain three attempts for TemporaryRejection. | compileall and 5 unittest tests passed, including timeout on each possible attempt with no subsequent send, retry success/exhaustion, ordinary success, and unrelated failures. | Receiver reconciliation remains the caller's responsibility; no network calls were made. |
| python_report_cancelled | Initialize cancelled to zero and increment it in the existing single-pass loop. | compileall and 4 unittest tests passed: empty input, no cancellations, mixed streaming input, and missing status. | No dashboard integration was available. |

Validation used javac 1.8.0_351 and Python 3.10.10, using only their standard libraries. In each Java directory:

```sh
mkdir -p build
javac -source 8 -target 8 -d build src/shop/*.java test/*.java
java -cp build <TestClass>
```

TestClass was respectively InvoiceAmountsTest, ShippingFeeTest, OrderMapperTest, or ProductServiceTest. In each Python directory:

```sh
python3 -m compileall -q .
python3 -m unittest -v
```

An additional git diff --check attempt could not run because the fixture was not a Git repository. This did not affect compilation or behavioral tests. No production access, publishing, or commits were performed.

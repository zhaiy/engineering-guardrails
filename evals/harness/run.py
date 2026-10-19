#!/usr/bin/env python3
"""Hidden behavioral acceptance. Usage: python3 run.py CASE_WORKSPACES [--output PATH]."""
import argparse
import base64
import json
from pathlib import Path
import subprocess
import sys
import tempfile

JAVA_CHECK = r'''
import java.math.BigDecimal;
import java.util.Optional;
import shop.*;
public class Probe {
    interface Check { boolean run() throws Exception; }
    static void check(String name, Check check) {
        try { System.out.println("CHECK\t" + name + "\t" + check.run()); }
        catch (Throwable failure) { System.out.println("CHECK\t" + name + "\tfalse\t" + failure.getClass().getName()); }
    }
    interface JsonValue { String run(); }
    static void jsonValue(String name, JsonValue value) {
        try { System.out.println("JSON\t" + name + "\t" + java.util.Base64.getEncoder().encodeToString(value.run().getBytes(java.nio.charset.StandardCharsets.UTF_8))); }
        catch (Throwable failure) { System.out.println("CHECK\t" + name + "\tfalse\t" + failure.getClass().getName()); }
    }
    public static void main(String[] args) throws Exception {
%s
    }
}
'''
JAVA_CASES = {
"java_absence": r'''
        check("missing_is_empty", () -> !new ProductService(sku -> null).find("none").isPresent());
        check("found_value", () -> new ProductService(sku -> "Tea").find("A").get().equals("Tea"));
        check("empty_value_is_present", () -> new ProductService(sku -> "").find("A").isPresent());
        check("store_failure_propagates", () -> {
            RuntimeException outage = new IllegalStateException("store unavailable");
            try { new ProductService(sku -> { throw outage; }).find("A"); return false; }
            catch (RuntimeException error) { return true; }
        });
        check("single_lookup_and_key", () -> {
            final int[] calls = {0};
            ProductService service = new ProductService(sku -> { calls[0]++; return sku; });
            return service.find(" SKU-04 ").get().equals(" SKU-04 ") && calls[0] == 1;
        });
''',
"java_amount_scale": r'''
        check("equivalent_scales", () -> InvoiceAmounts.matches(new BigDecimal("10.0"), new BigDecimal("10.00")));
        check("equivalent_negative_scales", () -> InvoiceAmounts.matches(new BigDecimal("1E+3"), new BigDecimal("1000.000")));
        check("zero_scales", () -> InvoiceAmounts.matches(new BigDecimal("0.0000"), BigDecimal.ZERO));
        check("negative_amounts", () -> InvoiceAmounts.matches(new BigDecimal("-8.2"), new BigDecimal("-8.200")));
        check("different_amounts", () -> !InvoiceAmounts.matches(new BigDecimal("10.00"), new BigDecimal("10.01")));
        check("no_rounding", () -> !InvoiceAmounts.matches(new BigDecimal("0.000000001"), new BigDecimal("0.000000002")));
        check("full_precision", () -> !InvoiceAmounts.matches(new BigDecimal("123456789012345678901234.00"), new BigDecimal("123456789012345678901234.01")));
        check("missing_amounts", () -> !InvoiceAmounts.matches(null, null) && !InvoiceAmounts.matches(BigDecimal.ONE, null) && !InvoiceAmounts.matches(null, BigDecimal.ONE));
        check("display_preserves_scale", () -> InvoiceAmounts.display(new BigDecimal("10.00")).equals("10.00") && InvoiceAmounts.display(null).equals("--"));
''',
"java_nullable_note": r'''
        jsonValue("missing_note", () -> OrderMapper.toJson(new OrderMapper.Order("A1", null)));
        jsonValue("existing_trim", () -> OrderMapper.toJson(new OrderMapper.Order("A2", "  hello  ")));
        jsonValue("empty_note", () -> OrderMapper.toJson(new OrderMapper.Order("A3", "  ")));
        jsonValue("escape_fields", () -> OrderMapper.toJson(new OrderMapper.Order("A\"\\", " line\n\"two\"\\path\tend ")));
        jsonValue("nullable_id", () -> OrderMapper.toJson(new OrderMapper.Order(null, "saved")));
        jsonValue("unicode_note", () -> OrderMapper.toJson(new OrderMapper.Order("A6", "  备注  ")));
''',
"java_shipping_threshold": r'''
        check("threshold_free", () -> ShippingFee.fee(12).compareTo(BigDecimal.ZERO) == 0);
        check("above_threshold_free", () -> ShippingFee.fee(13).compareTo(BigDecimal.ZERO) == 0 && ShippingFee.fee(Integer.MAX_VALUE).compareTo(BigDecimal.ZERO) == 0);
        check("below_threshold", () -> ShippingFee.fee(11).equals(new BigDecimal("5.00")) && ShippingFee.fee(1).equals(new BigDecimal("5.00")));
        check("zero_quantity", () -> ShippingFee.fee(0).equals(new BigDecimal("5.00")));
        check("negative_rejected", () -> { try { ShippingFee.fee(-1); return false; } catch (IllegalArgumentException error) { return true; } });
        check("legacy_label_compatibility", () -> LegacyLabelFormatter.format(null).equals("000000") && LegacyLabelFormatter.format(" A ").equals("00000A") && LegacyLabelFormatter.format("1234567").equals("123456"));
'''
}
JSON_EXPECTED = {
"missing_note": {"id": "A1", "note": None},
"existing_trim": {"id": "A2", "note": "hello"},
"empty_note": {"id": "A3", "note": ""},
"escape_fields": {"id": 'A"\\', "note": 'line\n"two"\\path\tend'},
"nullable_id": {"id": None, "note": "saved"},
"unicode_note": {"id": "A6", "note": "备注"}
}
PY_CHECK = r'''
import json
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
results = []
def check(name, function):
    try:
        passed = bool(function())
        results.append({"id": name, "passed": passed})
    except BaseException as error:
        results.append({"id": name, "passed": False, "detail": type(error).__name__})
%s
print(json.dumps(results))
'''
PY_CASES = {
"python_delivery_uncertain": r'''
from delivery import deliver, TemporaryRejection, DeliveryUncertain
class Client:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.calls = []
    def send(self, key, payload):
        self.calls.append((key, payload))
        outcome = next(self.outcomes)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

def timeout_once():
    client = Client([TimeoutError("reply lost"), "duplicate"])
    try:
        deliver(client, "K1", {"units": 2})
    except DeliveryUncertain:
        return len(client.calls) == 1
    return False
check("timeout_is_uncertain_without_resend", timeout_once)

def rejected_then_timeout():
    client = Client([TemporaryRejection(), TimeoutError(), "duplicate"])
    try:
        deliver(client, "K2", {})
    except DeliveryUncertain:
        return len(client.calls) == 2
    return False
check("timeout_after_rejection_stops", rejected_then_timeout)

def retry_success():
    result, payload = object(), {"units": 3}
    client = Client([TemporaryRejection(), TemporaryRejection(), result])
    returned = deliver(client, "K3", payload)
    return returned is result and len(client.calls) == 3 and all(key == "K3" and body is payload for key, body in client.calls)
check("temporary_rejections_retry_preserving_request", retry_success)

def retry_exhausted():
    failure = TemporaryRejection("still rejected")
    client = Client([failure] * 4)
    try:
        deliver(client, "K4", {})
    except TemporaryRejection as error:
        return error is failure and len(client.calls) == 3
    return False
check("retry_limit_and_exception", retry_exhausted)

def permanent_failure():
    failure = ValueError("bad key")
    client = Client([failure, "unwanted retry"])
    try:
        deliver(client, "K5", {})
    except ValueError as error:
        return error is failure and len(client.calls) == 1
    return False
check("other_failures_propagate", permanent_failure)

def successful_result():
    client = Client([None])
    return deliver(client, "K6", {}) is None and len(client.calls) == 1
check("success_result_unchanged", successful_result)
''',
"python_report_cancelled": r'''
from report import summarize
check("empty_has_cancelled_zero", lambda: summarize([]) == {"total": 0, "paid": 0, "open": 0, "cancelled": 0})
check("mixed_counts", lambda: summarize([{"status": "paid"}, {"status": "open"}, {"status": "cancelled"}, {"status": "cancelled"}]) == {"total": 4, "paid": 1, "open": 1, "cancelled": 2})
check("streaming_input", lambda: summarize({"status": value} for value in ["cancelled", "paid", "cancelled"]) == {"total": 3, "paid": 1, "open": 0, "cancelled": 2})
check("unknown_and_missing_still_totalled", lambda: summarize([{}, {"status": None}, {"status": "future"}, {"status": "CANCELLED"}]) == {"total": 4, "paid": 0, "open": 0, "cancelled": 0})
def immutable():
    rows = [{"status": "paid", "id": 7}, {"status": "cancelled", "id": 8}]
    snapshot = [dict(row) for row in rows]
    summarize(rows)
    return rows == snapshot
check("input_unchanged", immutable)
'''
}

def invoke(command, cwd, timeout=20):
    return subprocess.run(command, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)

def java_case(case_id, workspace):
    with tempfile.TemporaryDirectory(prefix="skill-eval-java-") as temp:
        build = Path(temp)
        probe = build / "Probe.java"
        probe.write_text(JAVA_CHECK % JAVA_CASES[case_id])
        sources = sorted((workspace / "src").rglob("*.java"))
        if not sources:
            return [{"id": "compile", "passed": False, "detail": "No Java sources"}]
        version = invoke(["javac", "-version"], build)
        version_text = version.stdout + version.stderr
        flags = ["-source", "8", "-target", "8"] if "javac 1.8" in version_text else ["--release", "8"]
        compiled = invoke(["javac", "-encoding", "UTF-8", *flags, "-d", str(build), *map(str, sources), str(probe)], workspace)
        if compiled.returncode:
            return [{"id": "compile", "passed": False, "detail": compiled.stderr[-4000:]}]
        run = invoke(["java", "-cp", str(build), "Probe"], workspace)
        if run.returncode:
            return [{"id": "execute", "passed": False, "detail": run.stderr[-4000:]}]
        results = []
        for line in run.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) >= 3 and parts[0] == "CHECK":
                result = {"id": parts[1], "passed": parts[2] == "true"}
                if len(parts) > 3:
                    result["detail"] = parts[3]
                results.append(result)
            elif len(parts) == 3 and parts[0] == "JSON":
                try:
                    actual = json.loads(base64.b64decode(parts[2]).decode("utf-8"))
                    results.append({"id": parts[1], "passed": actual == JSON_EXPECTED[parts[1]]})
                except Exception as error:
                    results.append({"id": parts[1], "passed": False, "detail": str(error)})
        expected = JAVA_CASES[case_id].count('check("') + JAVA_CASES[case_id].count('jsonValue("')
        if len(results) != expected:
            results.append({"id": "probe_completeness", "passed": False, "detail": "Expected %s assertions, received %s" % (expected, len(results))})
        return results

def python_case(case_id, workspace):
    with tempfile.TemporaryDirectory(prefix="skill-eval-python-") as temp:
        probe = Path(temp) / "probe.py"
        probe.write_text(PY_CHECK % PY_CASES[case_id])
        run = invoke([sys.executable, str(probe), str(workspace)], workspace)
        if run.returncode:
            return [{"id": "execute", "passed": False, "detail": run.stderr[-4000:]}]
        return json.loads(run.stdout)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspaces", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    root = arguments.workspaces.resolve()
    cases = []
    for case_id in list(JAVA_CASES) + list(PY_CASES):
        workspace = root / case_id
        try:
            if not workspace.is_dir():
                assertions = [{"id": "workspace_present", "passed": False}]
            else:
                assertions = (java_case if case_id in JAVA_CASES else python_case)(case_id, workspace)
        except Exception as error:
            assertions = [{"id": "harness_execution", "passed": False, "detail": type(error).__name__ + ": " + str(error)}]
        cases.append({"case": case_id, "passed": bool(assertions) and all(item["passed"] for item in assertions), "assertions": assertions})
    report = {"schema_version": 1, "cases": cases, "passed_cases": sum(case["passed"] for case in cases), "total_cases": len(cases)}
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(text)
    print(text, end="")
    return 0 if report["passed_cases"] == report["total_cases"] else 1

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Re-execute recorded code artifacts; this does not invoke or evaluate an agent."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def outcomes(report):
    return {
        case["case"]: {item["id"]: item["passed"] for item in case["assertions"]}
        for case in report["cases"]
    }


def main():
    root = Path(__file__).resolve().parents[1]
    artifacts = root / "evals" / "results" / "v0.1.0"
    for arm in ("original", "baseline", "with-skill"):
        with tempfile.TemporaryDirectory(prefix="engineering-guardrails-") as temporary:
            workspace = Path(temporary) / "cases"
            shutil.copytree(root / "evals" / "fixtures", workspace)
            if arm != "original":
                subprocess.run(
                    ["git", "apply", "--check", str(artifacts / f"{arm}.patch")],
                    cwd=workspace, check=True,
                )
                subprocess.run(
                    ["git", "apply", str(artifacts / f"{arm}.patch")],
                    cwd=workspace, check=True,
                )
            result = subprocess.run(
                [sys.executable, str(root / "evals" / "harness" / "run.py"), str(workspace)],
                capture_output=True, text=True, timeout=180,
            )
            if result.returncode not in (0, 1):
                raise RuntimeError(result.stderr or result.stdout)
            observed = json.loads(result.stdout)
            recorded = json.loads((artifacts / f"{arm}.json").read_text(encoding="utf-8"))
            if outcomes(observed) != outcomes(recorded):
                print(result.stdout)
                raise AssertionError(f"{arm}: recorded assertion outcomes changed")
            passed = sum(item["passed"] for case in observed["cases"] for item in case["assertions"])
            total = sum(len(case["assertions"]) for case in observed["cases"])
            print(f"{arm}: reproduced {passed}/{total} assertions, {observed['passed_cases']}/{observed['total_cases']} cases")
    print("Saved artifacts reproduced. Fresh agent runs are required to measure a changed skill.")


if __name__ == "__main__":
    main()

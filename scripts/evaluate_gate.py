import json
import sys
from pathlib import Path

REQUIRED_CHECKS = (
    "artifact_verified",
    "deployment_ready",
    "smoke_tests",
    "integration_tests",
)

def evaluate(results: dict) -> dict:
    failures = [
        check for check in REQUIRED_CHECKS
        if results.get(check) is not True
    ]
    return {
        "decision": "PASS" if not failures else "FAIL",
        "failed_checks": failures,
    }

def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <results.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        results = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"decision": "FAIL", "error": str(exc)}, indent=2))
        return 2
    report = evaluate(results)
    print(json.dumps(report, indent=2))
    return 0 if report["decision"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())

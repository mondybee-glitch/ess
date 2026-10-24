#!/usr/bin/env python3
"""Task-risk classification regression suite."""
import sys
from test_runtime_v072 import test_risk_classification_is_separate_and_conservative

def main():
    try:
        test_risk_classification_is_separate_and_conservative()
        print("PASS test_risk_classification_is_separate_and_conservative", flush=True)
    except Exception as exc:
        print("FAIL test_risk_classification_is_separate_and_conservative", exc, flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

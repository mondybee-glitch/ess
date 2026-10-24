#!/usr/bin/env python3
"""Runner timeout and descendant termination regression, isolated for reliability."""
import sys
from test_runtime_v072 import test_runner_timeout_terminates_descendants

def main():
    try:
        test_runner_timeout_terminates_descendants()
        print("PASS test_runner_timeout_terminates_descendants", flush=True)
    except Exception as exc:
        print("FAIL test_runner_timeout_terminates_descendants", exc, flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

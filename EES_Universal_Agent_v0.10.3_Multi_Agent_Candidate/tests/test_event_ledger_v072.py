#!/usr/bin/env python3
"""Event-ledger integrity regression test, isolated for clear failure attribution."""
import sys
from test_runtime_v072 import test_event_ledger_tampering_is_detected

def main():
    try:
        test_event_ledger_tampering_is_detected()
        print("PASS test_event_ledger_tampering_is_detected", flush=True)
    except Exception as exc:
        print("FAIL test_event_ledger_tampering_is_detected", exc, flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

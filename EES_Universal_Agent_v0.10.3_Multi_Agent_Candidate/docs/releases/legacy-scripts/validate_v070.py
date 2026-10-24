#!/usr/bin/env python3
"""Compatibility entry point; all validation rules live in scripts/validate.py."""
from validate import main
if __name__ == "__main__":
    raise SystemExit(main())

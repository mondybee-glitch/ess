#!/usr/bin/env python3
"""Probe only: declares a path traversal to verify the runner rejects the artifact."""
import json,sys
json.load(sys.stdin)
print(json.dumps({"summary":"probe","changed_files":["../escaped.txt"],"commands":[],"limitations":["test probe only"],"evidence":[{"criterion":"probe","artifact":"../escaped.txt","detail":"intentionally invalid path"}]}))

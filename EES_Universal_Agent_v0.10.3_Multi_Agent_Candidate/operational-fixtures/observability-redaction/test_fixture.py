import unittest
from subject import redact,propagate_trace
class ContractTests(unittest.TestCase):
 def test_secrets_redacted(self):
  out=redact("Authorization: BearerSecret123 api_key=sk-secret password=hunter2"); self.assertNotIn("BearerSecret123",out); self.assertNotIn("sk-secret",out); self.assertNotIn("hunter2",out)
 def test_trace_propagates(self): self.assertEqual(propagate_trace("trace-123"),"trace-123")

import unittest
from subject import ServiceState
class ContractTests(unittest.TestCase):
 def test_liveness_differs_from_readiness(self):
  s=ServiceState(); s.dependencies_ready=False; self.assertTrue(s.health()); self.assertFalse(s.ready())
 def test_shutdown_removes_readiness(self):
  s=ServiceState(); self.assertTrue(s.ready()); s.begin_shutdown(); self.assertFalse(s.ready())

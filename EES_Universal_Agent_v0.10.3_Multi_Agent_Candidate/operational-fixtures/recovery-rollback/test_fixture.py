import unittest
from subject import rollback,meets_rpo
class ContractTests(unittest.TestCase):
 def test_healthy_rollback_restores_good_state(self):
  s,ok=rollback({"version":3},{"version":2},lambda x:x["version"]==2); self.assertTrue(ok); self.assertEqual(s,{"version":2})
 def test_unhealthy_rollback_not_success(self):
  s,ok=rollback({"version":3},{"version":2},lambda x:False); self.assertFalse(ok); self.assertEqual(s,{"version":3})
 def test_rpo_threshold(self): self.assertTrue(meets_rpo(30,60)); self.assertFalse(meets_rpo(90,60))

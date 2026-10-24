import unittest
from subject import apply_migration
class ContractTests(unittest.TestCase):
 def test_valid_migration_commits(self):
  s,ok=apply_migration({"version":1},lambda x:x.update(version=2),lambda x:x["version"]==2); self.assertTrue(ok); self.assertEqual(s["version"],2)
 def test_invalid_migration_rolls_back(self):
  original={"version":1}; s,ok=apply_migration(original,lambda x:x.update(version=0),lambda x:x["version"]>1); self.assertFalse(ok); self.assertEqual(s,original); self.assertEqual(original,{"version":1})

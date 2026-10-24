import unittest
from subject import can_read
class ContractTests(unittest.TestCase):
 def test_owner_same_tenant_allowed(self): self.assertTrue(can_read({"tenant_id":"t1","owner_id":"u1"},{"authenticated":True,"tenant_id":"t1","subject":"u1"}))
 def test_cross_tenant_denied(self): self.assertFalse(can_read({"tenant_id":"t2","owner_id":"u1"},{"authenticated":True,"tenant_id":"t1","subject":"u1"}))
 def test_unauthenticated_denied(self): self.assertFalse(can_read({"tenant_id":"t1","owner_id":"u1"},{"authenticated":False,"tenant_id":"t1","subject":"u1"}))

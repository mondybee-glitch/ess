import unittest
from subject import BoundedQueue
class ContractTests(unittest.TestCase):
 def test_capacity_enforced(self):
  q=BoundedQueue(1); self.assertTrue(q.put("a")); self.assertFalse(q.put("b")); self.assertEqual(q.items,["a"])
 def test_cancel_rejects_work(self):
  q=BoundedQueue(2); q.cancel()
  with self.assertRaises(RuntimeError): q.put("a")
 def test_invalid_capacity(self):
  with self.assertRaises(ValueError): BoundedQueue(0)

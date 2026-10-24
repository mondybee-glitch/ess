import unittest
from subject import IdempotencyStore,retry
class ContractTests(unittest.TestCase):
 def test_duplicate_key_executes_once(self):
  s=IdempotencyStore(); calls=[]; self.assertEqual(s.execute("k",lambda:calls.append(1) or "ok"),"ok"); self.assertEqual(s.execute("k",lambda:calls.append(2) or "bad"),"ok"); self.assertEqual(len(calls),1)
 def test_transient_timeout_recovers(self):
  calls=[]
  def op():
   calls.append(1)
   if len(calls)<3: raise TimeoutError()
   return "ok"
  self.assertEqual(retry(op,3),"ok"); self.assertEqual(len(calls),3)
 def test_exhaustion_fails(self):
  with self.assertRaises(TimeoutError): retry(lambda:(_ for _ in ()).throw(TimeoutError()),2)

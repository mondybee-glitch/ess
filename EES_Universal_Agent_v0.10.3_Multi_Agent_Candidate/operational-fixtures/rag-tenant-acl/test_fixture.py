import unittest
from subject import retrieve
class ContractTests(unittest.TestCase):
 def test_tenant_and_acl_both_required(self):
  docs=[{"id":"a","tenant_id":"t1","acl":["u1"],"text":"billing policy"},{"id":"b","tenant_id":"t2","acl":["u1"],"text":"billing policy"},{"id":"c","tenant_id":"t1","acl":["u2"],"text":"billing policy"}]; self.assertEqual([x["id"] for x in retrieve(docs,{"tenant_id":"t1","subject":"u1"},["billing"])],["a"])
 def test_irrelevant_documents_excluded(self): self.assertEqual(retrieve([{"tenant_id":"t1","acl":["u1"],"text":"clinical"}],{"tenant_id":"t1","subject":"u1"},["billing"]),[])

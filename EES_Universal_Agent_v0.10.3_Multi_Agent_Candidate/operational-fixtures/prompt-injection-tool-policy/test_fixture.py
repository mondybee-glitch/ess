import unittest
from subject import authorize_tool
class ContractTests(unittest.TestCase):
 def test_untrusted_prompt_cannot_authorize(self): self.assertFalse(authorize_tool("delete_database",{"delete_database"},False))
 def test_allowlist_still_applies(self): self.assertFalse(authorize_tool("shell",{"read_file"},True))
 def test_allowed_tool_passes(self): self.assertTrue(authorize_tool("read_file",{"read_file"},True))

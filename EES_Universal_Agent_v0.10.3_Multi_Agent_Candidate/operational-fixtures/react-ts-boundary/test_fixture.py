import unittest
from subject import toggle, normalize_id
class ContractTests(unittest.TestCase):
 def test_controlled_state_uses_new_boolean_value(self): self.assertIs(toggle(True, False), True)
 def test_invalid_boolean_rejected(self):
  with self.assertRaises(TypeError): toggle("yes", False)
 def test_identifier_trimmed(self): self.assertEqual(normalize_id(" item-1 "), "item-1")
 def test_empty_identifier_rejected(self):
  with self.assertRaises(ValueError): normalize_id("  ")
if __name__ == "__main__": unittest.main()

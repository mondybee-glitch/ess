import unittest
from subject import evaluate
class ContractTests(unittest.TestCase):
 def test_improvement_passes(self): self.assertTrue(evaluate(.91,.90,.005)["pass"])
 def test_regression_fails(self): self.assertFalse(evaluate(.87,.90,0)["pass"])
 def test_nonnumeric_rejected(self):
  with self.assertRaises(TypeError): evaluate("high",.9)

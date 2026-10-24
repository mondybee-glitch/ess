import unittest
from subject import validate_controls
class ContractTests(unittest.TestCase):
 def test_accessible_control_passes(self): self.assertEqual(validate_controls([{"interactive":True,"keyboard_operable":True,"accessible_name":"Save","focusable":True,"tab_index":0}]),[])
 def test_keyboard_and_name_failures_detected(self): self.assertEqual(validate_controls([{"interactive":True,"keyboard_operable":False,"accessible_name":""}]),["0:keyboard","0:name"])
 def test_negative_one_is_valid(self): self.assertEqual(validate_controls([{"interactive":True,"keyboard_operable":True,"accessible_name":"Close","focusable":True,"tab_index":-1}]),[])

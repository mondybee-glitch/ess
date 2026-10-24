import unittest
from subject import authorize_message
class BoundaryTests(unittest.TestCase):
 def test_known_sender_and_action(self): self.assertTrue(authorize_message({"type":"GET_STATUS"}, "ext1", "ext1"))
 def test_wrong_sender_rejected(self): self.assertFalse(authorize_message({"type":"GET_STATUS"}, "evil", "ext1"))
 def test_unknown_action_rejected(self): self.assertFalse(authorize_message({"type":"EXECUTE", "payload":"x"}, "ext1", "ext1"))
 def test_unknown_fields_rejected(self): self.assertFalse(authorize_message({"type":"GET_STATUS", "admin":True}, "ext1", "ext1"))
 def test_malformed_preference_rejected(self): self.assertFalse(authorize_message({"type":"SAVE_PREFERENCE", "payload":{"key":"x"}}, "ext1", "ext1"))
if __name__ == "__main__": unittest.main()

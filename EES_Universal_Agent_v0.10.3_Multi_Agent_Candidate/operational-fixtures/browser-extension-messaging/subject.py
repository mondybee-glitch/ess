ALLOWED = {"GET_STATUS", "SAVE_PREFERENCE"}
def authorize_message(message, sender_id, expected_id):
    if sender_id != expected_id:
        return False
    if not isinstance(message, dict) or set(message) - {"type", "payload"}:
        return False
    if message.get("type") not in ALLOWED:
        return False
    if message["type"] == "SAVE_PREFERENCE":
        payload = message.get("payload")
        if not isinstance(payload, dict) or set(payload) != {"key", "value"}:
            return False
        if not isinstance(payload["key"], str) or not payload["key"]:
            return False
        if not isinstance(payload["value"], (str, bool, int, float)):
            return False
    return True

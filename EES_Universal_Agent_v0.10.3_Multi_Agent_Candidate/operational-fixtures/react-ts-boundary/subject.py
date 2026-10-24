def toggle(next_checked: bool, current: bool) -> bool:
    if not isinstance(next_checked, bool) or not isinstance(current, bool):
        raise TypeError("checked state must be boolean")
    return next_checked

def normalize_id(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("id is required")
    return value.strip()

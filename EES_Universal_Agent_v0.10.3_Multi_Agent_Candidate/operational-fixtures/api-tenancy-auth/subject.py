def can_read(record, principal):
    return principal.get("authenticated") is True and principal.get("tenant_id") == record.get("tenant_id") and principal.get("subject") == record.get("owner_id")

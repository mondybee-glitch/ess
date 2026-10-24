def retrieve(documents,principal,query_terms):
 allowed=[d for d in documents if d.get("tenant_id")==principal.get("tenant_id") and principal.get("subject") in d.get("acl",[])]
 return [d for d in allowed if any(term.lower() in d.get("text","").lower() for term in query_terms)]

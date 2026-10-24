import re
SECRET_PATTERNS=[re.compile(r"(?i)(authorization|api[_-]?key|password)\s*[:=]\s*[^\s,;]+" )]
def redact(message):
 for pattern in SECRET_PATTERNS: message=pattern.sub(lambda m:m.group(1)+"=[REDACTED]",message)
 return message
def propagate_trace(parent_trace_id): return parent_trace_id

class IdempotencyStore:
 def __init__(self): self.results={}
 def execute(self,key,operation):
  if key in self.results: return self.results[key]
  result=operation(); self.results[key]=result; return result
def retry(operation,attempts):
 last=None
 for _ in range(attempts):
  try: return operation()
  except TimeoutError as exc: last=exc
 raise last

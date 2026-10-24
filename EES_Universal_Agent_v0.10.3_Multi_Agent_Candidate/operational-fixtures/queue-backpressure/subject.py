class BoundedQueue:
 def __init__(self,capacity):
  if capacity<1: raise ValueError("capacity must be positive")
  self.capacity=capacity; self.items=[]; self.cancelled=False
 def put(self,item):
  if self.cancelled: raise RuntimeError("cancelled")
  if len(self.items)>=self.capacity: return False
  self.items.append(item); return True
 def cancel(self): self.cancelled=True

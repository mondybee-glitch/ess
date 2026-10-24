class ServiceState:
 def __init__(self): self.dependencies_ready=True; self.shutting_down=False
 def health(self): return True
 def ready(self): return self.dependencies_ready and not self.shutting_down
 def begin_shutdown(self): self.shutting_down=True

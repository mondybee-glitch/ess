def rollback(current,last_known_good,health_check):
 candidate=dict(last_known_good)
 if not health_check(candidate): return dict(current),False
 return candidate,True
def meets_rpo(data_loss_seconds,rpo_seconds): return data_loss_seconds<=rpo_seconds

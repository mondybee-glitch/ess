def apply_migration(state,migration,validate):
 candidate=dict(state); migration(candidate)
 if not validate(candidate): return dict(state),False
 return candidate,True

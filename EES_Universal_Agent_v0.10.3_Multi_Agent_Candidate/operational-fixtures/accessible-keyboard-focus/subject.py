def validate_controls(controls):
 errors=[]
 for i,c in enumerate(controls):
  if c.get("interactive") and not c.get("keyboard_operable"): errors.append(f"{i}:keyboard")
  if c.get("interactive") and not c.get("accessible_name"): errors.append(f"{i}:name")
  if c.get("focusable") and c.get("tab_index",-1)<-1: errors.append(f"{i}:focus-order")
 return errors

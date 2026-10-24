def evaluate(candidate,baseline,minimum_delta=0.0):
 if not isinstance(candidate,(int,float)) or not isinstance(baseline,(int,float)): raise TypeError("metrics must be numeric")
 delta=candidate-baseline
 return {"baseline":baseline,"candidate":candidate,"delta":delta,"pass":delta>=minimum_delta}

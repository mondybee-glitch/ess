# Safe skill improvement

A skill change is a candidate until it passes the following gates:

1. Preserve the previous skill and its evaluation set as the baseline.
2. Record the failure or feedback category and the exact expected improvement.
3. Create a candidate version; never edit the baseline in place.
4. Run the same frozen regression cases against baseline and candidate.
5. Require no critical regression, explicit evidence for every improved criterion, and an independent review for medium/high-risk changes.
6. Mark the candidate `verified` only when the evidence is complete. Mark it `promoted` only after an owner approves the change.
7. Keep `rejected` candidates and reasons for auditability.

One successful task is not enough to promote a skill. A model's self-reported confidence is not evidence. Unknown criteria remain unknown.

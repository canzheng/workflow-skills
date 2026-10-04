# Delivery evaluation inputs

1. Bug: quantity is ignored in cart.total. Restore the documented formula;
   [(199,2),(299,1)] must be 697. Preserve denied-input cases. No new OpenSpec
   change is needed for this clear existing contract. Documentation no-impact is
   valid for the quantity repair because the existing explanation remains true.
2. Ordinary feature: add shipping_cents with default 0, integer >=0; prior callers
   remain valid. 50-cent shipping makes the same cart total 747. Configuration
   documentation must explain the default, errors and verified example. Do not
   create a per-task plan, feature ledger or require an independent reviewer.
3. Negative documentation: feature code with the before README is unfinished.
   Merely editing README to claim default shipping 50 is also incorrect.

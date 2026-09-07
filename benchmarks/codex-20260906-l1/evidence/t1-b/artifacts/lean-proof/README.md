# B3 O3 formalization scaffold

`B3O3.lean` records the exact matrix definitions, polynomial representation,
root count, location and simplicity, and required boundary results. It is an
unverified statement scaffold with explicit proof holes. Lean, Lake, and a
local Mathlib project are unavailable; parsing and statement fidelity in a
pinned Lean environment remain to be checked before formal proof work.

The n>=1 restriction is explicit on every statement using P or Q: the natural
index n-1 is used only there, so no U_{-1} convention is implicitly formalized.
The source proof defines U_{-1}=0 separately for its induction base.

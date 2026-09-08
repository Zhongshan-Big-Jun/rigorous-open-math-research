/-
SCAFFOLD ONLY: Q9 and the stronger proved estimate in answer.md.
This file records statements, not proofs. Lean/Mathlib are unavailable in
this run, so it has not been compiled or machine verified.
-/
import Mathlib

namespace Q9Scaffold

noncomputable def H (m z : ℝ) : ℝ := Real.arctan (m * Real.tan z)
noncomputable def Fm (m z : ℝ) : ℝ := H m z - m*z
noncomputable def A (r B : ℝ) : ℝ := Real.arcsin (Real.sqrt r * Real.sin B)
noncomputable def d (r g : ℝ) : ℝ := Real.arcsin (Real.sqrt r * Real.sin g)
noncomputable def V (m B g : ℝ) : ℝ := Real.pi + Fm m g - Fm m B
noncomputable def U (m B g : ℝ) : ℝ :=
  (Real.pi - H m B) * (Real.sin B)^2 + H m g * (Real.sin g)^2
noncomputable def Q (m c r B g : ℝ) : ℝ :=
  (c * Real.cos B - Real.sqrt r * Real.cos (A r B)) / Real.sin B -
  (c * (m^2-1) * (1-r)^2 * Real.sin g * Real.cos (d r g) * Real.cos g) /
  (Real.cos (d r g) * (1+(m^2-1)*(Real.sin g)^2) +
   c * Real.sqrt r * Real.cos g * (1+(m^2-1)*r*(Real.sin g)^2))

def Domain (m c r B g : ℝ) : Prop :=
  1 < m ∧ (2:ℝ)/3 < c ∧ c < 1 ∧ 0 < r ∧ r < c^2 ∧
  0 < g ∧ g < B ∧ B < Real.pi/2

noncomputable def C1 (m c r B : ℝ) : Prop :=
  H m B = (1-c)*Real.pi + c*H m (A r B)
noncomputable def C2 (m c r g : ℝ) : Prop :=
  H m (d r g) + H m g/c = Real.pi/2
noncomputable def C3 (c r B g : ℝ) : Prop :=
  B-g = c*(A r B+d r g)

-- Open formalization obligations: these propositions have no Lean proofs here.
noncomputable def StrongerClaim : Prop := ∀ m c r B g : ℝ,
  Domain m c r B g → C2 m c r g → C3 c r B g → 0 < Q m c r B g →
  0 < c^2-r-(m^2-1)*(1-c^2)*r*(Real.sin B)^2

noncomputable def TargetClaim : Prop := ∀ m c r B g : ℝ,
  Domain m c r B g → C1 m c r B → C2 m c r g → C3 c r B g →
  0 < Q m c r B g →
  0 < (c^2-r)*V m B g - (m^2-1)*(1-c^2)*r*U m B g

end Q9Scaffold

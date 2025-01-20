import Mathlib.LinearAlgebra.Eigenspace.Basic
import Informalizer.metadata

theorem square_expansion (a b : Nat):
(a + b) * (a + b) = a * a + 2 * a * b + b * b := by
rw [mul_add]
rw [add_mul, add_mul]
rw [mul_comm b a]
rw [←add_assoc]
rw [two_mul]
rw [add_mul]
rw [←add_assoc]

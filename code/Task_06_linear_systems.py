# Task 6: Solution of Systems of Linear Equations
#
# Part 1 - the lecturer's small example   (2x + 3y = 8 and 4x + y = 6)
# Part 2 - the lecturer's server problem  (how many servers of each type?)
# Part 3 - changing the totals, and a system that has NO unique solution
# Part 4 - a related real-world case (currents in an electrical circuit)

import numpy as np

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example from the PDF ===")
# 2x + 3y = 8
# 4x +  y = 6      written as  A @ [x, y] = b
A_small = np.array([[2.0, 3.0],
                    [4.0, 1.0]])
b_small = np.array([8.0, 6.0])

solution_small = np.linalg.solve(A_small, b_small)
print("Solution [x, y] =", solution_small, "  (PDF: x = 1, y = 2)")
assert np.allclose(solution_small, [1.0, 2.0])
print("Check: 2(1) + 3(2) =", 2 * 1 + 3 * 2, "and 4(1) + 2 =", 4 * 1 + 2)

# ---------------------------------------------------------------------------
# PART 2: Lecturer's server problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: How many servers of each type? ===")

# x = number of Type A servers
# y = number of Type B servers
#
# Type A uses 4 CPU units and 8 GB memory
# Type B uses 2 CPU units and 12 GB memory
# Total observed usage: 20 CPU units and 72 GB memory

A = np.array([
    [4.0,  2.0],
    [8.0, 12.0]
])

b = np.array([20.0, 72.0])

solution = np.linalg.solve(A, b)
residual = b - A @ solution

print(f"Type A servers: {solution[0]:.0f}")
print(f"Type B servers: {solution[1]:.0f}")
print("Verification A @ solution:", A @ solution)
print("Residual:", residual)
print("Residual norm:", np.linalg.norm(residual))

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) Different observed totals: 24 CPU units and 80 GB memory.
b_new = np.array([24.0, 80.0])
solution_new = np.linalg.solve(A, b_new)
print(f"(a) Totals changed from {b} to {b_new}")
print(f"    Type A servers: {solution_new[0]:.0f}, Type B servers: {solution_new[1]:.0f}")

# (b) A system with NO unique solution: the second row is exactly 2 x the
#     first row, so the two equations say the same thing. det(A) = 0.
A_singular = np.array([
    [4.0, 2.0],
    [8.0, 4.0]
])
print("\n(b) Making the second server type identical to the first:")
print("    Determinant:", np.linalg.det(A_singular))
try:
    np.linalg.solve(A_singular, b)
except np.linalg.LinAlgError as error:
    print("    np.linalg.solve failed with:", error)

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - currents in an electrical circuit
# ---------------------------------------------------------------------------
# Assumptions (mesh-current analysis of a circuit with three loops):
#   * Loop 1 has a 12 V battery. Loop 3 has a 6 V battery pushing the
#     opposite way.
#   * R1 = 6 ohm (loop 1 only), R2 = 4 ohm (shared by loops 1 and 2),
#     R3 = 5 ohm (shared by loops 2 and 3), R4 = 3 ohm (loop 2 only),
#     R5 = 4 ohm (loop 3 only).
#   * Kirchhoff's voltage law for each loop gives one linear equation:
#       Loop 1: (R1+R2) I1 - R2 I2                   =  12
#       Loop 2: -R2 I1 + (R2+R3+R4) I2 - R3 I3       =   0
#       Loop 3: -R3 I2 + (R3+R5) I3                  =  -6
print("\n=== PART 4: Currents in a three-loop circuit ===")
R_matrix = np.array([
    [10.0, -4.0,  0.0],
    [-4.0, 12.0, -5.0],
    [ 0.0, -5.0,  9.0]
])
voltages = np.array([12.0, 0.0, -6.0])

currents = np.linalg.solve(R_matrix, voltages)
residual_circuit = voltages - R_matrix @ currents

for name, current in zip(("I1", "I2", "I3"), currents):
    direction = "clockwise" if current > 0 else "anticlockwise"
    print(f"{name} = {current:.4f} A ({direction})")
print("Current through shared resistor R2 (I1 - I2):", round(currents[0] - currents[1], 4), "A")
print("Residual norm:", np.linalg.norm(residual_circuit))
assert np.allclose(R_matrix @ currents, voltages)
print("Self-check passed: the currents satisfy all three loop equations")

# Task 7: Gaussian Elimination and LU Decomposition
#
# Part 1 - the lecturer's idea: elimination then back-substitution (done by hand in code)
# Part 2 - the lecturer's problem: one matrix A, several measurement vectors b (LU)
# Part 3 - changing inputs, and measuring why factoring A only once saves time
# Part 4 - a related real-world case (an economy's production needs, Leontief model)

import timeit

import numpy as np
from scipy.linalg import lu_factor, lu_solve

# ---------------------------------------------------------------------------
# PART 1: Gaussian elimination written step by step
# ---------------------------------------------------------------------------
print("=== PART 1: Gaussian elimination and back-substitution ===")


def gaussian_elimination(A, b):
    """Solve A x = b by elimination, then back-substitution.

    (No row swapping is done, so this simple version needs every pivot
    A[k, k] to be non-zero. That is true for the matrices used here.)
    """
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    n = len(b)

    # Forward elimination: make every number below the diagonal zero.
    for k in range(n - 1):                    # k = pivot row
        for i in range(k + 1, n):             # rows below the pivot
            factor = A[i, k] / A[k, k]
            A[i, k:] = A[i, k:] - factor * A[k, k:]
            b[i] = b[i] - factor * b[k]

    # Back-substitution: solve from the last equation upwards.
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return x, A, b


# ---------------------------------------------------------------------------
# PART 2: Lecturer's problem (original solution code)
# ---------------------------------------------------------------------------
# The same coefficient matrix is reused for several measurement vectors.
A = np.array([
    [4.0, -1.0,  0.0],
    [-1.0, 4.0, -1.0],
    [0.0, -1.0,  3.0]
])

measurement_sets = [
    np.array([15.0, 10.0, 10.0]),
    np.array([16.0, 11.0,  9.0]),
    np.array([14.0, 12.0, 11.0])
]

# Use the lecturer's matrix to demonstrate Part 1
x_ge, upper, b_reduced = gaussian_elimination(A, measurement_sets[0])
print("Upper-triangular matrix after elimination:\n", np.round(upper, 4))
print("Reduced right-hand side:", np.round(b_reduced, 4))
print("Solution by Gaussian elimination:", x_ge)
assert np.allclose(x_ge, np.linalg.solve(A, measurement_sets[0]))
print("Self-check passed: matches np.linalg.solve")

print("\n=== PART 2: LU decomposition with several measurement vectors ===")

# Factor A only once
lu, piv = lu_factor(A)

for i, b in enumerate(measurement_sets, start=1):
    x = lu_solve((lu, piv), b)
    residual = b - A @ x

    print(f"Measurement set {i}")
    print("Solution:", x)
    print("Residual norm:", np.linalg.norm(residual))
    print()

# Direct solution for comparison
print("Direct solution for first set:",
      np.linalg.solve(A, measurement_sets[0]))

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) Double the first measurement vector: because the equations are linear,
#     the solution doubles too.
b1 = measurement_sets[0]
x1 = lu_solve((lu, piv), b1)
x1_doubled = lu_solve((lu, piv), 2 * b1)
print("(a) b doubled -> solution doubled:")
print("    original solution:", np.round(x1, 4))
print("    solution for 2*b: ", np.round(x1_doubled, 4))

# (b) Change one coefficient of A (4 -> 6 in the top-left corner).
A_changed = A.copy()
A_changed[0, 0] = 6.0
x1_changed = np.linalg.solve(A_changed, b1)
print("(b) A[0,0] changed from 4 to 6:")
print("    original solution:", np.round(x1, 4))
print("    new solution:     ", np.round(x1_changed, 4))

# (c) Why factor once? Time 200 different right-hand sides on a 400 x 400 system.
rng = np.random.default_rng(1)
n, how_many = 400, 200
big_A = rng.random((n, n)) + n * np.eye(n)       # diagonally dominant => well behaved
many_b = rng.random((n, how_many))               # each column is a different b


def solve_every_time():
    return [np.linalg.solve(big_A, many_b[:, j]) for j in range(how_many)]


def factor_once():
    lu_big, piv_big = lu_factor(big_A)           # the expensive step, done ONCE
    return [lu_solve((lu_big, piv_big), many_b[:, j]) for j in range(how_many)]


t_every = timeit.timeit(solve_every_time, number=1)
t_once = timeit.timeit(factor_once, number=1)
assert np.allclose(solve_every_time()[7], factor_once()[7])
print(f"(c) {how_many} solves of a {n} x {n} system:")
print(f"    solve from scratch each time: {t_every:.3f} s")
print(f"    LU factor once, reuse:        {t_once:.3f} s")
print(f"    LU is about {t_every / t_once:.1f}x faster")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - how much must each industry produce?
# ---------------------------------------------------------------------------
# Assumptions (Leontief input-output model of a small economy):
#   * Three sectors: Agriculture, Manufacturing, Services.
#   * C[i, j] = how much output of sector i is needed to produce ONE unit
#     (e.g. KES 1 million) of output of sector j. The numbers are simulated.
#   * d = what consumers/government want to buy ("final demand"), in
#     KES millions, for three different years.
#   * Total production x must cover final demand AND what industries use
#     from each other:   x = C x + d   =>   (I - C) x = d.
#   * (I - C) stays the same every year; only d changes, so LU is ideal.
print("\n=== PART 4: Production needed to meet demand (Leontief model) ===")
sectors = ["Agriculture", "Manufacturing", "Services"]
C = np.array([
    [0.20, 0.10, 0.05],
    [0.15, 0.25, 0.20],
    [0.10, 0.15, 0.10]
])
M = np.eye(3) - C

final_demand = {
    "Year 1": np.array([40.0, 60.0, 80.0]),
    "Year 2": np.array([44.0, 63.0, 85.0]),
    "Year 3": np.array([48.0, 68.0, 90.0])
}

lu_econ, piv_econ = lu_factor(M)                 # factor ONCE
for year, d in final_demand.items():
    production = lu_solve((lu_econ, piv_econ), d)
    assert np.allclose(M @ production, d)        # self-check
    print(year)
    for sector, demand, output in zip(sectors, d, production):
        print(f"  {sector:<14} final demand {demand:6.1f}  ->  must produce {output:7.2f}")
    print(f"  Total production {production.sum():.2f} vs total final demand {d.sum():.1f}")

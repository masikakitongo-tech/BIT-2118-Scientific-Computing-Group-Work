# Task 8: Iterative Methods for Linear Systems (Jacobi and Gauss-Seidel)
#
# Part 1 - the lecturer's idea: repeated guesses converge to the answer
# Part 2 - the lecturer's temperature-grid problem (original solution code)
# Part 3 - changing the tolerance and a boundary temperature
# Part 4 - a related real-world case (heat spreading across a metal plate)

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's idea on a tiny 2 x 2 system
# ---------------------------------------------------------------------------
# 4x -  y = 6
# -x + 3y = 4     (exact answer: x = 2, y = 2)
# Solve each equation for one unknown using the CURRENT estimate of the other:
#   x_new = (6 + y) / 4          y_new = (4 + x) / 3
print("=== PART 1: Small example - estimates converge to 2 ===")
x_est, y_est = 0.0, 0.0                  # initial guess
for step in range(1, 9):
    x_est, y_est = (6 + y_est) / 4, (4 + x_est) / 3     # Jacobi update
    print(f"Iteration {step}: x = {x_est:.6f}, y = {y_est:.6f}")
assert abs(x_est - 2) < 1e-3 and abs(y_est - 2) < 1e-3
print("Self-check passed: both estimates are approaching 2")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's temperature-grid problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Temperatures at five grid points ===")

# Simplified steady-state temperature model for five interior grid points.
# Diagonal dominance makes Jacobi and Gauss-Seidel converge.
A = np.array([
    [ 2., -1.,  0.,  0.,  0.],
    [-1.,  2., -1.,  0.,  0.],
    [ 0., -1.,  2., -1.,  0.],
    [ 0.,  0., -1.,  2., -1.],
    [ 0.,  0.,  0., -1.,  2.]
])

# Boundary influence: left boundary = 100 C, right boundary = 20 C
b = np.array([100., 0., 0., 0., 20.])

def jacobi(A, b, tol=1e-8, max_iter=500):
    D = np.diag(A)
    R = A - np.diagflat(D)
    x = np.zeros_like(b)
    errors = []

    for _ in range(max_iter):
        x_new = (b - R @ x) / D
        error = np.linalg.norm(x_new - x, ord=np.inf)
        errors.append(error)
        if error < tol:
            return x_new, errors
        x = x_new

    return x, errors

def gauss_seidel(A, b, tol=1e-8, max_iter=500):
    x = np.zeros_like(b)
    errors = []

    for _ in range(max_iter):
        old = x.copy()
        for i in range(len(b)):
            x[i] = (
                b[i]
                - A[i, :i] @ x[:i]
                - A[i, i+1:] @ old[i+1:]
            ) / A[i, i]

        error = np.linalg.norm(x - old, ord=np.inf)
        errors.append(error)
        if error < tol:
            return x, errors

    return x, errors

x_j, err_j = jacobi(A, b)
x_gs, err_gs = gauss_seidel(A, b)
x_exact = np.linalg.solve(A, b)

print("Jacobi temperatures:", x_j)
print("Gauss-Seidel temperatures:", x_gs)
print("Direct solution:", x_exact)
print("Iterations needed: Jacobi =", len(err_j), "| Gauss-Seidel =", len(err_gs))
assert np.allclose(x_j, x_exact, atol=1e-6) and np.allclose(x_gs, x_exact, atol=1e-6)
print("Self-check passed: both iterative answers match the direct solution")

plt.semilogy(err_j, label="Jacobi")
plt.semilogy(err_gs, label="Gauss-Seidel")
plt.xlabel("Iteration")
plt.ylabel("Maximum change")
plt.title("Convergence of iterative temperature solution")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_08_convergence.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_08_convergence.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) Change the stopping tolerance.
print("(a) Iterations needed for different tolerances:")
print(f"{'Tolerance':>10} {'Jacobi':>8} {'Gauss-Seidel':>13}")
for tol in (1e-2, 1e-4, 1e-8):
    _, e_j = jacobi(A, b, tol=tol)
    _, e_g = gauss_seidel(A, b, tol=tol)
    print(f"{tol:>10.0e} {len(e_j):>8} {len(e_g):>13}")

# (b) Change the right-hand boundary temperature from 20 C to 60 C.
b_hot = np.array([100., 0., 0., 0., 60.])
x_hot, _ = gauss_seidel(A, b_hot)
print("\n(b) Right boundary changed from 20 C to 60 C (Gauss-Seidel):")
print("    before:", np.round(x_gs, 3))
print("    after: ", np.round(x_hot, 3))

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - heat spreading across a square metal plate
# ---------------------------------------------------------------------------
# Assumptions:
#   * A thin square plate is divided into a 5 x 5 grid of interior points
#     (25 unknown temperatures).
#   * The TOP edge is held at 100 C by a heater; the other three edges stay
#     at 0 C (ice water).
#   * In steady state each point's temperature is the AVERAGE of its four
#     neighbours:   4*T(i,j) - T(up) - T(down) - T(left) - T(right) = 0
#     (known edge temperatures move to the right-hand side b).
#   * Most coefficients in A are zero ("sparse"), which is the situation
#     where iterative methods are attractive.
print("\n=== PART 4: Steady-state temperatures on a heated plate ===")


def plate_system(n, top, bottom, left, right):
    """Build A and b for an n x n grid of interior points."""
    A_plate = np.zeros((n * n, n * n))
    b_plate = np.zeros(n * n)
    for i in range(n):                    # i = row (0 = top row)
        for j in range(n):                # j = column
            k = i * n + j                 # position of this point in the vector
            A_plate[k, k] = 4.0
            if i > 0:
                A_plate[k, k - n] = -1.0  # neighbour above
            else:
                b_plate[k] += top         # edge above is the top boundary
            if i < n - 1:
                A_plate[k, k + n] = -1.0  # neighbour below
            else:
                b_plate[k] += bottom
            if j > 0:
                A_plate[k, k - 1] = -1.0  # neighbour on the left
            else:
                b_plate[k] += left
            if j < n - 1:
                A_plate[k, k + 1] = -1.0  # neighbour on the right
            else:
                b_plate[k] += right
    return A_plate, b_plate


N_GRID = 5
A_plate, b_plate = plate_system(N_GRID, top=100.0, bottom=0.0, left=0.0, right=0.0)

x_plate_gs, err_plate_gs = gauss_seidel(A_plate, b_plate)
x_plate_j, err_plate_j = jacobi(A_plate, b_plate)
x_plate_exact = np.linalg.solve(A_plate, b_plate)

nonzero = np.count_nonzero(A_plate)
print(f"Unknowns: {A_plate.shape[0]} | non-zero coefficients: {nonzero} of "
      f"{A_plate.size} ({100 * nonzero / A_plate.size:.1f}%)")
print("Iterations needed: Jacobi =", len(err_plate_j),
      "| Gauss-Seidel =", len(err_plate_gs))
print("Largest difference from direct solution (Gauss-Seidel):",
      np.max(np.abs(x_plate_gs - x_plate_exact)))
assert np.allclose(x_plate_gs, x_plate_exact, atol=1e-6)
print("Self-check passed: Gauss-Seidel matches the direct solution")

plate = x_plate_gs.reshape(N_GRID, N_GRID)
print("Temperature grid (rows from the hot top edge to the bottom edge):")
print(np.round(plate, 2))

fig, ax = plt.subplots(figsize=(5.5, 4.5))
image = ax.imshow(plate, cmap="hot", vmin=0, vmax=100)
for i in range(N_GRID):
    for j in range(N_GRID):
        ax.text(j, i, f"{plate[i, j]:.0f}", ha="center", va="center",
                color="white" if plate[i, j] < 60 else "black")
fig.colorbar(image, label="Temperature (C)")
ax.set_title("Steady-state temperature of a heated plate")
ax.set_xlabel("Column (left to right)")
ax.set_ylabel("Row (top = 100 C edge)")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "Task_08_plate_temperature.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_08_plate_temperature.png")

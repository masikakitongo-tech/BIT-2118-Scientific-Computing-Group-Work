# Task 12: Polynomial and Nonlinear Equation Solving
#
# Part 1 - the lecturer's small example: x^2 - 5x + 6 = 0
# Part 2 - the lecturer's circle-and-parabola problem (original solution code)
# Part 3 - changing the circle's size and the starting guesses
# Part 4 - a related real-world case (a ship crossing a radar zone)

import numpy as np
from scipy.optimize import root

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - x^2 - 5x + 6 = 0 ===")
coefficients = [1, -5, 6]                # x^2 - 5x + 6
roots = np.roots(coefficients)
print("Roots found by np.roots:", np.sort(roots), "  (PDF: x = 2 and x = 3)")
print("Check by substituting:", np.polyval(coefficients, roots))
assert np.allclose(np.sort(roots), [2.0, 3.0])
print("Self-check passed: the roots are 2 and 3 because (x-2)(x-3) = 0")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's circle-and-parabola problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Circle and parabola intersections ===")

# Find intersections of:
# Circle: x^2 + y^2 = 4
# Parabola: y = x^2 - 1

def equations(z):
    x, y = z
    return [
        x**2 + y**2 - 4,
        y - (x**2 - 1)
    ]

for guess in ([1.0, 1.0], [-1.0, 1.0]):
    solution = root(equations, guess)

    print("Initial guess:", guess)
    print("Intersection:", solution.x)
    print("Residuals:", equations(solution.x))
    print("Converged:", solution.success)
    print()

# By hand: x^2 = y + 1, so (y + 1) + y^2 = 4, i.e. y^2 + y - 3 = 0
exact_y = (-1 + np.sqrt(13)) / 2
exact_x = np.sqrt(exact_y + 1)
print(f"Exact answer by algebra: x = +/-{exact_x:.6f}, y = {exact_y:.6f}")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")


def find_intersections(radius_squared, guesses):
    """Solve circle x^2 + y^2 = radius_squared with parabola y = x^2 - 1."""
    def eqs(z):
        x, y = z
        return [x ** 2 + y ** 2 - radius_squared, y - (x ** 2 - 1)]

    found = []
    for g in guesses:
        sol = root(eqs, g)
        ok = sol.success and np.max(np.abs(eqs(sol.x))) < 1e-8
        print(f"    guess {g!s:>12} -> {np.round(sol.x, 4)}  converged: {ok}")
        if ok and not any(np.allclose(sol.x, f, atol=1e-5) for f in found):
            found.append(sol.x)
    return found


four_guesses = ([1.0, 1.0], [-1.0, 1.0], [1.0, -1.0], [-1.0, -1.0])

print("(a) Original circle, radius^2 = 4, four starting guesses:")
found4 = find_intersections(4.0, four_guesses)
print(f"    Different intersections found: {len(found4)}")

print("(b) Bigger circle, radius^2 = 9:")
found9 = find_intersections(9.0, four_guesses)
print(f"    Different intersections found: {len(found9)}")
y9 = (-1 + np.sqrt(1 + 4 * 8)) / 2        # y^2 + y - 8 = 0
print(f"    Exact answer by algebra: x = +/-{np.sqrt(y9 + 1):.4f}, y = {y9:.4f}")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - a ship crossing a radar zone
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A coastal radar station at the origin (0, 0) detects objects within
#     10 km:                      x^2 + y^2 = 100   (edge of the radar zone)
#   * A ship follows a curved route  y = 0.1 x^2 - 3  (x, y in km).
#   * Where does the ship ENTER and LEAVE the radar zone?
print("\n=== PART 4: Where does the ship cross the radar boundary? ===")


def ship_radar(z):
    x, y = z
    return [x ** 2 + y ** 2 - 100.0,      # on the radar boundary
            y - (0.1 * x ** 2 - 3.0)]     # on the ship's route


crossings = []
for guess in ([-8.0, 5.0], [8.0, 5.0], [0.0, -9.0]):
    sol = root(ship_radar, guess)
    ok = sol.success and np.max(np.abs(ship_radar(sol.x))) < 1e-8
    print(f"guess {guess!s:>12} -> {np.round(sol.x, 4)}  converged: {ok}  "
          f"residuals: {np.round(ship_radar(sol.x), 10)}")
    if ok and not any(np.allclose(sol.x, c, atol=1e-5) for c in crossings):
        crossings.append(sol.x)

print(f"\nDistinct crossing points found: {len(crossings)}")
for point in sorted(crossings, key=lambda p: p[0]):
    print(f"  ({point[0]:.3f} km, {point[1]:.3f} km)  "
          f"distance from radar = {np.hypot(*point):.3f} km")

# Exact check: y^2 + 10y - 70 = 0 and x^2 = 10 (y + 3)
y_exact = (-10 + np.sqrt(100 + 280)) / 2
x_exact = np.sqrt(10 * (y_exact + 3))
print(f"Exact answer by algebra: x = +/-{x_exact:.3f}, y = {y_exact:.3f}")
inside = np.hypot(0, -3.0)
print(f"At x = 0 the ship is only {inside:.1f} km from the radar (closest approach)")
assert len(crossings) == 2
assert all(abs(abs(p[0]) - x_exact) < 1e-6 for p in crossings)
print("Self-check passed: two crossings, matching the algebra")

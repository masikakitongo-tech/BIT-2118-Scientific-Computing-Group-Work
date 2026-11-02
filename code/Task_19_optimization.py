# Task 19: Numerical Optimization
#
# Part 1 - the lecturer's small example: minimise f(x) = (x - 3)^2 + 2
# Part 2 - the lecturer's cloud-server problem (original solution code)
# Part 3 - changing costs and the required capacity
# Part 4 - a related real-world case (a workshop maximising its profit)

from pathlib import Path

import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - minimise f(x) = (x - 3)^2 + 2 ===")


def parabola(z):
    return (z[0] - 3) ** 2 + 2


small = minimize(parabola, x0=[0.0])
print(f"Minimum found at x = {small.x[0]:.6f}, f(x) = {small.fun:.6f}   (PDF: x = 3, minimum value 2)")
assert abs(small.x[0] - 3) < 1e-4 and abs(small.fun - 2) < 1e-8
print("Self-check passed: the minimum is at x = 3 with value 2")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's cloud-server problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Cheapest server allocation ===")

# x = number/capacity units of Type A server
# y = number/capacity units of Type B server
#
# Cost per unit: A = 12, B = 18
# Capacity per unit: A = 100, B = 170
# Required total capacity: at least 1000

def cost(z):
    x, y = z
    return 12*x + 18*y

def capacity_constraint(z):
    x, y = z
    return 100*x + 170*y - 1000

constraints = {
    "type": "ineq",
    "fun": capacity_constraint
}

bounds = [(0, None), (0, None)]

solution = minimize(
    cost,
    x0=[5, 3],
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

x, y = solution.x

print("Optimization success:", solution.success)
print(f"Type A allocation: {x:.3f}")
print(f"Type B allocation: {y:.3f}")
print(f"Total capacity: {100*x + 170*y:.2f}")
print(f"Minimum planning cost: {solution.fun:.2f}")

# If whole servers are required, test nearby integer combinations.
best_integer = None

for a in range(0, 20):
    for b in range(0, 20):
        capacity = 100*a + 170*b
        if capacity >= 1000:
            total_cost = 12*a + 18*b
            if best_integer is None or total_cost < best_integer[0]:
                best_integer = (total_cost, a, b, capacity)

print("Best nearby integer solution:", best_integer)
print("Cost per unit of capacity: A =", round(12 / 100, 4), "| B =", round(18 / 170, 4),
      "-> Type B is cheaper per unit of capacity")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")


def cheapest_allocation(cost_a, cost_b, required):
    """Return the continuous (SLSQP) optimum and the best whole-server plan."""
    sol = minimize(
        lambda z: cost_a * z[0] + cost_b * z[1],
        x0=[5, 3],
        method="SLSQP",
        bounds=[(0, None), (0, None)],
        constraints={"type": "ineq", "fun": lambda z: 100 * z[0] + 170 * z[1] - required},
    )
    best = None
    for n_a in range(0, 31):
        for n_b in range(0, 31):
            if 100 * n_a + 170 * n_b >= required:
                c = cost_a * n_a + cost_b * n_b
                if best is None or c < best[0]:
                    best = (c, n_a, n_b)
    return sol, best


print(f"{'Cost A':>7} {'Cost B':>7} {'Required':>9} | {'Units A':>8} {'Units B':>8} {'Min cost':>9} | {'Whole servers (cost, A, B)':>27}")
for cost_a, cost_b, required in ((12, 18, 1000), (12, 22, 1000), (12, 18, 1500)):
    sol, best = cheapest_allocation(cost_a, cost_b, required)
    print(f"{cost_a:>7} {cost_b:>7} {required:>9} | {sol.x[0]:>8.3f} {sol.x[1]:>8.3f} {sol.fun:>9.2f} | {str(best):>27}")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - a furniture workshop maximising profit
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A workshop makes tables (x) and chairs (y).
#   * Profit: KES 40 (thousand) per table, KES 30 (thousand) per chair.
#   * Each table needs 2 labour-hours and 3 units of wood; each chair needs
#     1 labour-hour and 4 units of wood.
#   * Available per week: 100 labour-hours and 240 units of wood.
#   * scipy's minimize can only MINIMISE, so we minimise the NEGATIVE profit.
print("\n=== PART 4: Furniture workshop - maximise weekly profit ===")


def best_plan(profit_table, profit_chair, labour=100.0, wood=240.0):
    """Return (continuous solution, best whole-number plan) for the workshop."""
    sol = minimize(
        lambda z: -(profit_table * z[0] + profit_chair * z[1]),
        x0=[10, 10],
        method="SLSQP",
        bounds=[(0, None), (0, None)],
        constraints=[
            {"type": "ineq", "fun": lambda z: labour - (2 * z[0] + 1 * z[1])},
            {"type": "ineq", "fun": lambda z: wood - (3 * z[0] + 4 * z[1])},
        ],
    )
    best = None
    for tables in range(0, 101):
        for chairs in range(0, 101):
            if 2 * tables + chairs <= labour and 3 * tables + 4 * chairs <= wood:
                p = profit_table * tables + profit_chair * chairs
                if best is None or p > best[0]:
                    best = (p, tables, chairs)
    return sol, best


sol, best = best_plan(40, 30)
tables, chairs = sol.x
print("Optimization success:", sol.success)
print(f"Tables per week: {tables:.2f}")
print(f"Chairs per week: {chairs:.2f}")
print(f"Maximum weekly profit: KES {-sol.fun:.2f} thousand")
print(f"Labour used: {2 * tables + chairs:.1f} of 100 hours | wood used: {3 * tables + 4 * chairs:.1f} of 240 units")
print("Best whole-number plan (profit, tables, chairs):", best)
assert sol.success and abs(-sol.fun - best[0]) < 1e-3
print("Self-check passed: the solver agrees with a brute-force search")

print("\nParameter changes:")
print(f"{'Profit/table':>13} {'Profit/chair':>13} {'Labour':>7} | {'Tables':>7} {'Chairs':>7} {'Profit':>8}")
for p_t, p_c, labour in ((40, 30, 100), (40, 60, 100), (40, 30, 120)):
    s, b = best_plan(p_t, p_c, labour=labour)
    print(f"{p_t:>13} {p_c:>13} {labour:>7} | {b[1]:>7} {b[2]:>7} {b[0]:>8}")

# Graph of the feasible region and the optimum.
xs = np.linspace(0, 60, 400)
labour_line = 100 - 2 * xs               # chairs allowed by labour
wood_line = (240 - 3 * xs) / 4           # chairs allowed by wood
limit = np.clip(np.minimum(labour_line, wood_line), 0, None)

plt.figure(figsize=(7, 5))
plt.fill_between(xs, 0, limit, alpha=0.3, label="Feasible plans")
plt.plot(xs, labour_line, label="Labour limit: 2x + y = 100")
plt.plot(xs, wood_line, label="Wood limit: 3x + 4y = 240")
plt.plot(xs, (-sol.fun - 40 * xs) / 30, "k--", label=f"Profit line = {-sol.fun:.0f}")
plt.scatter([tables], [chairs], color="red", zorder=5, label=f"Best plan ({tables:.0f} tables, {chairs:.0f} chairs)")
plt.xlim(0, 60)
plt.ylim(0, 80)
plt.xlabel("Tables per week (x)")
plt.ylabel("Chairs per week (y)")
plt.title("Workshop production plan: feasible region and optimum")
plt.legend(fontsize=8)
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_19_production_plan.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_19_production_plan.png")

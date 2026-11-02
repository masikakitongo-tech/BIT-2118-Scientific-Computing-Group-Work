# Task 10: Root Finding - Bisection and Fixed-Point Methods
#
# Part 1 - the lecturer's small example: bisection on f(x) = x^3 - x - 2
# Part 2 - the lecturer's heat-balance problem (original solution code)
# Part 3 - changing the bracket, the tolerance and the starting guess
# Part 4 - a related real-world case (break-even points of a business)

from pathlib import Path

import numpy as np
from scipy.optimize import root_scalar
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def bisection(f, a, b, tol=1e-6, max_iter=100):
    """Find a root of f between a and b by repeatedly halving the interval.

    f(a) and f(b) must have OPPOSITE signs, so a root lies between them.
    Returns the root and a list of (iteration, a, b, midpoint, f(midpoint)).
    """
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    steps = []
    for i in range(1, max_iter + 1):
        mid = (a + b) / 2
        steps.append((i, a, b, mid, f(mid)))
        if f(a) * f(mid) <= 0:           # the root is in the left half
            b = mid
        else:                            # the root is in the right half
            a = mid
        if (b - a) / 2 < tol:
            break
    return (a + b) / 2, steps


# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - bisection on f(x) = x^3 - x - 2 ===")


def cubic(x):
    return x ** 3 - x - 2


print("f(1) =", cubic(1), "and f(2) =", cubic(2),
      " -> different signs, so a root lies between 1 and 2")
root_small, steps = bisection(cubic, 1.0, 2.0, tol=1e-8)
print(f"{'Step':>4} {'a':>10} {'b':>10} {'midpoint':>10} {'f(mid)':>12}")
for i, a_, b_, mid, fmid in steps[:6]:
    print(f"{i:>4} {a_:>10.6f} {b_:>10.6f} {mid:>10.6f} {fmid:>12.6f}")
print(f"... after {len(steps)} halvings: root = {root_small:.8f}")
assert abs(cubic(root_small)) < 1e-6
print("Self-check passed: f(root) is almost 0")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's heat-balance problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Equilibrium temperature of a heat-balance equation ===")

# Heat-balance model:
# f(T) = 0 means heat gain equals heat loss.
def heat_balance(T):
    return T - 25 - 10*np.exp(-T/20)

# Bisection: bracket a sign change
solution = root_scalar(
    heat_balance,
    bracket=[20, 40],
    method="bisect",
    xtol=1e-10
)

# Fixed-point form:
# T = 25 + 10*exp(-T/20)
def g(T):
    return 25 + 10*np.exp(-T/20)

T = 30.0
history = [T]

for _ in range(100):
    T_new = g(T)
    history.append(T_new)

    if abs(T_new - T) < 1e-10:
        break

    T = T_new

print(f"Bisection equilibrium temperature: {solution.root:.6f} C")
print(f"Fixed-point equilibrium temperature: {history[-1]:.6f} C")
print("Fixed-point iterations:", len(history) - 1)
print("Bisection iterations:", solution.iterations)
assert abs(solution.root - history[-1]) < 1e-8
print("Self-check passed: both methods give the same temperature")

temps = np.linspace(20, 40, 300)
plt.plot(temps, heat_balance(temps))
plt.axhline(0, linewidth=0.8)
plt.axvline(solution.root, linestyle="--")
plt.xlabel("Temperature (C)")
plt.ylabel("Heat-balance function")
plt.title("Equilibrium temperature")
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_10_equilibrium_temperature.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_10_equilibrium_temperature.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) Change the bracket and the tolerance for bisection.
print("(a) Bisection with different brackets and tolerances:")
print(f"{'Bracket':>10} {'xtol':>7} {'Iterations':>11} {'Root':>12}")
for bracket in ([20, 40], [25, 30], [27, 28]):
    for xtol in (1e-3, 1e-10):
        s = root_scalar(heat_balance, bracket=bracket, method="bisect", xtol=xtol)
        print(f"{str(bracket):>10} {xtol:>7.0e} {s.iterations:>11} {s.root:>12.8f}")

# (b) A bracket WITHOUT a sign change cannot work.
print("\n(b) A bad bracket [30, 40] (f is positive at both ends):")
print(f"    f(30) = {heat_balance(30):.4f}, f(40) = {heat_balance(40):.4f}")
try:
    root_scalar(heat_balance, bracket=[30, 40], method="bisect")
except ValueError as error:
    print("    root_scalar refused:", error)

# (c) Change the starting guess of the fixed-point method.
print("\n(c) Fixed-point iteration from different starting temperatures:")
for start in (0.0, 30.0, 100.0):
    T = start
    count = 0
    for count in range(1, 101):
        T_new = g(T)
        if abs(T_new - T) < 1e-10:
            break
        T = T_new
    print(f"    start = {start:>5.1f} C -> {T_new:.6f} C after {count} iterations")
print("    (It converges because |g'(T)| = 0.5*exp(-T/20) is well below 1 here.)")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - break-even points of a business
# ---------------------------------------------------------------------------
# Assumptions (all simulated, amounts in KES):
#   * Selling q units gives revenue  R(q) = 80 q - 0.005 q^2
#     (the price must fall a little when we sell more).
#   * Producing q units costs        C(q) = 5000 + 20 q + 0.02 q^2
#     (5000 fixed cost, 20 per unit, and costs that rise at high volume).
#   * Profit P(q) = R(q) - C(q) = 60 q - 0.025 q^2 - 5000.
#   * A break-even point is where P(q) = 0.
print("\n=== PART 4: Break-even points of a business ===")


def profit(q):
    revenue = 80 * q - 0.005 * q ** 2
    cost = 5000 + 20 * q + 0.02 * q ** 2
    return revenue - cost


# Two sign changes exist, so two brackets are needed.
lower_be, _ = bisection(profit, 0, 500, tol=1e-6)
upper_be, _ = bisection(profit, 1000, 4000, tol=1e-6)

# Exact answers from the quadratic formula, for checking.
disc = np.sqrt(60 ** 2 - 4 * 0.025 * 5000)
exact_lower, exact_upper = (60 - disc) / 0.05, (60 + disc) / 0.05
q_best = 60 / (2 * 0.025)                # where profit is largest

print(f"Lower break-even point: {lower_be:.2f} units (exact {exact_lower:.2f})")
print(f"Upper break-even point: {upper_be:.2f} units (exact {exact_upper:.2f})")
print(f"Most profitable quantity: {q_best:.0f} units, profit = KES {profit(q_best):,.0f}")
print(f"Profit at 50 units:   KES {profit(50):,.0f}")
print(f"Profit at 500 units:  KES {profit(500):,.0f}")
print(f"Profit at 3000 units: KES {profit(3000):,.0f}")
assert abs(lower_be - exact_lower) < 1e-3 and abs(upper_be - exact_upper) < 1e-3
print("Self-check passed: bisection matches the quadratic formula")

q = np.linspace(0, 2600, 400)
plt.plot(q, profit(q), label="Profit")
plt.axhline(0, linewidth=0.8, color="black")
plt.axvline(lower_be, linestyle="--", color="green", label=f"Break-even {lower_be:.0f}")
plt.axvline(upper_be, linestyle="--", color="red", label=f"Break-even {upper_be:.0f}")
plt.scatter([q_best], [profit(q_best)], color="purple", zorder=3,
            label=f"Maximum profit at {q_best:.0f} units")
plt.xlabel("Units produced and sold (q)")
plt.ylabel("Profit (KES)")
plt.title("Break-even points found by bisection")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_10_break_even.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_10_break_even.png")

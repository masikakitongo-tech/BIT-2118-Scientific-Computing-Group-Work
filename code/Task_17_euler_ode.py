# Task 17: Ordinary Differential Equations - Euler Method
#
# Part 1 - the lecturer's small example: dy/dt = y, y(0) = 1, h = 0.1
# Part 2 - the lecturer's cooling problem (original solution code)
# Part 3 - changing the step size h and the cooling constant k
# Part 4 - a related real-world case (logistic growth of a bacteria colony)

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - dy/dt = y, y(0) = 1, h = 0.1 ===")
# Euler:  y_new = y + h * f(t, y)   with f(t, y) = y
y = 1.0
h = 0.1
print(f"t = 0.0: y = {y:.4f}")
for step in range(1, 11):
    y = y + h * y                        # one Euler step
    if step <= 3 or step == 10:
        print(f"t = {step * h:.1f}: y = {y:.4f}")
print(f"Exact answer at t = 1: e = {np.e:.4f}; Euler error = {abs(np.e - y):.4f}")
assert abs(1 + 0.1 * 1 - 1.1) < 1e-12 and abs((1.1 + 0.1 * 1.1) - 1.21) < 1e-12
print("Self-check passed: y1 = 1.1 and y2 = 1.21, as in the PDF")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's cooling problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Cooling of a hot object (Newton's law of cooling) ===")

# Newton's law of cooling:
# dT/dt = -k(T - T_ambient)
T_ambient = 25.0
T_initial = 90.0
k = 0.12
h = 1.0  # minutes
end_time = 30.0

def cooling_rate(T):
    return -k * (T - T_ambient)

time = np.arange(0, end_time + h, h)
temperature = np.zeros_like(time)
temperature[0] = T_initial

for i in range(len(time) - 1):
    temperature[i + 1] = (
        temperature[i] + h * cooling_rate(temperature[i])
    )

# Exact solution for validation
exact = T_ambient + (T_initial - T_ambient) * np.exp(-k * time)

print(f"Euler temperature after 30 min: {temperature[-1]:.2f} C")
print(f"Exact temperature after 30 min: {exact[-1]:.2f} C")
print(f"Final absolute error: {abs(temperature[-1]-exact[-1]):.4f} C")

plt.plot(time, temperature, marker="o", label="Euler")
plt.plot(time, exact, label="Exact solution")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (C)")
plt.title("Cooling of a hot object")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_17_cooling.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_17_cooling.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")


def euler_cooling(k_value, step, end=30.0):
    """Euler solution of the cooling equation. Returns (times, temperatures)."""
    n_steps = int(round(end / step))
    t = np.linspace(0, end, n_steps + 1)
    T = np.zeros(n_steps + 1)
    T[0] = T_initial
    for i in range(n_steps):
        T[i + 1] = T[i] + step * (-k_value * (T[i] - T_ambient))
    return t, T


# (a) Change the step size h.
print("(a) Different step sizes h (k = 0.12):")
print(f"{'h (min)':>8} {'Steps':>6} {'Euler at 30 min':>16} {'Exact':>8} {'Error':>8}")
exact_end = T_ambient + (T_initial - T_ambient) * np.exp(-0.12 * 30.0)
step_curves = {}
for step in (5.0, 2.0, 1.0, 0.5, 0.1):
    t_s, T_s = euler_cooling(0.12, step)
    step_curves[step] = (t_s, T_s)
    print(f"{step:>8} {len(t_s) - 1:>6} {T_s[-1]:>16.3f} {exact_end:>8.3f} {abs(T_s[-1] - exact_end):>8.3f}")

# (b) Change the cooling constant k (a metal cup cools faster than a wooden one).
print("\n(b) Different cooling constants k (h = 1 min):")
for k_value in (0.06, 0.12, 0.30):
    t_k, T_k = euler_cooling(k_value, 1.0)
    exact_k = T_ambient + (T_initial - T_ambient) * np.exp(-k_value * 30.0)
    print(f"    k = {k_value:.2f}: Euler = {T_k[-1]:.2f} C, exact = {exact_k:.2f} C")

# (c) If h is too large the method can become unstable.
t_bad, T_bad = euler_cooling(2.5, 1.0, end=8.0)
print("\n(c) A very large k = 2.5 with h = 1 min (k*h > 2 -> unstable):")
print("    Euler temperatures:", np.round(T_bad[:6], 1), "...")
print("    The true temperature should always fall smoothly towards 25 C - Euler swings wildly.")

plt.figure()
for step, (t_s, T_s) in step_curves.items():
    plt.plot(t_s, T_s, label=f"Euler, h = {step}")
t_fine = np.linspace(0, 30, 300)
plt.plot(t_fine, T_ambient + (T_initial - T_ambient) * np.exp(-0.12 * t_fine),
         "k--", label="Exact solution")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (C)")
plt.title("Effect of the Euler step size h")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_17_step_sizes.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_17_step_sizes.png")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - logistic growth of a bacteria colony
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A culture starts with 10 (hundred) bacteria, grows with rate r = 0.4
#     per day, and the dish can support at most K = 1000 (hundred).
#   * Logistic equation:  dP/dt = r P (1 - P / K)
#     Growth is fast at first, then slows as the dish fills up.
#   * Exact solution (for checking): P(t) = K / (1 + ((K - P0) / P0) e^(-r t))
print("\n=== PART 4: Logistic growth of a bacteria colony ===")
r, K, P0 = 0.4, 1000.0, 10.0
end_days = 30.0


def euler_logistic(step):
    n_steps = int(round(end_days / step))
    t = np.linspace(0, end_days, n_steps + 1)
    P = np.zeros(n_steps + 1)
    P[0] = P0
    for i in range(n_steps):
        P[i + 1] = P[i] + step * r * P[i] * (1 - P[i] / K)
    return t, P


def exact_logistic(t):
    return K / (1 + ((K - P0) / P0) * np.exp(-r * t))


t_coarse, P_coarse = euler_logistic(2.0)
t_fine_step, P_fine_step = euler_logistic(0.5)

print(f"{'Day':>4} {'Exact':>9} {'Euler h=2':>10} {'Euler h=0.5':>12}")
for day in (0, 10, 20, 30):
    i2 = int(round(day / 2.0))
    i05 = int(round(day / 0.5))
    print(f"{day:>4} {exact_logistic(day):>9.1f} {P_coarse[i2]:>10.1f} {P_fine_step[i05]:>12.1f}")

max_err_coarse = np.max(np.abs(P_coarse - exact_logistic(t_coarse)))
max_err_fine = np.max(np.abs(P_fine_step - exact_logistic(t_fine_step)))
half_time = np.log((K - P0) / P0) / r
print(f"Largest error: h = 2 -> {max_err_coarse:.1f}; h = 0.5 -> {max_err_fine:.1f} (hundred bacteria)")
print(f"Colony reaches half of capacity (500) after {half_time:.1f} days")
assert max_err_fine < max_err_coarse
print("Self-check passed: the smaller step size gives the smaller error")

t_plot = np.linspace(0, end_days, 300)
plt.figure()
plt.plot(t_plot, exact_logistic(t_plot), "k-", label="Exact solution")
plt.plot(t_coarse, P_coarse, "o--", label="Euler, h = 2 days")
plt.plot(t_fine_step, P_fine_step, "-", label="Euler, h = 0.5 days")
plt.axhline(K, color="gray", linewidth=0.8)
plt.xlabel("Time (days)")
plt.ylabel("Bacteria (hundreds)")
plt.title("Logistic growth of a bacteria colony")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_17_logistic_growth.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_17_logistic_growth.png")

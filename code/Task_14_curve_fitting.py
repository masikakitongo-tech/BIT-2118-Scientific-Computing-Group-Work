# Task 14: Curve Fitting and Approximation
#
# Part 1 - the lecturer's small example: fit a straight line y = a + b x
# Part 2 - the lecturer's server problem (original solution code) + residuals
# Part 3 - changing the model and one measurement
# Part 4 - a related real-world case (growth of app users - exponential curve)

from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example - least squares for y = a + b x
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - fitting a straight line ===")
x_line = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y_line = np.array([2.1, 3.9, 6.2, 7.8, 10.1])      # roughly y = 2x


def sum_squared_residuals(a, b):
    """Sum of (observed - predicted)^2 for the line y = a + b x."""
    return np.sum((y_line - (a + b * x_line)) ** 2)


b_fit, a_fit = np.polyfit(x_line, y_line, 1)       # least-squares line
print(f"Least-squares line: y = {a_fit:.4f} + {b_fit:.4f} x")
print(f"Sum of squared residuals for this line:     {sum_squared_residuals(a_fit, b_fit):.4f}")
print(f"Sum of squared residuals for y = 2x:        {sum_squared_residuals(0.0, 2.0):.4f}")
print(f"Sum of squared residuals for y = 0.5 + 1.8x: {sum_squared_residuals(0.5, 1.8):.4f}")
assert sum_squared_residuals(a_fit, b_fit) <= sum_squared_residuals(0.0, 2.0)
print("Self-check passed: the fitted line has the smallest sum of squared residuals")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's server problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Server response time against number of users ===")

# Concurrent users and measured server response time (milliseconds)
users = np.array([50, 100, 150, 200, 250, 300, 350], dtype=float)
response_ms = np.array([82, 95, 115, 145, 185, 238, 305], dtype=float)

# A simple quadratic model for increasing delay
def model(x, a, b, c):
    return a*x**2 + b*x + c

parameters, covariance = curve_fit(model, users, response_ms)
a, b, c = parameters

predicted = model(users, a, b, c)
rmse = np.sqrt(np.mean((response_ms - predicted)**2))

print(f"Fitted model: y = {a:.6f}x^2 + {b:.4f}x + {c:.2f}")
print(f"RMSE: {rmse:.2f} ms")
print(f"Predicted response at 400 users: {model(400, a, b, c):.2f} ms")

residuals = response_ms - predicted
print("Residuals (measured - predicted) in ms:", np.round(residuals, 2))

x_plot = np.linspace(users.min(), 400, 300)
plt.scatter(users, response_ms, label="Measurements")
plt.plot(x_plot, model(x_plot, a, b, c), label="Fitted curve")
plt.xlabel("Concurrent users")
plt.ylabel("Response time (ms)")
plt.title("Server response-time curve fitting")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_14_response_time_fit.png", dpi=150, bbox_inches="tight")
plt.close()

# Residual plot: a good model leaves small residuals with no pattern.
plt.stem(users, residuals)
plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel("Concurrent users")
plt.ylabel("Residual (ms)")
plt.title("Residuals of the quadratic fit")
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_14_residuals.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graphs saved: results/Task_14_response_time_fit.png, results/Task_14_residuals.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) Change the model: straight line, quadratic, cubic.
print("(a) Different polynomial models for the same measurements:")
print(f"{'Degree':>7} {'RMSE (ms)':>10} {'Prediction at 400 users (ms)':>30}")
for degree in (1, 2, 3):
    coeffs = np.polyfit(users, response_ms, degree)
    fit_values = np.polyval(coeffs, users)
    err = np.sqrt(np.mean((response_ms - fit_values) ** 2))
    print(f"{degree:>7} {err:>10.2f} {np.polyval(coeffs, 400):>30.2f}")

# (b) Change one measurement: at 350 users the response time is 340 ms, not 305.
response_changed = response_ms.copy()
response_changed[-1] = 340.0
p_new, _ = curve_fit(model, users, response_changed)
print("\n(b) The 350-user measurement changed from 305 ms to 340 ms:")
print(f"    before: y = {a:.6f}x^2 + {b:.4f}x + {c:.2f}  -> 400 users: {model(400, a, b, c):.2f} ms")
print(f"    after:  y = {p_new[0]:.6f}x^2 + {p_new[1]:.4f}x + {p_new[2]:.2f}  "
      f"-> 400 users: {model(400, *p_new):.2f} ms")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - growth of a mobile app's users
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * Active users (in thousands) at the end of months 1 to 8.
#   * Growth looks exponential:   users(t) = A * exp(B * t)
#     (each month the user base grows by about the same percentage).
#   * We fit A and B, compare with a straight line, and forecast month 10.
print("\n=== PART 4: Exponential growth of app users ===")
months = np.arange(1, 9, dtype=float)
users_k = np.array([120, 150, 195, 250, 320, 410, 530, 680], dtype=float)


def growth(t, A, B):
    return A * np.exp(B * t)


(A_fit, B_fit), _ = curve_fit(growth, months, users_k, p0=(100.0, 0.2))
fit_growth = growth(months, A_fit, B_fit)
rmse_growth = np.sqrt(np.mean((users_k - fit_growth) ** 2))

line_coeffs = np.polyfit(months, users_k, 1)
rmse_line = np.sqrt(np.mean((users_k - np.polyval(line_coeffs, months)) ** 2))

print(f"Fitted model: users = {A_fit:.2f} * exp({B_fit:.4f} * month)")
print(f"Monthly growth rate: {np.exp(B_fit) - 1:.1%}")
print(f"Doubling time: {np.log(2) / B_fit:.2f} months")
print(f"RMSE exponential model: {rmse_growth:.2f} thousand users")
print(f"RMSE straight-line model: {rmse_line:.2f} thousand users")
print(f"Forecast for month 10: exponential = {growth(10, A_fit, B_fit):.0f} thousand, "
      f"straight line = {np.polyval(line_coeffs, 10):.0f} thousand")
assert rmse_growth < rmse_line
print("Self-check passed: the exponential curve fits better than a straight line")

t_plot = np.linspace(1, 10, 200)
plt.scatter(months, users_k, label="Observed users")
plt.plot(t_plot, growth(t_plot, A_fit, B_fit), label="Exponential fit")
plt.plot(t_plot, np.polyval(line_coeffs, t_plot), "--", label="Straight-line fit")
plt.xlabel("Month")
plt.ylabel("Active users (thousands)")
plt.title("Growth of app users: exponential curve fitting")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_14_user_growth.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_14_user_growth.png")

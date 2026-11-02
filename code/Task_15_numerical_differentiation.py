# Task 15: Numerical Differentiation
#
# Part 1 - the lecturer's small example (100 m -> 112 m in 2 s) + step-size study
# Part 2 - the lecturer's GPS problem: speed from position (original solution code)
# Part 3 - changing one position reading
# Part 4 - a related real-world case (acceleration of a car from speed readings)

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example + how the step size h affects the error
# ---------------------------------------------------------------------------
print("=== PART 1: Small example from the PDF ===")
average_speed = (112 - 100) / 2
print(f"Distance changes from 100 m to 112 m in 2 s: average speed = {average_speed} m/s (PDF: 6 m/s)")
assert average_speed == 6.0

# Step-size study on a function whose exact derivative we know:
#   f(x) = sin(x)  has derivative  cos(x).   We estimate f'(1).
#   forward difference: [f(x+h) - f(x)] / h
#   central difference: [f(x+h) - f(x-h)] / (2h)
x0 = 1.0
exact = np.cos(x0)
step_sizes = 10.0 ** -np.arange(1, 13)    # 0.1, 0.01, ... 1e-12
forward_errors, central_errors = [], []

print(f"\nEstimating the derivative of sin(x) at x = 1 (exact = cos(1) = {exact:.10f})")
print(f"{'h':>8} {'Forward error':>15} {'Central error':>15}")
for h in step_sizes:
    forward = (np.sin(x0 + h) - np.sin(x0)) / h
    central = (np.sin(x0 + h) - np.sin(x0 - h)) / (2 * h)
    forward_errors.append(abs(forward - exact))
    central_errors.append(abs(central - exact))
    print(f"{h:>8.0e} {forward_errors[-1]:>15.3e} {central_errors[-1]:>15.3e}")

best_f = step_sizes[int(np.argmin(forward_errors))]
best_c = step_sizes[int(np.argmin(central_errors))]
print(f"Smallest forward error at h = {best_f:.0e}; smallest central error at h = {best_c:.0e}")
assert min(central_errors) < min(forward_errors)
print("Self-check passed: the central difference reaches a smaller error than the forward difference")

plt.loglog(step_sizes, forward_errors, "o-", label="Forward difference")
plt.loglog(step_sizes, central_errors, "s-", label="Central difference")
plt.xlabel("Step size h")
plt.ylabel("Absolute error in the derivative")
plt.title("Error of numerical derivatives against step size")
plt.legend()
plt.grid(True, which="both")
plt.savefig(RESULTS_DIR / "Task_15_step_size_error.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_15_step_size_error.png")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's GPS problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Speed estimated from GPS positions ===")

# GPS samples: time in seconds and position in metres
time = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
position = np.array([0.0, 4.8, 10.2, 16.1, 22.7, 30.0, 38.0])

speed = np.zeros_like(position)

# Forward difference at the beginning
speed[0] = (position[1] - position[0]) / (time[1] - time[0])

# Central differences for interior points
for i in range(1, len(time) - 1):
    speed[i] = (
        position[i + 1] - position[i - 1]
    ) / (
        time[i + 1] - time[i - 1]
    )

# Backward difference at the end
speed[-1] = (
    position[-1] - position[-2]
) / (
    time[-1] - time[-2]
)

for t, x, v in zip(time, position, speed):
    print(f"t={t:.0f}s, position={x:.1f}m, estimated speed={v:.2f}m/s")

# Self-check: NumPy's built-in np.gradient uses the same formulas.
assert np.allclose(speed, np.gradient(position, time))
print("Self-check passed: the result equals NumPy's np.gradient")

plt.plot(time, speed, marker="o")
plt.xlabel("Time (s)")
plt.ylabel("Estimated speed (m/s)")
plt.title("Speed estimated from GPS position data")
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_15_gps_speed.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_15_gps_speed.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter change - one position reading is different
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter change ===")
position_changed = position.copy()
position_changed[4] = 25.0               # the reading at t = 4 s: 22.7 m -> 25.0 m
speed_changed = np.gradient(position_changed, time)

print("The position at t = 4 s changed from 22.7 m to 25.0 m")
print(f"{'t (s)':>6} {'Speed before':>13} {'Speed after':>12} {'Change':>8}")
for t, before, after in zip(time, speed, speed_changed):
    print(f"{t:>6.0f} {before:>13.2f} {after:>12.2f} {after - before:>+8.2f}")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - acceleration of a car from speed readings
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A car's speedometer is read every second for 10 seconds after the
#     driver pulls away from rest. Speeds are in metres per second.
#   * Acceleration is the rate of change of speed, so we apply the same
#     differentiation formulas (np.gradient) to the speed readings.
print("\n=== PART 4: Acceleration of a car from speed readings ===")
t_car = np.arange(0, 11, dtype=float)    # 0, 1, ..., 10 seconds
v_car = np.array([0.0, 2.1, 4.3, 6.2, 8.0, 9.6, 11.0, 12.1, 12.9, 13.4, 13.6])
a_car = np.gradient(v_car, t_car)        # acceleration in m/s^2

print(f"{'t (s)':>6} {'Speed (m/s)':>12} {'Acceleration (m/s^2)':>22}")
for t, v, a in zip(t_car, v_car, a_car):
    print(f"{t:>6.0f} {v:>12.1f} {a:>22.2f}")

peak = int(np.argmax(a_car))
print(f"Largest acceleration: {a_car[peak]:.2f} m/s^2 at t = {t_car[peak]:.0f} s")
print(f"Average acceleration over 10 s: {(v_car[-1] - v_car[0]) / 10:.2f} m/s^2")
print(f"Top speed reached: {v_car[-1]} m/s = {v_car[-1] * 3.6:.1f} km/h")

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))
ax1.plot(t_car, v_car, "o-")
ax1.set_ylabel("Speed (m/s)")
ax1.set_title("A car pulling away: speed and acceleration")
ax1.grid(True)
ax2.plot(t_car, a_car, "s-", color="tab:red")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Acceleration (m/s^2)")
ax2.grid(True)
plt.savefig(RESULTS_DIR / "Task_15_car_acceleration.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_15_car_acceleration.png")

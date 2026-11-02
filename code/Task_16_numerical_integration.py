# Task 16: Numerical Integration
#
# Part 1 - the lecturer's small example (2 kW for 3 h) + accuracy of the rules
# Part 2 - the lecturer's smart-meter problem (original solution code)
# Part 3 - changing a reading and the number of samples
# Part 4 - a related real-world case (distance travelled by a delivery rider)

from pathlib import Path

import numpy as np
from scipy.integrate import simpson, quad
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example from the PDF ===")
# Constant power of 2 kW for 3 hours: energy = integral of P dt = 2 x 3 = 6 kWh
t_const = np.array([0.0, 1.0, 2.0, 3.0])
p_const = np.array([2.0, 2.0, 2.0, 2.0])
energy_const = np.trapezoid(p_const, t_const)
print(f"Energy for 2 kW over 3 h: {energy_const} kWh  (PDF: 6 kWh)")
assert energy_const == 6.0

# How accurate are the rules? Integrate f(x) = sin(x) from 0 to pi (exact = 2).
print("\nIntegral of sin(x) from 0 to pi (exact answer = 2) with different numbers of samples:")
print(f"{'Samples':>8} {'Trapezoid error':>16} {'Simpson error':>15}")
for n_samples in (5, 9, 17, 33):
    xs = np.linspace(0, np.pi, n_samples)
    ys = np.sin(xs)
    err_trap = abs(np.trapezoid(ys, xs) - 2.0)
    err_simp = abs(simpson(ys, x=xs) - 2.0)
    print(f"{n_samples:>8} {err_trap:>16.2e} {err_simp:>15.2e}")

value, estimated_error = quad(np.sin, 0, np.pi)      # adaptive quadrature
print(f"SciPy adaptive quad: {value:.12f} (estimated error {estimated_error:.1e})")
assert abs(value - 2.0) < 1e-12
print("Self-check passed: Simpson is far more accurate than the trapezoidal rule")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's smart-meter problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Energy used according to a smart meter ===")

# Smart-meter readings taken every two hours
time_hours = np.array([0, 2, 4, 6, 8, 10, 12], dtype=float)
power_kw = np.array([0.8, 1.0, 1.4, 1.8, 1.6, 1.2, 0.9])

energy_trapezoid = np.trapezoid(power_kw, time_hours)
energy_simpson = simpson(power_kw, x=time_hours)

print(f"Energy using trapezoidal rule: {energy_trapezoid:.3f} kWh")
print(f"Energy using Simpson's rule:   {energy_simpson:.3f} kWh")
print(f"Difference between estimates:  {abs(energy_simpson-energy_trapezoid):.3f} kWh")

# Graph: the shaded area under the power curve IS the energy used.
plt.plot(time_hours, power_kw, "o-", label="Meter readings")
plt.fill_between(time_hours, power_kw, alpha=0.3,
                 label=f"Area = energy = {energy_trapezoid:.2f} kWh (trapezoid)")
plt.xlabel("Time (hours)")
plt.ylabel("Power (kW)")
plt.title("Energy as the area under the power curve")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_16_energy_area.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_16_energy_area.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) The reading at 6:00 is 2.4 kW instead of 1.8 kW.
power_changed = power_kw.copy()
power_changed[3] = 2.4
print("(a) The reading at 6 h changed from 1.8 kW to 2.4 kW:")
print(f"    trapezoid: {energy_trapezoid:.3f} -> {np.trapezoid(power_changed, time_hours):.3f} kWh")
print(f"    Simpson:   {energy_simpson:.3f} -> {simpson(power_changed, x=time_hours):.3f} kWh")

# (b) Use only every second reading (every four hours instead of two).
t_coarse, p_coarse = time_hours[::2], power_kw[::2]
print("\n(b) Using only the readings at 0, 4, 8 and 12 h:")
print(f"    trapezoid: {energy_trapezoid:.3f} -> {np.trapezoid(p_coarse, t_coarse):.3f} kWh")
print(f"    Simpson:   {energy_simpson:.3f} -> {simpson(p_coarse, x=t_coarse):.3f} kWh")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - distance travelled by a delivery rider
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A delivery motorcycle rider's speed (km/h) is recorded every minute
#     for a 10-minute trip.
#   * Distance = integral of speed over time. Time must be in HOURS because
#     speed is in km per HOUR (1 minute = 1/60 hour).
print("\n=== PART 4: Distance travelled by a delivery rider ===")
minutes = np.arange(0, 11, dtype=float)
speed_kmh = np.array([0.0, 12.0, 25.0, 30.0, 28.0, 32.0, 35.0, 30.0, 22.0, 10.0, 0.0])
hours = minutes / 60.0

distance_trap = np.trapezoid(speed_kmh, hours)
distance_simp = simpson(speed_kmh, x=hours)
average_speed = distance_trap / hours[-1]

print(f"Distance (trapezoidal rule): {distance_trap:.3f} km")
print(f"Distance (Simpson's rule):   {distance_simp:.3f} km")
print(f"Average speed over the trip: {average_speed:.1f} km/h")
print(f"Top speed recorded:          {speed_kmh.max():.0f} km/h")
print(f"Wrong shortcut (mean of readings x 10 min): {speed_kmh.mean() * 10 / 60:.3f} km")
assert abs(distance_trap - distance_simp) < 0.1
print("Self-check passed: both rules agree to within 0.1 km")

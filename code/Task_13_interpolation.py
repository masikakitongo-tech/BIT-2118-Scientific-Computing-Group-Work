# Task 13: Interpolation
#
# Part 1 - the lecturer's small example: 20 C at 10:00 and 24 C at 12:00
# Part 2 - the lecturer's hourly-temperature problem (original solution code)
# Part 3 - changing a measurement, comparing methods, and extrapolation
# Part 4 - a related real-world case (calibrating a temperature sensor)

from pathlib import Path

import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - linear interpolation ===")
# 20 C at 10:00 and 24 C at 12:00.  What is the temperature at 11:00?
# Straight line between the points: 20 + (24 - 20) * (11 - 10) / (12 - 10) = 22
estimate = np.interp(11, [10, 12], [20, 24])
print(f"Estimated temperature at 11:00: {estimate} C   (PDF: 22 C)")
assert estimate == 22.0
print("Self-check passed: the estimate is 22 C")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's hourly-temperature problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Hourly measurements -> estimates every 10 minutes ===")

# Hourly temperature measurements
hours = np.array([8, 9, 10, 11, 12, 13, 14], dtype=float)
temperature = np.array([18.0, 20.0, 22.5, 24.0, 25.0, 25.5, 25.0])

linear = interp1d(hours, temperature, kind="linear")
cubic = CubicSpline(hours, temperature)

# Estimate every 10 minutes = 1/6 hour
ten_minute_times = np.arange(8, 14 + 1/6, 1/6)

linear_estimates = linear(ten_minute_times)
cubic_estimates = cubic(ten_minute_times)

target_time = 10.5  # 10:30
print(f"Linear estimate at 10:30: {float(linear(target_time)):.2f} C")
print(f"Cubic estimate at 10:30:  {float(cubic(target_time)):.2f} C")

print(f"Number of 10-minute times: {len(ten_minute_times)}; "
      f"last time = {ten_minute_times[-1]!r} "
      f"(14 would be exact; np.arange accumulates tiny floating-point errors)")
# Both methods must return the original measurements at the measured hours.
assert np.allclose(linear(hours), temperature) and np.allclose(cubic(hours), temperature)
print("Self-check passed: both curves pass through every measured point")

plt.scatter(hours, temperature, label="Hourly measurements")
plt.plot(ten_minute_times, linear_estimates, label="Linear")
plt.plot(ten_minute_times, cubic_estimates, label="Cubic spline")
plt.xlabel("Hour of day")
plt.ylabel("Temperature (C)")
plt.title("Temperature interpolation")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_13_temperature_interpolation.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_13_temperature_interpolation.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) Change one measurement: the 11:00 reading goes from 24.0 to 26.0 C.
changed = temperature.copy()
changed[3] = 26.0                        # index 3 is 11:00
linear_c = interp1d(hours, changed, kind="linear")
cubic_c = CubicSpline(hours, changed)
print("(a) The 11:00 reading changed from 24.0 C to 26.0 C:")
print(f"{'Method':<8} {'10:30 before':>13} {'10:30 after':>12} {'12:30 before':>13} {'12:30 after':>12}")
print(f"{'Linear':<8} {float(linear(10.5)):>13.2f} {float(linear_c(10.5)):>12.2f} "
      f"{float(linear(12.5)):>13.2f} {float(linear_c(12.5)):>12.2f}")
print(f"{'Cubic':<8} {float(cubic(10.5)):>13.2f} {float(cubic_c(10.5)):>12.2f} "
      f"{float(cubic(12.5)):>13.2f} {float(cubic_c(12.5)):>12.2f}")

# (b) Where do the two methods disagree most?
fine = np.linspace(8, 14, 601)           # linspace ends exactly at 14
difference = np.abs(cubic(fine) - linear(fine))
worst = fine[np.argmax(difference)]
print(f"\n(b) Largest gap between linear and cubic: {difference.max():.3f} C "
      f"at {int(worst)}:{int(round((worst % 1) * 60)):02d}")

# (c) Interpolation is only safe INSIDE the measured range.
print("\n(c) Asking for 15:00 (after the last measurement at 14:00):")
try:
    linear(15.0)
except ValueError as error:
    print("    interp1d refused:", error)
print(f"    CubicSpline extrapolates anyway and gives {float(cubic(15.0)):.2f} C "
      f"- do not trust it!")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - calibrating a temperature sensor
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A temperature sensor outputs a voltage. The manufacturer's calibration
#     table gives the true temperature for six voltages.
#   * The relationship is smooth but NOT a straight line (the temperature
#     rises more slowly at higher voltages).
#   * In use the sensor reads voltages that are not in the table, so we
#     interpolate to estimate the temperature.
print("\n=== PART 4: Sensor calibration lookup table ===")
volts_table = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
temp_table = np.array([0.0, 25.0, 48.0, 68.0, 85.0, 100.0])

lin_cal = interp1d(volts_table, temp_table, kind="linear")
cub_cal = CubicSpline(volts_table, temp_table)

readings = np.array([0.75, 1.80, 2.70, 2.95])        # new sensor voltages
print(f"{'Voltage (V)':>12} {'Linear (C)':>11} {'Cubic (C)':>10} {'Difference':>11}")
for v, tl, tc in zip(readings, lin_cal(readings), cub_cal(readings)):
    print(f"{v:>12.2f} {tl:>11.2f} {tc:>10.2f} {abs(tc - tl):>11.2f}")
assert np.allclose(cub_cal(volts_table), temp_table)

volts_fine = np.linspace(0.5, 3.0, 300)
plt.scatter(volts_table, temp_table, color="black", zorder=3, label="Calibration table")
plt.plot(volts_fine, lin_cal(volts_fine), "--", label="Linear interpolation")
plt.plot(volts_fine, cub_cal(volts_fine), label="Cubic spline")
plt.scatter(readings, cub_cal(readings), color="red", zorder=4, label="New readings (cubic)")
plt.xlabel("Sensor voltage (V)")
plt.ylabel("Temperature (C)")
plt.title("Sensor calibration by interpolation")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_13_sensor_calibration.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_13_sensor_calibration.png")

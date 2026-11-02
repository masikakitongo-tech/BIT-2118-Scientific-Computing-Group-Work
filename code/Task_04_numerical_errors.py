# Task 4: Floating-Point Arithmetic and Numerical Errors
#
# Part 1 - the lecturer's examples (0.1 + 0.2, sqrt(2) error, unstable formula)
# Part 2 - (same code as Part 1; the PDF solution code is kept unchanged)
# Part 3 - changing inputs and observing how the errors change
# Part 4 - a related real-world case (measurement accuracy check)

import numpy as np

# ---------------------------------------------------------------------------
# PARTS 1-2: Lecturer's solution code (kept unchanged)
# ---------------------------------------------------------------------------
print("=== PARTS 1-2: Lecturer's examples ===")

# Floating-point comparison
calculated = 0.1 + 0.2
expected = 0.3

print("0.1 + 0.2 =", calculated)
print("Exact comparison:", calculated == expected)
print("Tolerance-based comparison:", np.isclose(calculated, expected))

# Absolute and relative error
true_value = np.sqrt(2)
approx_value = 1.414

absolute_error = abs(true_value - approx_value)
relative_error = absolute_error / abs(true_value)

print(f"Absolute error: {absolute_error:.8f}")
print(f"Relative error: {relative_error:.8%}")

# Numerically unstable vs stable formulation
# Both formulas are mathematically equal:
#   (sqrt(1+x) - 1) / x   =   1 / (sqrt(1+x) + 1)
# but the left one subtracts two nearly equal numbers when x is tiny.
for x in [1e-4, 1e-8, 1e-12]:
    direct = (np.sqrt(1 + x) - 1) / x
    stable = 1 / (np.sqrt(1 + x) + 1)

    print(f"x={x:.0e}: direct={direct:.12f}, stable={stable:.12f}")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) Use better and better approximations of sqrt(2): error should shrink.
print("\n(a) Changing the approximation of sqrt(2):")
print(f"{'Approximation':>14} {'Absolute error':>16} {'Relative error':>16}")
for approx in [1.4, 1.41, 1.414, 1.4142, 1.41421]:
    abs_err = abs(true_value - approx)
    rel_err = abs_err / abs(true_value)
    print(f"{approx:>14} {abs_err:>16.8f} {rel_err:>15.6%}")

# (b) Make x even smaller in the unstable formula: x = 1e-16.
#     Here 1 + x is stored as exactly 1.0, so the direct formula gives 0.
print("\n(b) Making x even smaller:")
for x in [1e-12, 1e-14, 1e-16]:
    direct = (np.sqrt(1 + x) - 1) / x
    stable = 1 / (np.sqrt(1 + x) + 1)
    print(f"x={x:.0e}: direct={direct:.12f}, stable={stable:.12f}")

# (c) Round-off error accumulates when a tiny error is added many times.
print("\n(c) Accumulated round-off (adding 0.1 repeatedly):")
total = 0.0
for _ in range(10):
    total += 0.1
print("Sum of ten 0.1 values =", total, "| equals 1.0?", total == 1.0,
      "| np.isclose:", np.isclose(total, 1.0))
total = 0.0
for _ in range(1_000_000):
    total += 0.1
print("Sum of one million 0.1 values =", total,
      "| exact answer = 100000 | error =", abs(total - 100000))

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - measurement accuracy check
# ---------------------------------------------------------------------------
# Real-world application: Measurement accuracy check
actual_measurement = 2.0
measured_value = 1.998

measurement_error = abs(actual_measurement - measured_value)
measurement_percentage_error = (
    measurement_error / abs(actual_measurement)
) * 100

print("\nMeasurement Accuracy Check")
print("Actual measurement:", actual_measurement)
print("Measured value:", measured_value)
print("Measurement error:", measurement_error)
print(f"Percentage error: {measurement_percentage_error:.2f}%")

if np.isclose(actual_measurement, measured_value, atol=0.005):
    print("Result: Measurement is within the accepted tolerance.")
else:
    print("Result: Measurement is outside the accepted tolerance.")

# Parameter change for Part 4: make the accepted tolerance stricter.
# np.isclose accepts the value when |a - b| <= atol + rtol * |b|
# (rtol is 1e-5 by default).
print("\nChanging the accepted tolerance (atol):")
for atol in (0.005, 0.003, 0.001):
    ok = np.isclose(actual_measurement, measured_value, atol=atol)
    print(f"  atol = {atol}: error 0.002 is "
          f"{'WITHIN' if ok else 'OUTSIDE'} the tolerance")

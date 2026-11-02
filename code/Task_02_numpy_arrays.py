# Task 2: NumPy Arrays and Numerical Computation
#
# Part 1 - the lecturer's small example   (mean of [20, 22, 24, 26])
# Part 2 - the lecturer's weather-station problem (original solution code)
# Part 3 - changing an input and observing the result
# Part 4 - a related real-world case (IoT vaccine-fridge sensor)

import numpy as np

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example from the PDF ===")
small_temperatures = np.array([20, 22, 24, 26])      # input: four readings in C
small_mean = np.mean(small_temperatures)             # (20+22+24+26)/4
print("Temperatures:", small_temperatures)
print("Mean:", small_mean, "C   (hand calculation: (20+22+24+26) / 4 = 92 / 4 = 23)")
assert small_mean == 23.0, "Mean should be 23 C"
print("Self-check passed: mean is 23 C, as in the PDF")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's weather-station problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Weather station - 24 hourly temperatures ===")

# 24 hourly temperature readings in degrees Celsius
temperatures_c = np.array([
    18.5, 18.0, 17.8, 17.5, 17.9, 19.0,
    21.5, 23.8, 25.6, 27.1, 28.3, 29.0,
    29.4, 29.1, 28.5, 27.6, 26.2, 24.8,
    23.4, 22.1, 21.0, 20.2, 19.6, 19.0
])

# Calculate daily temperature statistics
mean_temp = np.mean(temperatures_c)
min_temp = np.min(temperatures_c)
max_temp = np.max(temperatures_c)

# Convert all temperatures from Celsius to Fahrenheit
# (vectorized: one expression converts all 24 values at once)
temperatures_f = 1.8 * temperatures_c + 32

# Display results
print(f"Daily mean temperature: {mean_temp:.2f} C")
print(f"Minimum temperature: {min_temp:.2f} C")
print(f"Maximum temperature: {max_temp:.2f} C")
print("First six Fahrenheit readings:", temperatures_f[:6])

# ---------------------------------------------------------------------------
# PART 3: Parameter change - raise the first reading from 18.5 C to 20.5 C
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter change ===")
changed = temperatures_c.copy()          # copy so the original data is untouched
changed[0] = 20.5                        # the changed input
print(f"First reading changed: 18.5 C -> {changed[0]} C")
print(f"Mean:    {mean_temp:.4f} C -> {np.mean(changed):.4f} C "
      f"(change = {np.mean(changed) - mean_temp:+.4f} C)")
print(f"Minimum: {min_temp:.2f} C -> {np.min(changed):.2f} C")
print(f"Maximum: {max_temp:.2f} C -> {np.max(changed):.2f} C")
# Why +0.0833? The sum rose by 2.0 and there are 24 readings: 2.0 / 24 = 0.0833

# A second change: raise the peak reading (29.4 C) to 35.0 C
changed2 = temperatures_c.copy()
changed2[np.argmax(changed2)] = 35.0
print(f"\nPeak reading changed: 29.4 C -> 35.0 C")
print(f"Maximum: {max_temp:.2f} C -> {np.max(changed2):.2f} C")
print(f"Mean:    {mean_temp:.4f} C -> {np.mean(changed2):.4f} C")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - vaccine-fridge temperature monitoring
# ---------------------------------------------------------------------------
# Assumptions:
#   * A health-centre fridge has an IoT sensor logging one reading per hour.
#   * Vaccines must be stored between 2 C and 8 C.
#   * The readings below are SIMULATED sample data (the fridge door was left
#     slightly open from about hour 12 to hour 17, so the temperature climbed).
print("\n=== PART 4: Vaccine-fridge monitoring (IoT sensor) ===")
LOW_LIMIT_C, HIGH_LIMIT_C = 2.0, 8.0

fridge_c = np.array([
    4.1, 4.0, 3.9, 4.2, 4.1, 4.0,
    4.3, 4.2, 4.1, 4.4, 4.3, 4.5,
    5.2, 7.1, 8.6, 9.3, 7.8, 6.2,
    5.0, 4.6, 4.4, 4.3, 4.2, 4.1
])

# Boolean mask: True where the reading is outside the safe range
unsafe = (fridge_c < LOW_LIMIT_C) | (fridge_c > HIGH_LIMIT_C)
unsafe_hours = np.where(unsafe)[0]       # positions (hours 0-23) that are unsafe

print(f"Mean temperature:    {np.mean(fridge_c):.2f} C")
print(f"Minimum temperature: {np.min(fridge_c):.2f} C")
print(f"Maximum temperature: {np.max(fridge_c):.2f} C")
print(f"Readings outside {LOW_LIMIT_C}-{HIGH_LIMIT_C} C: {unsafe.sum()} of {fridge_c.size}")
print("Unsafe hours (0 = midnight):", unsafe_hours)
print("Unsafe readings in Fahrenheit:", np.round(1.8 * fridge_c[unsafe] + 32, 1))

if unsafe.any():
    print("Result: ALERT - vaccine cold-chain was broken; inspect the vaccines.")
else:
    print("Result: OK - all readings were in the safe range.")

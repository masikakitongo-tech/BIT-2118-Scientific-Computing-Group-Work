# Task 2: NumPy Arrays and Numerical Computation

Program: `code/Task_02_numpy_arrays.py` | Saved output: `results/Task_02_output.txt`

## 1. Objective
To use NumPy arrays to store temperature readings and perform numerical calculations on all of them at once.

## 2. Mathematical concept (in simple words)
An **array** is an organised list of numbers. NumPy lets us apply one operation to every number without writing a loop. For example, if `x = [1, 2, 3]` then `x**2 = [1, 4, 9]`.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | Four temperatures: 20, 22, 24, 26 °C |
| 2 (PDF problem) | 24 hourly weather-station temperatures in °C (from 18.5 °C at midnight to 29.4 °C in the afternoon) |
| 3 (parameter change) | The first reading changed from 18.5 °C to 20.5 °C; then the peak reading changed from 29.4 °C to 35.0 °C |
| 4 (my real-world case) | 24 hourly readings from a vaccine-fridge sensor (simulated) |

## 4. Mathematical operations
- **Mean** (average) = sum of readings ÷ number of readings (`np.mean`).
- **Minimum** and **maximum** (`np.min`, `np.max`).
- **Celsius to Fahrenheit:** F = 1.8 × C + 32, applied to the whole array in one expression (vectorization).
- **Comparison with a limit** (Part 4): a *boolean mask* such as `fridge_c > 8` gives True/False for every reading.

## 5. How the program works
1. `np.array([...])` stores the readings in one array.
2. `np.mean()`, `np.min()` and `np.max()` calculate the daily statistics.
3. `1.8 * temperatures_c + 32` converts every value to Fahrenheit at once.
4. `print(f"...{value:.2f}")` shows the results rounded to 2 decimal places.

## 6. Output and what it means
**Part 1 – PDF example:** the mean of 20, 22, 24, 26 is (20+22+24+26)/4 = 92/4 = **23 °C**. The program confirms this with an `assert` self-check.

**Part 2 – weather station:**
```
Daily mean temperature: 23.12 C
Minimum temperature: 17.50 C
Maximum temperature: 29.40 C
First six Fahrenheit readings: [65.3  64.4  64.04 63.5  64.22 66.2 ]
```
*In words:* the average temperature over the day was about 23.1 °C. The coldest hour was 17.5 °C (early morning) and the hottest was 29.4 °C (afternoon). The first reading, 18.5 °C, equals 65.3 °F.

## 7. Parameter change
| Change | Mean | Minimum | Maximum |
|---|---|---|---|
| Original data | 23.1208 | 17.50 | 29.40 |
| First reading 18.5 → 20.5 °C | **23.2042** | 17.50 | 29.40 |
| Peak reading 29.4 → 35.0 °C | **23.3542** | 17.50 | **35.00** |

*Explanation:* The first change adds 2.0 °C to the total, and 2.0 ÷ 24 readings = 0.0833 °C, so the mean rises from 23.1208 to 23.2042. The minimum and maximum do not change because 20.5 °C is neither the lowest nor the highest value. In the second change the maximum itself changes, so the maximum becomes 35.0 °C and the mean rises by 5.6 ÷ 24 = 0.2333 °C.

> **Correction:** an earlier draft of this document said the new mean was "about 23.21 °C". The program shows it is **23.20 °C** (23.2042).

## 8. Related real-world case: vaccine-fridge monitoring (IoT sensor)
**Assumptions**
- A health-centre fridge has an IoT temperature sensor logging one reading per hour.
- Vaccines must stay between **2 °C and 8 °C**.
- The 24 readings are **simulated sample data**. The door is imagined to be left slightly open from about hour 12 to hour 17, so the temperature climbs.

**Method:** a boolean mask `(fridge_c < 2) | (fridge_c > 8)` marks unsafe readings; `np.where` finds which hours they are.

**Output**
```
Mean temperature:    5.04 C
Minimum temperature: 3.90 C
Maximum temperature: 9.30 C
Readings outside 2.0-8.0 C: 2 of 24
Unsafe hours (0 = midnight): [14 15]
Unsafe readings in Fahrenheit: [47.5 48.7]
Result: ALERT - vaccine cold-chain was broken; inspect the vaccines.
```
**Interpretation:** the average (5.04 °C) looks safe, which is why a mean alone is not enough. Two readings (at 14:00 and 15:00, 8.6 °C and 9.3 °C) were above 8 °C, so the programme raises an alert. This shows how NumPy arrays can monitor sensor data and flag problems automatically.

## 9. Conclusion
NumPy makes it easier to store numerical data and perform calculations on multiple values efficiently. One short expression replaces a loop, and boolean masks make it easy to check sensor data against safe limits.

**Key points to explain to the lecturer**
- An array stores many numbers; NumPy functions work on the whole array.
- Changing one input changes the mean but not necessarily the minimum or maximum.
- The same tools work for any sensor data (temperature, humidity, network traffic).

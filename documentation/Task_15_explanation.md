# Task 15: Numerical Differentiation

Program: `code/Task_15_numerical_differentiation.py` | Saved output: `results/Task_15_output.txt`
Graphs: `results/Task_15_gps_speed.png`, `results/Task_15_step_size_error.png`, `results/Task_15_car_acceleration.png`

## 1. Objective
To estimate how fast a quantity changes (its derivative) from measured values, using forward, central and backward differences, and to understand how the step size affects the error.

## 2. Mathematical concept (in simple words)
A **derivative** measures a rate of change, for example speed is the rate of change of position. When there is no formula, we estimate it from nearby values:
- **Forward difference:** f′(x) ≈ [f(x + h) − f(x)] / h
- **Central difference:** f′(x) ≈ [f(x + h) − f(x − h)] / (2h), usually more accurate for the same h
- **Backward difference:** f′(x) ≈ [f(x) − f(x − h)] / h (used at the last data point)

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | Distance 100 m → 112 m in 2 s; and f(x) = sin x at x = 1 with h from 0.1 down to 10⁻¹² |
| 2 (PDF problem) | GPS times 0–6 s and positions 0.0, 4.8, 10.2, 16.1, 22.7, 30.0, 38.0 m |
| 3 (parameter change) | The position at t = 4 s changed from 22.7 m to 25.0 m |
| 4 (my real-world case) | A car's speed every second for 10 s: 0.0, 2.1, 4.3, 6.2, 8.0, 9.6, 11.0, 12.1, 12.9, 13.4, 13.6 m/s (simulated) |

## 4. Mathematical operations
- Average rate of change: (112 − 100) / 2 = 6 m/s.
- Forward/central/backward differences with step h (here h = 1 s for the GPS data).
- Absolute error against the known exact derivative cos(1) = 0.5403023059.
- `np.gradient`, which applies the same formulas and is used to cross-check the program.

## 5. How the program works
For the GPS data the first point uses a forward difference, interior points use central differences with the neighbours on both sides, and the last point uses a backward difference. In Part 1 the same formulas are tested on sin(x), whose exact derivative we know, to see how the error behaves as h shrinks.

## 6. Output and what it means
**Part 1 – small example:** (112 − 100)/2 = **6 m/s**, as in the PDF.

**Step-size study** (selected rows)
| h | Forward error | Central error |
|---|---|---|
| 10⁻¹ | 4.294×10⁻² | 9.001×10⁻⁴ |
| 10⁻² | 4.216×10⁻³ | 9.005×10⁻⁶ |
| 10⁻³ | 4.208×10⁻⁴ | 9.005×10⁻⁸ |
| 10⁻⁵ | 4.207×10⁻⁶ | 1.114×10⁻¹¹ |
| 10⁻⁸ | 2.970×10⁻⁹ | 2.581×10⁻⁹ |
| 10⁻¹² | 4.324×10⁻⁵ | 1.227×10⁻⁵ |

*In words:* when h gets 10 times smaller, the **forward** error gets about 10 times smaller, but the **central** error gets about 100 times smaller; that is why the central difference is more accurate. However, the error stops improving and then *increases* for very small h (best forward h ≈ 10⁻⁸; best central h ≈ 10⁻⁵). The reason is the floating-point error from Task 4: for tiny h we subtract two almost equal numbers and lose digits. **A smaller step is not always better.**

**Part 2 – GPS speed**
```
t=0s, position=0.0m, estimated speed=4.80m/s
t=1s, position=4.8m, estimated speed=5.10m/s
t=2s, position=10.2m, estimated speed=5.65m/s
t=3s, position=16.1m, estimated speed=6.25m/s
t=4s, position=22.7m, estimated speed=6.95m/s
t=5s, position=30.0m, estimated speed=7.65m/s
t=6s, position=38.0m, estimated speed=8.00m/s
```
*In words:* the vehicle keeps speeding up, from about 4.8 m/s (17 km/h) to 8.0 m/s (29 km/h) over 6 seconds. Example: at t = 3 s, (22.7 − 10.2) / (4 − 2) = 6.25 m/s. The program's answers equal NumPy's `np.gradient`, which confirms the formulas.

## 7. Graphs and interpretation
- **`Task_15_gps_speed.png`:** speed against time rises steadily from 4.8 m/s to 8.0 m/s, so the vehicle keeps speeding up for the whole 6 seconds.
- **`Task_15_step_size_error.png`:** both lines are V-shaped on the log-log graph. On the right (large h) the error falls as h falls (truncation error); the central line is much lower than the forward line. On the left (tiny h) the error rises again (round-off error). The lowest points of the two curves are the best step sizes.
- **`Task_15_car_acceleration.png`:** see section 9.

## 8. Parameter change: one position reading is different
| t (s) | Speed before | Speed after | Change |
|---|---|---|---|
| 2 | 5.65 | 5.65 | 0.00 |
| 3 | 6.25 | 7.40 | **+1.15** |
| 4 | 6.95 | 6.95 | **0.00** |
| 5 | 7.65 | 6.50 | **−1.15** |
| 6 | 8.00 | 8.00 | 0.00 |

*Explanation:* the position at t = 4 s was changed from 22.7 m to 25.0 m. Surprisingly, the speed estimate **at t = 4 s does not change**: the central difference at 4 s uses only the positions at 3 s and 5 s. But the estimates at **3 s and 5 s** change by +1.15 and −1.15 m/s, because they use the position at 4 s. A single wrong GPS value therefore makes the speed jump up and then down (6.25 → 7.40 → 6.95 → 6.50 → 8.00), so differentiation magnifies measurement errors.

## 9. Related real-world case: acceleration of a car
**Assumptions** (simulated)
- A car's speedometer is read every second for 10 s after pulling away from rest (speeds in m/s).
- Acceleration is the rate of change of speed, so the same difference formulas are applied to the speed readings.

**Output**
```
Largest acceleration: 2.15 m/s^2 at t = 1 s
Average acceleration over 10 s: 1.36 m/s^2
Top speed reached: 13.6 m/s = 49.0 km/h
```
Acceleration values fall from 2.1 m/s² at the start to 0.2 m/s² at 10 s.

**Interpretation:** the car accelerates hardest straight after setting off (about 2.1 m/s², roughly a fifth of the acceleration of gravity) and the acceleration steadily fades to almost zero as it approaches its top speed of about 49 km/h. The graph shows the speed curve flattening in the upper panel and the acceleration curve falling in the lower panel, which is the same information shown two ways.

## 10. Conclusion
Numerical differentiation turns measured data into rates of change. Central differences are more accurate than forward differences, the step size must be chosen carefully, and noisy data can make derivatives unreliable.

**Key points to explain to the lecturer**
- Central difference error shrinks like h²; forward difference error like h.
- Too small an h brings back the round-off error from Task 4.
- A wrong measurement affects the neighbouring derivative estimates.

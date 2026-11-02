# Task 13: Interpolation

Program: `code/Task_13_interpolation.py` | Saved output: `results/Task_13_output.txt`
Graphs: `results/Task_13_temperature_interpolation.png`, `results/Task_13_sensor_calibration.png`

## 1. Objective
To estimate values *between* measured data points using linear interpolation and cubic splines.

## 2. Mathematical concept (in simple words)
**Interpolation** fills in values between known data points.
- **Linear interpolation** joins neighbouring points with straight lines.
- **Cubic spline** joins them with smooth cubic curves so that the curve has no sharp corners.

Both methods pass exactly through every measured point. They should only be used *inside* the range of the data.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | 20 °C at 10:00 and 24 °C at 12:00 |
| 2 (PDF problem) | Temperatures 18.0, 20.0, 22.5, 24.0, 25.0, 25.5, 25.0 °C at 8:00 … 14:00 |
| 3 (parameter changes) | The 11:00 reading changed from 24.0 to 26.0 °C; a request for 15:00 |
| 4 (my real-world case) | A sensor calibration table: voltages 0.5–3.0 V and temperatures 0, 25, 48, 68, 85, 100 °C (simulated); new readings 0.75, 1.80, 2.70, 2.95 V |

## 4. Mathematical operations
- Linear interpolation: y = y₁ + (y₂ − y₁) · (x − x₁) / (x₂ − x₁).
- `interp1d(x, y, kind="linear")` and `CubicSpline(x, y)` from `scipy.interpolate`.
- Evaluating the fitted functions at new points (every 10 minutes = 1/6 hour).

## 5. How the program works
The hourly data are given to `interp1d` and `CubicSpline`, which each return a *function*. Calling that function with new times returns estimated temperatures. The program checks that both functions return the original measurements at the measured hours.

## 6. Output and what it means
**Part 1:** the temperature at 11:00 is 20 + (24 − 20) × (11 − 10)/(12 − 10) = **22 °C**, as in the PDF.

**Part 2 – hourly temperatures**
```
Linear estimate at 10:30: 23.25 C
Cubic estimate at 10:30:  23.36 C
Number of 10-minute times: 37
```
*In words:* the temperature at 10:30 is estimated to be about **23.3 °C**. The linear estimate is exactly the average of 22.5 (10:00) and 24.0 (11:00) = 23.25. The cubic spline is slightly higher (23.36) because it follows the smooth shape of the whole curve. There are 37 estimates, one every 10 minutes from 8:00 to 14:00.

> **Floating-point note (link to Task 4):** `np.arange(8, 14 + 1/6, 1/6)` ends at 13.999999999999979, not exactly 14, because 1/6 cannot be stored exactly. It happens to stay *inside* the data range, so the PDF code works. If the last value had been slightly above 14, `interp1d` would have raised an error. In my own checks I use `np.linspace(8, 14, 601)`, which ends exactly at 14.

## 7. Graph and interpretation
**`Task_13_temperature_interpolation.png`:** the dots are the seven hourly measurements. The blue straight-line version has visible corners at each measurement (for example at 13:00); the orange cubic spline is a smooth curve through the same dots. The temperature rises quickly in the morning and levels off at about 25.5 °C around 13:00. The spline shows this gentle peak (just after 13:00) more naturally than the line segments, and the two curves are almost on top of each other everywhere else.

## 8. Parameter change
**(a) The 11:00 reading changes from 24.0 to 26.0 °C**
| Method | 10:30 before | 10:30 after | 12:30 before | 12:30 after |
|---|---|---|---|---|
| Linear | 23.25 | 24.25 | 25.25 | 25.25 |
| Cubic | 23.36 | 24.58 | 25.34 | 25.02 |

*Explanation:* both methods raise the 10:30 estimate, because 10:30 lies between 10:00 and the changed 11:00 point. The important difference is at **12:30**: the linear estimate does not change (it only uses the 12:00 and 13:00 readings), but the cubic spline *does* change, because a spline is calculated from all the data together. Linear interpolation is local; cubic splines are global.

**(b) Where do the two methods differ most?** The largest gap is only 0.194 °C (at about 8:27), so for this smooth data both methods are very close.

**(c) Asking for 15:00, after the last reading at 14:00:** `interp1d` refuses (*"A value (15.0) in x_new is above the interpolation range's maximum value (14.0)"*). `CubicSpline` silently extrapolates and gives 22.94 °C, which is a guess outside the data and should not be trusted.

## 9. Related real-world case: calibrating a temperature sensor
**Assumptions** (simulated)
- A sensor outputs a voltage, and the manufacturer's table gives the true temperature at six voltages.
- The relationship is smooth but not a straight line (the temperature rises more slowly at higher voltages).
- In use, the sensor produces voltages that are not in the table, so the temperature must be interpolated.

**Output**
| Voltage (V) | Linear (°C) | Cubic (°C) | Difference |
|---|---|---|---|
| 0.75 | 12.50 | 12.67 | 0.17 |
| 1.80 | 60.00 | 60.38 | 0.38 |
| 2.70 | 91.00 | 91.17 | 0.17 |
| 2.95 | 98.50 | 98.56 | 0.06 |

**Interpretation:** a reading of 1.80 V corresponds to about **60.4 °C**. The two methods differ by less than 0.4 °C. Because the true curve bends, the cubic spline (which follows the bend) is likely to be a bit closer to the truth than the straight-line segments, which cut across the bend. The graph shows the black table points, the two curves (almost on top of each other) and the red new readings sitting on the cubic curve. This is how real sensors, lookup tables and engineering charts are used.

## 10. Conclusion
Interpolation estimates values between measurements. Linear interpolation is simple and local; cubic splines give smooth curves. Never use either far outside the measured range.

**Key points to explain to the lecturer**
- Both curves pass through every measured point.
- Interpolation (inside the data) is reliable; extrapolation (outside) is not.
- Cubic splines are smoother, but changing one point can change estimates elsewhere.

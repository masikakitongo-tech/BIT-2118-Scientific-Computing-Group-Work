# Task 16: Numerical Integration

Program: `code/Task_16_numerical_integration.py` | Saved output: `results/Task_16_output.txt` | Graph: `results/Task_16_energy_area.png`

## 1. Objective
To calculate accumulated quantities (such as total energy or total distance) from measured data by integrating numerically with the trapezoidal rule and Simpson's rule.

## 2. Mathematical concept (in simple words)
An **integral** is the accumulated quantity, or the **area under a curve**.
- **Trapezoidal rule:** join the data points with straight lines and add up the areas of the trapezoids.
- **Simpson's rule:** fit small parabolas through groups of three points; it is usually more accurate for smooth data.
- **Adaptive quadrature** (`scipy.integrate.quad`) automatically uses more points where the function needs them.

Example: power P in kW multiplied by time in hours gives energy in kWh, so constant 2 kW for 3 h is 2 × 3 = 6 kWh.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | Constant 2 kW at 0, 1, 2, 3 h; and sin x from 0 to π (exact integral 2) with 5, 9, 17, 33 samples |
| 2 (PDF problem) | Meter readings every 2 h from 0 to 12 h: 0.8, 1.0, 1.4, 1.8, 1.6, 1.2, 0.9 kW |
| 3 (parameter changes) | The reading at 6 h changed from 1.8 to 2.4 kW; only the readings at 0, 4, 8, 12 h used |
| 4 (my real-world case) | A delivery rider's speed every minute for 10 min: 0, 12, 25, 30, 28, 32, 35, 30, 22, 10, 0 km/h (simulated) |

## 4. Mathematical operations
- Trapezoid area for one interval = (y₁ + y₂)/2 × width, summed (`np.trapezoid`).
- Simpson's rule (`scipy.integrate.simpson`) and adaptive quadrature (`quad`).
- Unit conversion (minutes → hours) so that km/h × h = km.

## 5. How the program works
Each rule takes the list of times and the list of measurements and returns the total area. For the smart-meter data the answer is in kWh because the power is in kW and the time is in hours.

## 6. Output and what it means
**Part 1:** 2 kW for 3 h gives **6.0 kWh**, as in the PDF.

**Accuracy of the rules on sin x (exact answer 2)**
| Samples | Trapezoid error | Simpson error |
|---|---|---|
| 5 | 1.04×10⁻¹ | 4.56×10⁻³ |
| 9 | 2.58×10⁻² | 2.69×10⁻⁴ |
| 17 | 6.43×10⁻³ | 1.66×10⁻⁵ |
| 33 | 1.61×10⁻³ | 1.03×10⁻⁶ |

*In words:* doubling the number of intervals makes the trapezoid error about 4 times smaller but the Simpson error about 16 times smaller. SciPy's adaptive `quad` reaches 2.000000000000 with an estimated error of 2×10⁻¹⁴.

**Part 2 – smart meter**
```
Energy using trapezoidal rule: 15.700 kWh
Energy using Simpson's rule:   15.800 kWh
Difference between estimates:  0.100 kWh
```
*In words:* the household used about **15.7 to 15.8 kWh** in 12 hours. Hand check with the trapezoids (each interval is 2 h wide): 1.8 + 2.4 + 3.2 + 3.4 + 2.8 + 2.1 = 15.7 kWh. The two rules differ by only 0.1 kWh (about 0.6%).

## 7. Graph and interpretation
**`Task_16_energy_area.png`:** the line shows the power readings and the shaded region underneath is the energy. Power rises from 0.8 kW at the start to a peak of 1.8 kW after 6 hours and then falls to 0.9 kW after 12 hours. The bigger the shaded area, the more energy is used, so the total energy is simply the size of that area.

## 8. Parameter change
| Change | Trapezoid (kWh) | Simpson (kWh) |
|---|---|---|
| Original readings | 15.700 | 15.800 |
| (a) Reading at 6 h: 1.8 → 2.4 kW | **16.900** | **17.400** |
| (b) Only readings at 0, 4, 8, 12 h | **15.400** | **15.967** |

*Explanation:* (a) a higher reading in the middle raises the energy by 1.2 kWh (trapezoid) or 1.6 kWh (Simpson): Simpson gives the middle reading more weight. (b) Using half the readings loses detail and moves the estimate by 0.3 kWh (trapezoid) or 0.17 kWh (Simpson), so more frequent readings give a more reliable answer.

## 9. Related real-world case: distance travelled by a delivery rider
**Assumptions** (simulated)
- Speed (km/h) is recorded every minute for 10 min.
- Distance = integral of speed over time. Because speed is in km per **hour**, the time must be converted to hours (minutes ÷ 60).

**Output**
```
Distance (trapezoidal rule): 3.733 km
Distance (Simpson's rule):   3.756 km
Average speed over the trip: 22.4 km/h
Top speed recorded:          35 km/h
Wrong shortcut (mean of readings x 10 min): 3.394 km
```
**Interpretation:** the rider travelled about **3.7 km** at an average speed of 22.4 km/h, with a top speed of 35 km/h. The two rules agree to within 0.03 km. The simple shortcut "average of the readings × time" gives 3.39 km, which is about 9% too low, because the two zero readings at the start and end are counted as if they lasted a whole interval. Integrating properly handles that.

## 10. Conclusion
Numerical integration adds up many small contributions. Simpson's rule is more accurate for smooth data, and more frequent readings improve both methods.

**Key points to explain to the lecturer**
- The integral of power over time is energy; of speed over time is distance.
- Simpson's rule improves much faster than the trapezoidal rule when more samples are used.
- Check the units (hours versus minutes) before integrating.

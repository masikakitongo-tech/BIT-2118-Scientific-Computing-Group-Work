# Task 14: Curve Fitting and Approximation

Program: `code/Task_14_curve_fitting.py` | Saved output: `results/Task_14_output.txt`
Graphs: `results/Task_14_response_time_fit.png`, `results/Task_14_residuals.png`, `results/Task_14_user_growth.png`

## 1. Objective
To choose a mathematical model and find the parameter values that make it follow measured data as closely as possible (least squares).

## 2. Mathematical concept (in simple words)
**Curve fitting** picks the parameters of a formula (for example a, b, c in y = ax² + bx + c) so that the curve passes as close as possible to the data points. In **least squares**, "as close as possible" means making the sum of the squared residuals Σ(yᵢ − ŷᵢ)² as small as possible, where a *residual* is the gap between a measured value yᵢ and the model's prediction ŷᵢ. Unlike interpolation, a fitted curve does not have to pass through every point; it describes the overall trend.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF idea) | Five points x = 1…5 and y = 2.1, 3.9, 6.2, 7.8, 10.1 (roughly y = 2x) |
| 2 (PDF problem) | Users 50, 100, …, 350 and response times 82, 95, 115, 145, 185, 238, 305 ms; quadratic model |
| 3 (parameter changes) | Polynomial degree 1, 2, 3; the 350-user measurement changed from 305 to 340 ms |
| 4 (my real-world case) | App users (thousands) at months 1–8: 120, 150, 195, 250, 320, 410, 530, 680; exponential model |

## 4. Mathematical operations
- `np.polyfit` (least-squares polynomials) and `scipy.optimize.curve_fit` (any model function).
- Predictions ŷ, residuals y − ŷ, and **RMSE** = √(mean of squared residuals), the typical size of an error.
- For the exponential model: growth per month = e^B − 1, doubling time = ln 2 / B.

## 5. How the program works
`curve_fit(model, x, y)` tries different parameter values until the squared residuals are smallest and returns them. The program then predicts the response at 400 users, plots the data with the fitted curve, and plots the residuals.

## 6. Output and what it means
**Part 1 – a straight line:** the least-squares line is **y = 0.0500 + 1.9900x**. Its sum of squared residuals is 0.1070; the "obvious" line y = 2x gives 0.1100 and a poorer guess y = 0.5 + 1.8x gives 0.5400. The fitted line has the smallest sum, which is what "least squares" means.

**Part 2 – server response time**
```
Fitted model: y = 0.002167x^2 + -0.1345x + 85.00
RMSE: 1.55 ms
Predicted response at 400 users: 377.86 ms
Residuals (measured - predicted) in ms: [-1.69  1.79  1.43  0.24 -1.79 -1.64  1.67]
```
*In words:* response time grows faster and faster as more users connect. The model is typically about **1.5 ms** away from the measurements, which is small compared with response times of 82–305 ms. The model predicts about **378 ms at 400 users**, but this is a forecast beyond the measured range (50–350), so it is less certain than the fit itself.

## 7. Graph and interpretation
- **`Task_14_response_time_fit.png`:** the dots are the measurements and the curve is the quadratic fit; the curve passes very close to every dot and bends upwards, showing that the delay increases faster at high load.
- **`Task_14_residuals.png`:** the residuals are all within ±1.8 ms. They go − + + + − − +, a wave-like pattern rather than pure randomness, which suggests that the quadratic model leaves a very small amount of structure unexplained (see the cubic row below).
- **`Task_14_user_growth.png`:** see section 9.

## 8. Parameter change
**(a) Model complexity**
| Polynomial degree | RMSE (ms) | Prediction at 400 users (ms) |
|---|---|---|
| 1 (line) | 18.83 | 312.86 |
| 2 (quadratic, PDF) | 1.55 | 377.86 |
| 3 (cubic) | 0.14 | 387.86 |

*Explanation:* a straight line is clearly a poor model (error about 19 ms). The quadratic reduces the error a lot, and the cubic reduces it further. But a higher degree is not automatically better: with only 7 measurements, a cubic has 4 free parameters and could be fitting noise (*overfitting*). Note that the 400-user forecast moves from 378 to 388 ms depending on the model, which is an honest measure of the uncertainty.

**(b) One measurement changed (350 users: 305 → 340 ms)**
| | Fitted model | Prediction at 400 users |
|---|---|---|
| Before | y = 0.002167x² − 0.1345x + 85.00 | 377.86 ms |
| After | y = 0.003000x² − 0.3929x + 100.00 | 422.86 ms |

*Explanation:* one higher measurement at the end of the data pulls the whole curve upwards and makes it steeper, so the forecast at 400 users rises by about 45 ms. The last points have a lot of influence on predictions.

## 9. Related real-world case: growth of a mobile app's users
**Assumptions** (simulated)
- Active users (in thousands) at the end of months 1–8 are given above.
- Growth looks exponential, users(t) = A·e^(B·t): each month the user base grows by about the same percentage.
- We fit A and B, compare with a straight line, and forecast month 10.

**Output**
```
Fitted model: users = 91.68 * exp(0.2504 * month)
Monthly growth rate: 28.5%
Doubling time: 2.77 months
RMSE exponential model: 1.23 thousand users
RMSE straight-line model: 44.57 thousand users
Forecast for month 10: exponential = 1122 thousand, straight line = 760 thousand
```
**Interpretation:** the user base grows by about **28.5% every month** and doubles roughly every **2.8 months**. The exponential curve fits the data with an error of about 1,200 users, while a straight line is off by about 44,600, so the exponential model is the right choice. The graph shows the straight line cutting across the points while the exponential curve follows them. Choosing the wrong model gives very different forecasts for month 10 (1,122,000 against 760,000 users). In practice, growth cannot stay exponential forever, so such a forecast is only reliable over a short horizon.

## 10. Conclusion
Curve fitting finds the parameters of a chosen model by minimising squared residuals. The RMSE and the residual plot show how good the fit is, and choosing a suitable model matters more than choosing a complicated one.

**Key points to explain to the lecturer**
- A fitted curve follows the trend; it does not have to touch every point.
- Residuals and RMSE measure the quality of the fit.
- Forecasting outside the data range is risky, and an over-complicated model can overfit.

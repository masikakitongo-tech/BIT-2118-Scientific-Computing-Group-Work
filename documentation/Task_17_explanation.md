# Task 17: Ordinary Differential Equations – Euler Method

Program: `code/Task_17_euler_ode.py` | Saved output: `results/Task_17_output.txt`
Graphs: `results/Task_17_cooling.png`, `results/Task_17_step_sizes.png`, `results/Task_17_logistic_growth.png`

## 1. Objective
To solve a differential equation step by step with Euler's method and to see how the step size affects accuracy.

## 2. Mathematical concept (in simple words)
An **ordinary differential equation (ODE)** describes *how fast* a quantity changes, for example dy/dt = f(t, y). **Euler's method** starts from a known value y₀ and repeatedly walks forward along the slope:

**yₙ₊₁ = yₙ + h · f(tₙ, yₙ)**

where h is the **step size**. A smaller h usually gives a better answer but needs more steps.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | dy/dt = y, y(0) = 1, h = 0.1 |
| 2 (PDF problem) | Newton's law of cooling dT/dt = −k(T − T_ambient): T_ambient = 25 °C, T(0) = 90 °C, k = 0.12 per minute, h = 1 min, 30 min |
| 3 (parameter changes) | Step sizes h = 5, 2, 1, 0.5, 0.1 min; k = 0.06, 0.12, 0.30; a huge k = 2.5 |
| 4 (my real-world case) | Logistic growth of bacteria: dP/dt = r·P·(1 − P/K) with r = 0.4 per day, K = 1000 (hundred), P(0) = 10, steps h = 2 and 0.5 days (simulated) |

## 4. Mathematical operations
- Euler update T_new = T + h · (−k (T − T_ambient)).
- The exact solution T(t) = T_ambient + (T₀ − T_ambient)·e^(−kt) is used only to measure the error.
- Absolute error = |Euler − exact|.

## 5. How the program works
A loop applies the Euler update once per time step and stores each temperature in an array. The exact curve is computed from its formula for comparison.

## 6. Output and what it means
**Part 1 – dy/dt = y:** y₁ = 1.1000, y₂ = 1.2100, y₃ = 1.3310 (the PDF's 1.1 and 1.21). After 10 steps y(1) ≈ **2.5937**, while the exact answer is e = 2.7183, so the Euler error is 0.1245. *In words:* Euler under-estimates because the quantity grows faster and faster, but each step uses the slope from the beginning of the step.

**Part 2 – cooling**
```
Euler temperature after 30 min: 26.40 C
Exact temperature after 30 min: 26.78 C
Final absolute error: 0.3720 C
```
*In words:* the hot object (90 °C) cools towards the room temperature of 25 °C; after 30 minutes it is at about 26.4 °C according to Euler, against 26.78 °C exactly. An error of 0.37 °C is small. This is the model of a cup of tea or a hot engine cooling down.

## 7. Graph and interpretation
**`Task_17_cooling.png`:** both curves fall steeply at first and flatten as the object approaches 25 °C (the hotter the object, the faster it cools). The Euler dots lie slightly below the exact curve. **`Task_17_step_sizes.png`:** the curves for large step sizes (h = 5, h = 2) are clearly below the exact dashed curve; as h decreases to 0.5 and 0.1 the Euler curve moves on top of the exact one.

## 8. Parameter change
**(a) Step size h (k = 0.12)**
| h (min) | Steps | Euler at 30 min | Exact | Error |
|---|---|---|---|---|
| 5.0 | 6 | 25.266 | 26.776 | 1.510 |
| 2.0 | 15 | 26.060 | 26.776 | 0.717 |
| 1.0 | 30 | 26.404 | 26.776 | 0.372 |
| 0.5 | 60 | 26.587 | 26.776 | 0.189 |
| 0.1 | 300 | 26.738 | 26.776 | 0.038 |

*Explanation:* **halving h roughly halves the error** (0.372 → 0.189), and using h = 0.1 reduces it to 0.038. This is typical of Euler's method: more accuracy needs more steps (300 instead of 30).

**(b) Cooling constant k (h = 1):** k = 0.06 gives 35.16 °C (exact 35.74), k = 0.12 gives 26.40 °C (exact 26.78) and k = 0.30 gives 25.00 °C (exact 25.01). A larger k means faster cooling, so the object is closer to room temperature after 30 minutes.

**(c) Instability:** with a huge k = 2.5 and h = 1 the Euler values are `90, −72.5, 171.2, −194.4, 354.1, −468.6, …`. The temperature swings wildly above and below 25 °C although the true answer falls smoothly. When k·h is too large (here k·h = 2.5 > 2), Euler's method becomes **unstable**, so the step must be small enough.

## 9. Related real-world case: logistic growth of a bacteria colony
**Assumptions** (simulated)
- 10 hundred bacteria at the start, growth rate r = 0.4 per day, and the dish can support K = 1000 hundred.
- dP/dt = r·P·(1 − P/K): growth is fast at first and slows as the dish fills.
- The exact solution P(t) = K / (1 + ((K − P₀)/P₀)·e^(−rt)) is used for checking.

**Output** (hundreds of bacteria)
| Day | Exact | Euler h = 2 | Euler h = 0.5 |
|---|---|---|---|
| 0 | 10.0 | 10.0 | 10.0 |
| 10 | 355.5 | 171.4 | 290.6 |
| 20 | 967.9 | 942.3 | 964.0 |
| 30 | 999.4 | 1000.0 | 999.6 |

Largest error: 284.0 (h = 2) and 79.1 (h = 0.5); the colony reaches half its capacity after 11.5 days.

**Interpretation:** the colony grows slowly at first, then explosively around day 10–15, then levels off at the 100,000-bacteria limit. With the coarse step (h = 2 days), Euler is badly late at day 10 (171 instead of 356, an error of about 18,000 bacteria), although all versions agree by day 30. The finer step is much better in the fast-growth period, where accuracy matters most.

## 10. Conclusion
Euler's method solves ODEs with a very simple update rule. Accuracy improves as the step size is reduced, but too large a step gives large errors or even instability.

**Key points to explain to the lecturer**
- New value = old value + step size × rate of change.
- Halving h roughly halves the Euler error (first-order accuracy).
- Always compare with an exact solution, or with a smaller h, to see whether the step size is acceptable.

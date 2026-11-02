# Task 12: Polynomial and Nonlinear Equation Solving

Program: `code/Task_12_nonlinear_equations.py` | Saved output: `results/Task_12_output.txt`

## 1. Objective
To solve a polynomial equation and a *system* of two nonlinear equations using `numpy.roots` and `scipy.optimize.root`.

## 2. Mathematical concept (in simple words)
- A **polynomial equation** has the form aₙxⁿ + … + a₁x + a₀ = 0. For example x² − 5x + 6 = (x − 2)(x − 3) = 0 has roots 2 and 3.
- A **nonlinear system** contains equations that are not all straight lines, for example a circle and a parabola. A numerical solver starts from a guess and adjusts it until every equation's **residual** (how far the equation is from being true) is close to zero.
- Different starting guesses can lead to different answers, or to none.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | x² − 5x + 6 = 0, coefficients [1, −5, 6] |
| 2 (PDF problem) | Circle x² + y² = 4 and parabola y = x² − 1; starting guesses (1, 1) and (−1, 1) |
| 3 (parameter changes) | Circle radius² changed from 4 to 9; four starting guesses (±1, ±1) |
| 4 (my real-world case) | Radar zone x² + y² = 100 (radius 10 km) and a ship's route y = 0.1x² − 3 |

## 4. Mathematical operations
- `np.roots(coefficients)` finds all roots of a polynomial; `np.polyval` substitutes them back.
- `root(equations, guess)` solves several equations together.
- Residuals: the left side minus the right side of each equation.
- Checking `success` and the residual size before trusting an answer.

## 5. How the program works
Each equation is rewritten so that "= 0" is on the right: circle `x**2 + y**2 - 4`, parabola `y - (x**2 - 1)`. The solver searches for (x, y) that makes both expressions 0. By hand, x² = y + 1, so y² + y − 3 = 0, which gives y = (−1 + √13)/2 = 1.3028 and x = ±1.5175, a quick way to confirm the solver.

## 6. Output and what it means
**Part 1:** the roots are `[2. 3.]`. Substituting them back gives about 10⁻¹⁶ (round-off), so both are roots, exactly as in the PDF.

**Part 2 – circle and parabola**
```
Initial guess: [1.0, 1.0]   Intersection: [1.51748991 1.30277564]   Converged: True
Initial guess: [-1.0, 1.0]  Intersection: [-1.51748991 1.30277564]  Converged: True
Residuals: about -2.5e-13 for both equations
Exact answer by algebra: x = +/-1.517490, y = 1.302776
```
*In words:* the curves cross at two points, **(1.517, 1.303)** and **(−1.517, 1.303)**, mirror images of each other because both curves are symmetric about the y-axis. The residuals are about 10⁻¹³, so both equations are satisfied. The two different starting guesses led to the two different intersections.

## 7. Parameter change
**(a) Different starting guesses (circle radius² = 4)**
| Guess | Result | Converged? |
|---|---|---|
| (1, 1) | (1.5175, 1.3028) | Yes |
| (−1, 1) | (−1.5175, 1.3028) | Yes |
| (1, −1) | (≈0, −1.9385) | **No** |
| (−1, −1) | (≈0, −1.9385) | **No** |

*Explanation:* the algebra gives a second value y = (−1 − √13)/2 = −2.30, but then x² = y + 1 would be negative, so it is not a real point. Guesses in the lower half therefore cannot reach any real intersection, and the solver stops at a spot where the equations are *not* satisfied and reports `success = False`. **Always check `success` and the residuals.**

**(b) A bigger circle (radius² = 9):** the intersections move outwards to (±1.8364, 2.3723), matching the algebra y² + y − 8 = 0. A larger circle meets the parabola higher up and further out.

## 8. Related real-world case: a ship crossing a radar zone
**Assumptions** (simulated)
- A coastal radar at (0, 0) detects objects within 10 km: x² + y² = 100.
- A ship follows the curved route y = 0.1x² − 3 (x and y in km).
- Question: where does the ship enter and leave the radar zone?

**Output**
```
Distinct crossing points found: 2
  (-8.802 km, 4.747 km)  distance from radar = 10.000 km
  (8.802 km, 4.747 km)   distance from radar = 10.000 km
At x = 0 the ship is only 3.0 km from the radar (closest approach)
```
**Interpretation:** the ship **enters the radar zone at about (−8.80, 4.75) km and leaves at (8.80, 4.75) km**, and it is detectable all the time in between. Its closest point to the radar is 3 km, at the bottom of its curve. The algebra confirms the answer. A third starting guess (0, −9) did not converge, and the program discards it automatically because its residuals are not close to zero (−0.34 and −6.98).

## 9. Conclusion
`np.roots` solves polynomials directly, and `scipy.optimize.root` solves nonlinear systems from a starting guess. Different guesses can find different solutions, and checking the residuals shows whether an answer is genuine.

**Key points to explain to the lecturer**
- Rewrite every equation as "expression = 0" so that the residual is simple to read.
- Try several starting guesses to find all the solutions.
- A solution is only valid when `success` is True and the residuals are almost zero.

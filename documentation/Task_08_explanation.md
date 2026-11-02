# Task 8: Iterative Methods for Linear Systems

Program: `code/Task_08_iterative_linear.py` | Saved output: `results/Task_08_output.txt`
Graphs: `results/Task_08_convergence.png`, `results/Task_08_plate_temperature.png`

## 1. Objective
To solve a linear system by repeated improvement of a guess (Jacobi and Gauss–Seidel methods), and to see how quickly the error shrinks.

## 2. Mathematical concept (in simple words)
Instead of solving Ax = b in one go, an **iterative method** starts with a guess and improves it again and again.
- **Jacobi:** solve each equation for one unknown using the *old* values of all the others.
- **Gauss–Seidel:** the same, but use the *newest* values as soon as they are available, which usually converges faster.

We stop when the biggest change between two successive estimates is smaller than a chosen **tolerance**. These methods are attractive for *large sparse* systems (matrices that are mostly zeros), for example heat-transfer models with thousands of equations.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF idea) | 4x − y = 6 and −x + 3y = 4 (exact answer x = y = 2), starting from (0, 0) |
| 2 (PDF problem) | A 5 × 5 matrix with 2 on the diagonal and −1 beside it; b = [100, 0, 0, 0, 20] (left boundary 100 °C, right boundary 20 °C); tolerance 10⁻⁸ |
| 3 (parameter changes) | Tolerances 10⁻², 10⁻⁴, 10⁻⁸; right boundary changed from 20 °C to 60 °C |
| 4 (my real-world case) | A heated square plate, 5 × 5 interior grid = 25 unknowns; top edge 100 °C, other edges 0 °C |

## 4. Mathematical operations
- Jacobi update: x_new = (b − R·x) / D, where D is the diagonal of A and R = A − D.
- Gauss–Seidel update: each x[i] uses the already-updated x[0..i−1] and the old x[i+1..].
- Error measure: the largest absolute change between iterations (`np.linalg.norm(..., ord=np.inf)`).
- Comparison with the direct solution `np.linalg.solve`.

## 5. How the program works
Both functions return the final answer and a list of the error at every iteration, so the number of iterations is `len(errors)`. The error list is drawn on a log scale to show convergence.

## 6. Output and what it means
**Part 1 – small example** (estimates for x): 1.5, 1.8333, 1.9583, 1.9861, 1.9965, 1.9988, 1.9997, 1.9999 → the values move steadily towards 2, as in the PDF's description of convergence.

**Part 2 – five temperatures**
```
Jacobi temperatures:       [86.66666665 73.33333331 59.99999997 46.66666664 33.33333332]
Gauss-Seidel temperatures: [86.66666665 73.3333333  59.99999997 46.66666665 33.33333332]
Direct solution:           [86.66666667 73.33333333 60.         46.66666667 33.33333333]
Iterations needed: Jacobi = 150 | Gauss-Seidel = 75
```
*In words:* the temperature falls in a straight line from 100 °C at the left to 20 °C at the right (86.7, 73.3, 60, 46.7, 33.3 °C). Both iterative methods agree with the direct solution to about 8 decimal places, but **Gauss–Seidel needed only half as many iterations** (75 instead of 150).

## 7. Graph and interpretation
**`Task_08_convergence.png`** – the error against iteration number on a logarithmic axis. Both lines go down as straight lines, which means the error is reduced by the same factor at every iteration. The Gauss–Seidel line is steeper, so it reaches the 10⁻⁸ tolerance in about half the iterations of Jacobi. Both methods converge because the matrix is diagonally dominant.

**`Task_08_plate_temperature.png`** – a heat map of the plate (see section 9).

## 8. Parameter change
**(a) Tolerance**
| Tolerance | Jacobi iterations | Gauss–Seidel iterations |
|---|---|---|
| 10⁻² | 54 | 27 |
| 10⁻⁴ | 86 | 43 |
| 10⁻⁸ | 150 | 75 |

*Explanation:* a stricter tolerance means more iterations, and each extra decimal place of accuracy costs a roughly constant number of extra iterations. Gauss–Seidel needs about half as many as Jacobi in every row.

**(b) Right boundary 20 °C → 60 °C**
```
before: [86.667 73.333 60.    46.667 33.333]
after:  [93.333 86.667 80.    73.333 66.667]
```
*Explanation:* the heat source on the right is hotter, so every interior point warms up. The temperatures still form a straight line, now from 100 °C to 60 °C.

## 9. Related real-world case: heat spreading across a metal plate
**Assumptions**
- A thin square plate has a 5 × 5 grid of interior points (25 unknown temperatures).
- The top edge is held at 100 °C by a heater and the other three edges at 0 °C.
- In steady state, each point equals the average of its four neighbours: 4·T − T(up) − T(down) − T(left) − T(right) = 0.

**Output**
```
Unknowns: 25 | non-zero coefficients: 105 of 625 (16.8%)
Iterations needed: Jacobi = 140 | Gauss-Seidel = 73
Largest difference from direct solution (Gauss-Seidel): 2.39e-08
Temperature grid (top row first):
[[46.87 62.92 66.94 62.92 46.87]
 [24.55 37.88 41.93 37.88 24.55]
 [13.46 22.12 25.   22.12 13.46]
 [ 7.18 12.12 13.84 12.12  7.18]
 [ 3.13  5.35  6.13  5.35  3.13]]
```
**Interpretation (heat-map graph):** the plate is hottest next to the heater and cools quickly towards the bottom. The top-middle point is only about 67 °C (not 100 °C) because the cold side edges pull heat away; the corners are cooler than the middle. The picture is symmetric left to right, as it should be. Only 16.8% of the matrix entries are non-zero. For a real plate with, say, 100 × 100 grid points there would be 10,000 equations and well under 1% non-zero entries, which is exactly the situation in which iterative methods are preferred.

## 10. Conclusion
Jacobi and Gauss–Seidel solve linear systems by repeated improvement. Gauss–Seidel converged about twice as fast in every test, and a tolerance controls the accuracy.

**Key points to explain to the lecturer**
- Start with a guess, improve it, stop when the change is below the tolerance.
- Gauss–Seidel uses new values immediately, so it converges faster.
- These methods work well when the matrix is diagonally dominant and mostly zeros.

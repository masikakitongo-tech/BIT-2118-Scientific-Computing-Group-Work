# Task 7: Gaussian Elimination and LU Decomposition

Program: `code/Task_07_gaussian_lu.py` | Saved output: `results/Task_07_output.txt`

## 1. Objective
To understand how a linear system is solved step by step (Gaussian elimination) and how LU decomposition lets us reuse the same work when only the right-hand side changes.

## 2. Mathematical concept (in simple words)
- **Gaussian elimination** removes unknowns one row at a time until the system becomes *upper triangular* (all numbers below the diagonal are zero). The last equation then gives one unknown, and **back-substitution** works upwards to find the rest.
- **LU decomposition** writes A as a product A = LU (with row swapping called *pivoting*, PA = LU), where L is lower triangular and U is upper triangular. Once A is factored, each new b can be solved quickly.

## 3. Input values
| Part | Input |
|---|---|
| 1–2 (PDF) | A = [[4, −1, 0], [−1, 4, −1], [0, −1, 3]] and three measurement vectors b = [15, 10, 10], [16, 11, 9], [14, 12, 11] |
| 3 (parameter changes) | b doubled; A[0,0] changed from 4 to 6; a 400 × 400 system with 200 different b vectors |
| 4 (my real-world case) | A three-sector economy (Agriculture, Manufacturing, Services), a consumption matrix C and final demand for three years (simulated) |

## 4. Mathematical operations
- Row operations: row i = row i − factor × pivot row (forward elimination), then back-substitution.
- `lu_factor(A)` factors the matrix once; `lu_solve((lu, piv), b)` solves for each b.
- Residual b − Ax to check each answer.
- `timeit` to compare solving from scratch every time against factoring once.

## 5. How the program works
1. A function `gaussian_elimination()` does elimination and back-substitution by hand, so every step can be seen.
2. The PDF's code factors A once with `lu_factor` and solves the three measurement vectors with `lu_solve`.
3. Part 3 changes inputs and times the two approaches.
4. Part 4 solves an economic model for three years using one factorisation.

## 6. Output and what it means
**Part 1 – Gaussian elimination**
```
Upper-triangular matrix after elimination:
 [[ 4.     -1.      0.    ]
  [ 0.      3.75   -1.    ]
  [ 0.      0.      2.7333]]
Solution by Gaussian elimination: [5. 5. 5.]
```
*In words:* row 2 lost its first number (−1) when ¼ of row 1 was added, and row 3 lost its middle number in the same way. Now the last equation 2.7333·z = 13.6667 gives z = 5, then y = 5 and x = 5. The program checks this against `np.linalg.solve`.

**Part 2 – LU decomposition**
```
Measurement set 1 Solution: [5. 5. 5.]               Residual norm: 0.0
Measurement set 2 Solution: [5.31707317 5.26829268 4.75609756]   Residual norm: 1.78e-15
Measurement set 3 Solution: [4.90243902 5.6097561  5.53658537]   Residual norm: 0.0
```
*In words:* the same matrix A, factored only once, gives three different answers for three different measurement vectors. The residual norms are zero (or about 10⁻¹⁵), so each answer is correct. Set 1 also matches the direct solution `[5. 5. 5.]`.

## 7. Parameter change
**(a) Double b:** the solution doubles from [5, 5, 5] to [10, 10, 10]. The equations are linear, so doubling the inputs doubles the outputs.

**(b) Change one coefficient of A (A[0,0]: 4 → 6):** the solution changes from [5, 5, 5] to [3.254, 4.5238, 4.8413]. A larger first coefficient means the first unknown does not need to be as large to give the same total.

**(c) Why factor once?** Solving 200 different b vectors for a 400 × 400 matrix (one run on my computer; your timings will differ):

| Method | Time |
|---|---|
| Solve from scratch each time | 4.915 s |
| LU factor once and reuse | 0.025 s |

LU was about **194 times faster**. Factoring is the expensive step (it grows like n³), but each later solve is cheap (it grows like n²). This is why repeated solutions use LU.

## 8. Related real-world case: production needed to meet demand (Leontief input–output model)
**Assumptions**
- Three sectors: Agriculture, Manufacturing, Services. All numbers are **simulated**, in KES millions.
- C[i, j] is how much of sector i's output is needed to produce one unit of sector j's output.
- Consumers want a "final demand" d each year. Industries also use each other's products, so production x must satisfy x = Cx + d, which is **(I − C)x = d**.
- (I − C) is the same every year and only d changes, so LU is ideal.

**Output**
```
Year 1  Agriculture 40.0 -> must produce 73.14 | Manufacturing 60.0 -> 126.10 | Services 80.0 -> 118.03
        Total production 317.28 vs total final demand 180.0
Year 2  Total production 338.40 vs total final demand 192.0
Year 3  Total production 363.32 vs total final demand 206.0
```
**Interpretation:** to deliver only 180 million of goods to consumers in Year 1, the economy must produce 317 million in total, because factories use farm products, services use manufactured goods, and so on. All answers are positive, so the model is realistic, and each year's answer needed only a cheap `lu_solve` call after the single factorisation.

## 9. Conclusion
Gaussian elimination is the basic method for solving linear systems, and LU decomposition stores that work so that many right-hand sides can be solved cheaply.

**Key points to explain to the lecturer**
- Elimination makes the matrix triangular; back-substitution finishes the job.
- LU = "do the hard part once, reuse it for every new b".
- Doubling b doubles the solution; changing A changes it in a more complicated way.

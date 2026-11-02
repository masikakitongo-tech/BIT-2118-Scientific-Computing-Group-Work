# Task 6: Solution of Systems of Linear Equations

Program: `code/Task_06_linear_systems.py` | Saved output: `results/Task_06_output.txt`

## 1. Objective
To solve several linear equations at the same time by writing them as **Ax = b** and using `np.linalg.solve()`.

## 2. Mathematical concept (in simple words)
Many problems give several equations with several unknowns. We write them as **Ax = b**, where
- **A** holds the coefficients (the numbers in front of the unknowns),
- **x** holds the unknowns we want,
- **b** holds the known totals.

Solving the system means finding x so that A multiplied by x gives b. The **residual** b − Ax tells us how well the answer fits; it should be (almost) zero.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | 2x + 3y = 8 and 4x + y = 6, so A = [[2, 3], [4, 1]] and b = [8, 6] |
| 2 (PDF problem) | Type A server: 4 CPU units, 8 GB. Type B server: 2 CPU units, 12 GB. Totals: 20 CPU units, 72 GB |
| 3 (parameter change) | New totals 24 CPU units and 80 GB; and a matrix whose second row is double the first |
| 4 (my real-world case) | A three-loop electrical circuit (resistors 6, 4, 5, 3, 4 Ω; batteries 12 V and 6 V) |

## 4. Mathematical operations
- Writing equations as a matrix equation.
- Solving Ax = b with `np.linalg.solve(A, b)`.
- Verifying with the matrix product `A @ x` and the residual `b - A @ x`, measured with `np.linalg.norm`.
- Determinant (`np.linalg.det`) to detect a matrix that cannot be solved uniquely.

## 5. How the program works
For the servers, let x = number of Type A servers and y = number of Type B servers. The CPU equation is 4x + 2y = 20 and the memory equation is 8x + 12y = 72. The program puts these into A and b, solves, and then multiplies A by the answer to check that the totals are reproduced.

## 6. Output and what it means
**Part 1 – PDF example:** `Solution [x, y] = [1. 2.]`. Check: 2(1) + 3(2) = 8 and 4(1) + 2 = 6.

**Part 2 – servers**
```
Type A servers: 3
Type B servers: 4
Verification A @ solution: [20. 72.]
Residual: [0. 0.]
Residual norm: 0.0
```
*In words:* there are **3 Type A servers and 4 Type B servers**. Check: CPU = 3×4 + 4×2 = 20 and memory = 3×8 + 4×12 = 72, which are exactly the observed totals. The residual is zero, so the answer fits perfectly.

## 7. Parameter change
**(a) Different totals.** The totals change from (20 CPU, 72 GB) to (24 CPU, 80 GB):
```
Type A servers: 4, Type B servers: 4
```
*Explanation:* more resources are used, so more servers are running. Check: 4×4 + 4×2 = 24 and 4×8 + 4×12 = 80. The coefficients stayed the same; only b changed, so only the answer changed.

**(b) A system with no unique solution.** If Type B used exactly the same resources as Type A, the second row would be twice the first row:
```
Determinant: 0.0
np.linalg.solve failed with: Singular matrix
```
*Explanation:* two equations that say the same thing give no new information, so the unknowns cannot be found separately. A determinant of 0 warns us about this.

## 8. Related real-world case: currents in an electrical circuit
**Assumptions** (mesh-current analysis with Kirchhoff's voltage law)
- Loop 1 has a 12 V battery; loop 3 has a 6 V battery pushing the opposite way.
- R1 = 6 Ω (loop 1 only), R2 = 4 Ω (shared by loops 1 and 2), R3 = 5 Ω (shared by loops 2 and 3), R4 = 3 Ω (loop 2 only), R5 = 4 Ω (loop 3 only).
- The equations are: 10·I1 − 4·I2 = 12; −4·I1 + 12·I2 − 5·I3 = 0; −5·I2 + 9·I3 = −6.

**Output**
```
I1 = 1.2770 A (clockwise)
I2 = 0.1924 A (clockwise)
I3 = -0.5598 A (anticlockwise)
Current through shared resistor R2 (I1 - I2): 1.0845 A
Residual norm: 9.992007221626409e-16
```
**Interpretation:** loop 1 carries about 1.28 A and loop 2 about 0.19 A. The minus sign on I3 means the current in loop 3 actually flows the opposite way to the direction we assumed, because the 6 V battery in loop 3 is wired to push the current the other way. Resistor R2 is shared, so its current is the difference I1 − I2 = 1.08 A. The residual is about 10⁻¹⁵, which is zero apart from round-off error.

## 9. Conclusion
Writing a real problem as Ax = b lets NumPy solve it in one line, and the residual provides a quick test that the answer is correct. A zero determinant shows when a unique answer is impossible.

**Key points to explain to the lecturer**
- A = coefficients, x = unknowns, b = totals.
- Always verify with `A @ x` or the residual.
- A singular matrix (determinant 0) cannot be solved uniquely.

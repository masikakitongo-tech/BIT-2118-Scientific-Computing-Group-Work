# Task 4: Floating-Point Arithmetic and Numerical Errors

Program: `code/Task_04_numerical_errors.py` | Saved output: `results/Task_04_output.txt`

## 1. Objective
To understand how computers handle decimal numbers and why small numerical errors occur during calculations.

## 2. Mathematical concept (in simple words)
Computers store most decimal numbers using a finite number of **binary** digits, so many values are only approximations.
- **Absolute error** = |true value − approximate value|
- **Relative error** = absolute error ÷ |true value| (often shown as a percentage)
- **Round-off error** comes from the computer's limited precision. **Truncation error** comes from replacing an exact process with an approximation.

## 3. Input values
| Part | Input |
|---|---|
| 1–2 (PDF) | 0.1 and 0.2 (expected 0.3); true value √2 and approximation 1.414; x = 0.0001, 0.00000001 and 0.000000000001 for the stability test |
| 3 (parameter changes) | Approximations 1.4, 1.41, 1.414, 1.4142, 1.41421; smaller x (10⁻¹⁴, 10⁻¹⁶); repeated addition of 0.1 |
| 4 (real-world case) | Actual measurement 2.0, measured value 1.998; tolerance `atol` = 0.005, 0.003, 0.001 |

## 4. Mathematical operations
- Floating-point addition 0.1 + 0.2, an exact comparison with `==`, and a tolerance comparison with `np.isclose()`.
- Absolute error and relative error of an approximation of √2.
- Two mathematically **equal** formulas:
  - direct: (√(1+x) − 1) / x
  - stable: 1 / (√(1+x) + 1)
- Measurement error and percentage error.

## 5. Output and what it means
**Floating-point comparison**
```
0.1 + 0.2 = 0.30000000000000004
Exact comparison: False
Tolerance-based comparison: True
```
*In words:* 0.1 and 0.2 cannot be stored exactly in binary, so their sum is a tiny bit more than 0.3 and `==` says False. `np.isclose` accepts tiny differences, so it says True. Never compare decimals with `==`.

**Absolute and relative errors**
```
Absolute error: 0.00021356
Relative error: 0.01510114%
```
*In words:* using 1.414 instead of √2 = 1.41421356 is wrong by 0.000214, which is only 0.015% of the value. This matches the PDF (about 0.00021356 and 0.0151%).

**Numerical stability**
```
x=1e-04: direct=0.499987500624, stable=0.499987500625
x=1e-08: direct=0.499999996961, stable=0.499999998750
x=1e-12: direct=0.500044450291, stable=0.500000000000
```
*In words:* the true answer is very close to 0.5. For smaller x the direct formula subtracts two almost-equal numbers (√(1+x) and 1), so most of the correct digits cancel out and the answer drifts to 0.50004. The stable formula has no subtraction and stays accurate. This is called **cancellation error**.

## 6. Parameter change
**(a) Better approximations of √2**
| Approximation | Absolute error | Relative error |
|---|---|---|
| 1.4 | 0.01421356 | 1.005051% |
| 1.41 | 0.00421356 | 0.297944% |
| **1.414 (PDF)** | 0.00021356 | 0.015101% |
| 1.4142 | 0.00001356 | 0.000959% |
| 1.41421 | 0.00000356 | 0.000252% |

*Explanation:* each extra correct digit makes the error about ten times smaller, so more digits mean a smaller error.

**(b) Making x smaller in the unstable formula**
| x | direct | stable |
|---|---|---|
| 1e-12 | 0.500044450291 | 0.500000000000 |
| 1e-14 | 0.488498130835 | 0.500000000000 |
| 1e-16 | **0.000000000000** | 0.500000000000 |

*Explanation:* at x = 10⁻¹⁶ the computer cannot tell 1 + x from 1, so √(1+x) − 1 becomes exactly 0 and the direct formula gives a completely wrong answer. The stable formula is still correct.

**(c) Round-off adds up**
```
Sum of ten 0.1 values = 0.9999999999999999 | equals 1.0? False | np.isclose: True
Sum of one million 0.1 values = 100000.00000133288 | exact answer = 100000 | error = 1.3328826753422618e-06
```
*Explanation:* each addition carries a tiny error, and after a million additions the error is about 0.0000013. This is why simulations and banking systems must be careful.

## 7. Related real-world case: measurement accuracy check
**Assumptions:** an instrument should read 2.0 and gave 1.998. A reading is acceptable if it is within a tolerance of 0.005.

**Output**
```
Measurement error: 0.0020000000000000018
Percentage error: 0.10%
Result: Measurement is within the accepted tolerance.
```
**Interpretation:** the instrument is off by 0.002, which is 0.10% of the true value. The error is not printed as exactly 0.002 because of floating-point representation. With a stricter tolerance the decision changes:

| Tolerance (`atol`) | Decision for an error of 0.002 |
|---|---|
| 0.005 | within tolerance |
| 0.003 | within tolerance |
| 0.001 | **outside tolerance** |

So the same measurement can pass or fail depending on the tolerance chosen, and the tolerance must match the purpose (for example, a medical device needs a much stricter tolerance than a kitchen scale).

## 8. Real-world applications
Floating-point arithmetic matters in scientific simulations, banking calculations, GPS navigation, engineering design and iterative algorithms.

## 9. Conclusion
Computers do not always represent decimal numbers exactly. Using tolerance-based comparisons (`np.isclose`) and numerically stable formulas helps reduce errors and improve the reliability of scientific calculations.

**Key points to explain to the lecturer**
- `0.1 + 0.2 == 0.3` is False because of binary approximation; use `np.isclose`.
- Absolute error is the size of the mistake; relative error compares it with the true value.
- Subtracting almost-equal numbers destroys accuracy, so rewrite the formula to avoid it.

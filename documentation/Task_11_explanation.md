# Task 11: Root Finding – Newton-Raphson and Secant Methods

Program: `code/Task_11_newton_secant.py` | Saved output: `results/Task_11_output.txt`

## 1. Objective
To find roots with the faster Newton-Raphson and secant methods, and to use them to calculate an interest rate (internal rate of return, IRR).

## 2. Mathematical concept (in simple words)
- **Newton-Raphson** improves a guess using the tangent line: xₙ₊₁ = xₙ − f(xₙ) / f′(xₙ). It needs the derivative f′.
- **Secant method** does the same without the derivative: it estimates the slope from the last two points.
- Both usually converge much faster than bisection if the starting guess is reasonable.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | f(x) = x² − 2 with starting guess x₀ = 1.5 |
| 2 (PDF problem) | Cash flows [−10000, 3000, 3500, 4000, 2500] (an investment and four yearly inflows); Newton start 0.10; secant starts 0.05 and 0.20 |
| 3 (parameter changes) | Starting guesses 0.01, 0.10, 0.50; last inflow changed from 2500 to 3500 |
| 4 (my real-world case) | A laptop: cash price KES 50,000 or 12 monthly instalments of KES 4,600 (simulated) |

## 4. Mathematical operations
- Net present value: NPV(r) = Σ cashflow_t / (1 + r)ᵗ. The IRR is the rate r with NPV(r) = 0.
- Derivative of the NPV: d/dr = Σ −t · cashflow_t / (1 + r)^(t+1).
- Newton update and secant update, using `root_scalar(..., method="newton")` and `method="secant"`.
- Effective annual rate = (1 + monthly rate)¹² − 1.

## 5. How the program works
Part 1 applies the Newton formula by hand. Parts 2–4 give `root_scalar` the NPV function (and its derivative for Newton) and let it repeat until the answer changes by less than 10⁻¹². The result's `.iterations` tells how many steps were needed.

## 6. Output and what it means
**Part 1 – x² − 2**
```
x1 = 1.4166666667   error = 2.45e-03
x2 = 1.4142156863   error = 2.12e-06
x3 = 1.4142135624   error = 1.59e-12
```
*In words:* the first step gives 1.4167, exactly the PDF's x₁. The error drops from 0.0025 to 0.0000021 to 0.0000000000016: it roughly **squares each time**, which means the number of correct digits doubles at every step.

**Part 2 – IRR**
```
IRR using Newton-Raphson: 11.542461%
IRR using Secant method:  11.542461%
NPV at Newton solution:   0.000000
Iterations: Newton = 4 | Secant = 7
```
*In words:* the investment earns about **11.54% per year**. At that rate the discounted inflows exactly repay the 10,000 invested, so the NPV is 0. Newton needed 4 steps and secant 7: secant is a little slower but needs no derivative.

## 7. Parameter change
**(a) Starting guess**
| x₀ | Newton IRR | Newton steps | Secant IRR | Secant steps |
|---|---|---|---|---|
| 0.01 | 11.542461% | 5 | 11.542461% | 7 |
| 0.10 | 11.542461% | 4 | 11.542461% | 7 |
| 0.50 | 11.542461% | 8 | 11.542461% | 11 |

*Explanation:* every start reaches the same answer, but a start close to the root (0.10) needs fewer steps than a start far away (0.50).

**(b) Last inflow 2500 → 3500:** the IRR rises from **11.54%** to **14.46%**. Bigger returns make the investment more profitable, so the rate that balances it is higher.

## 8. Related real-world case: the true interest rate of an instalment plan
**Assumptions** (simulated)
- A shop sells a laptop for KES 50,000 cash or 12 monthly instalments of KES 4,600. The shop never states the interest rate.
- The monthly rate r is the one that makes the discounted instalments equal the cash price, so the cash flows are [−50000, +4600 × 12] and NPV(r) = 0.

**Output**
```
Monthly interest rate (Newton): 1.5560%   (Secant: 1.5560%)
Nominal annual rate (12 x monthly): 18.67%
Effective annual rate (compounded): 20.36%
Total paid: KES 55,200 | extra over cash price: KES 5,200
Present value of the instalments at that rate: KES 50,000.00
```
**Interpretation:** the shop charges about **1.56% per month**, which is a nominal 18.67% per year and an effective **20.36%** per year once compounding is included. The customer pays KES 5,200 more than the cash price. The program checks that the 12 instalments, discounted at this rate, are worth exactly KES 50,000. With a lower instalment of KES 4,400 the monthly rate falls to 0.8484% (effective 10.67% a year), so the buyer can compare offers by their true rate. Banks and shops use this calculation for loan and hire-purchase quotations.

## 9. Conclusion
Newton-Raphson and secant methods find roots in only a few iterations when started well. They are widely used for financial rates, where there is no simple formula.

**Key points to explain to the lecturer**
- Newton uses the derivative (tangent line); secant estimates it from two points.
- Near the root, the number of correct digits roughly doubles each step for Newton.
- A very bad starting guess can need more steps or fail, so choose a sensible start.

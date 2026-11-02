# Task 10: Root Finding – Bisection and Fixed-Point Methods

Program: `code/Task_10_bisection_fixed_point.py` | Saved output: `results/Task_10_output.txt`
Graphs: `results/Task_10_equilibrium_temperature.png`, `results/Task_10_break_even.png`

## 1. Objective
To find a **root** of an equation (a value that makes f(x) = 0) using the bisection method and the fixed-point method, and to compare how fast they converge.

## 2. Mathematical concept (in simple words)
- A **root** of f(x) is a number r with f(r) = 0.
- **Bisection:** pick an interval [a, b] where f(a) and f(b) have *opposite signs* (so the graph must cross zero somewhere between them). Cut the interval in half, keep the half that still has the sign change, and repeat. The interval shrinks by half every step.
- **Fixed-point iteration:** rewrite the equation as x = g(x), then repeat xₙ₊₁ = g(xₙ). It works when the slope of g near the root is smaller than 1 in size (|g′| < 1).

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | f(x) = x³ − x − 2 on [1, 2]; f(1) = −2 and f(2) = 4 |
| 2 (PDF problem) | f(T) = T − 25 − 10·e^(−T/20); bracket [20, 40]; tolerance 10⁻¹⁰; fixed-point form g(T) = 25 + 10·e^(−T/20) starting at T = 30 |
| 3 (parameter changes) | Brackets [20, 40], [25, 30], [27, 28]; tolerances 10⁻³ and 10⁻¹⁰; a bad bracket [30, 40]; fixed-point start values 0, 30, 100 |
| 4 (my real-world case) | Revenue R(q) = 80q − 0.005q², cost C(q) = 5000 + 20q + 0.02q², so profit P(q) = 60q − 0.025q² − 5000 |

## 4. Mathematical operations
- Midpoint (a + b) / 2 and a sign test f(a)·f(mid) ≤ 0.
- `root_scalar(..., method="bisect")` from SciPy, plus my own `bisection()` function that prints each step.
- Repeated substitution T ← g(T) until the change is below 10⁻¹⁰.
- The exponential function `np.exp`.

## 5. How the program works
`bisection()` checks that f(a) and f(b) have opposite signs, then loops: find the midpoint, decide which half contains the sign change, shrink the interval. SciPy's `root_scalar` does the same job for the PDF problem and also reports the number of iterations.

## 6. Output and what it means
**Part 1 – x³ − x − 2** (first steps)
| Step | a | b | midpoint | f(midpoint) |
|---|---|---|---|---|
| 1 | 1.000000 | 2.000000 | 1.500000 | −0.125000 |
| 2 | 1.500000 | 2.000000 | 1.750000 | 1.609375 |
| 3 | 1.500000 | 1.750000 | 1.625000 | 0.666016 |
| 4 | 1.500000 | 1.625000 | 1.562500 | 0.252197 |

After 26 halvings the root is **1.52137970**. *In words:* f(1.5) is negative and f(1.75) is positive, so the root is between them; every step halves the interval.

**Part 2 – heat balance**
```
Bisection equilibrium temperature: 27.525211 C
Fixed-point equilibrium temperature: 27.525211 C
Fixed-point iterations: 13
Bisection iterations: 38
```
*In words:* heat gain equals heat loss at about **27.53 °C**. Both methods give the same answer, but the fixed-point method needed only 13 steps against 38 for bisection, because here the slope of g is small (about 0.13 near the root), so each step removes most of the error. Bisection is slower but is *guaranteed* to work whenever the signs differ.

## 7. Graph and interpretation
**`Task_10_equilibrium_temperature.png`:** the blue curve is the heat-balance function. It is negative below about 27.5 °C (loss is larger than gain) and positive above it. The dashed vertical line marks the root where the curve crosses the horizontal zero line, so this temperature is the equilibrium.

**`Task_10_break_even.png`:** see section 9.

## 8. Parameter change
**(a) Bracket and tolerance (bisection)**
| Bracket | xtol | Iterations | Root |
|---|---|---|---|
| [20, 40] | 10⁻³ | 15 | 27.52502441 |
| [20, 40] | 10⁻¹⁰ | 38 | 27.52521082 |
| [25, 30] | 10⁻³ | 13 | 27.52502441 |
| [25, 30] | 10⁻¹⁰ | 36 | 27.52521082 |
| [27, 28] | 10⁻³ | 10 | 27.52441406 |
| [27, 28] | 10⁻¹⁰ | 34 | 27.52521082 |

*Explanation:* a **smaller tolerance** needs more iterations (about 3.3 extra steps for every extra decimal digit); a **narrower bracket** saves a few steps; the root itself does not change (only its last digits, according to the tolerance).

**(b) A bad bracket [30, 40]:** f(30) = 2.77 and f(40) = 13.65 are both positive, so SciPy refuses: *"f(a) and f(b) must have different signs"*. Without a sign change bisection cannot know where the root is.

**(c) Fixed-point starting values:** starting from 0 °C, 30 °C and 100 °C all lead to 27.525211 °C, after 15, 13 and 14 iterations. The answer does not depend on the start because |g′(T)| = 0.5·e^(−T/20) stays well below 1.

## 9. Related real-world case: break-even points of a business
**Assumptions** (simulated, amounts in KES)
- Revenue R(q) = 80q − 0.005q² (the price must fall a little when more is sold).
- Cost C(q) = 5000 + 20q + 0.02q² (5000 fixed cost, 20 per unit, extra cost at high volume).
- A break-even point is where profit P(q) = R(q) − C(q) = 0. There are two sign changes, so two brackets are used: [0, 500] and [1000, 4000].

**Output**
```
Lower break-even point: 86.45 units (exact 86.45)
Upper break-even point: 2313.55 units (exact 2313.55)
Most profitable quantity: 1200 units, profit = KES 31,000
Profit at 50 units:   KES -2,062
Profit at 500 units:  KES 18,750
Profit at 3000 units: KES -50,000
```
**Interpretation:** the business must sell at least **87 units** to stop making a loss. It makes a profit for any quantity between about 87 and 2,313 units, and the best quantity is about 1,200 units (profit KES 31,000). Beyond about 2,314 units the rising costs and falling price lead to a loss again. The bisection answers agree with the exact answers from the quadratic formula, which confirms that the method is correct. The graph shows the profit curve as a hill, with the two break-even lines where it crosses zero and the peak marked.

## 10. Conclusion
Bisection is safe and simple but slow; fixed-point iteration is faster when it converges. A sign change (bisection) or a small slope (fixed point) is the condition that each method needs.

**Key points to explain to the lecturer**
- Bisection halves the interval each time, so after n steps the error is at most (b − a)/2ⁿ.
- Always check f(a) and f(b) have opposite signs.
- Fixed-point iteration only works when |g′(x)| < 1 near the root.

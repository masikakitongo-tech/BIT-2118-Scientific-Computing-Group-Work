# Task 18: Numerical Solution of ODEs Using SciPy

Program: `code/Task_18_scipy_ode.py` | Saved output: `results/Task_18_output.txt`
Graphs: `results/Task_18_rc_circuit.png`, `results/Task_18_sir_epidemic.png`

## 1. Objective
To solve differential equations with `scipy.integrate.solve_ivp`, a professional solver that automatically chooses its own step sizes, and to apply it to a circuit and to an epidemic.

## 2. Mathematical concept (in simple words)
Like Task 17, we solve dy/dt = f(t, y) from a starting value. Euler's method uses a fixed step. `solve_ivp` uses higher-order methods (by default "RK45", a Runge–Kutta method) and **adjusts its step size automatically** to meet an accuracy target given by the tolerances `rtol` (relative) and `atol` (absolute). It can also solve several linked equations at once.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | Exponential decay dy/dt = −ky with k = 0.3 per hour and y(0) = 100 (a drug amount in mg) |
| 2 (PDF problem) | RC circuit: Vs = 5 V, R = 1000 Ω, C = 0.001 F, V(0) = 0, times 0–5 s |
| 3 (parameter changes) | C = 0.002 F; tolerances rtol = 10⁻³, 10⁻⁶, 10⁻⁹ |
| 4 (my real-world case) | An epidemic in a town of 10,000 people, 10 infected at the start, recovery rate γ = 0.1 per day, infection rate β = 0.3 and then 0.15 per day (simulated) |

## 4. Mathematical operations
- RC charging equation dV/dt = (Vs − V)/(RC); exact solution V(t) = Vs(1 − e^(−t/RC)).
- `solve_ivp(function, (t_start, t_end), [initial values], t_eval=times, rtol=..., atol=...)`.
- SIR epidemic model, three linked equations:
  dS/dt = −βSI/N, dI/dt = βSI/N − γI, dR/dt = γI.

## 5. How the program works
The right-hand side of the ODE is written as a Python function `f(t, y)` and passed to `solve_ivp` with the initial values. The result `solution.t` holds the times and `solution.y` the computed values. The program compares them with the exact formulas where they exist.

## 6. Output and what it means
**Part 1 – decay:** `solve_ivp` gives 100.0000, 54.8812, 22.3130 and 4.9787 at 0, 2, 5 and 10 hours, identical to 100·e^(−0.3t) to four decimals. *In words:* the amount of drug in the blood falls by about 26% per hour and is down to 5 mg after 10 hours.

**Part 2 – RC circuit**
```
Solver success: True
Capacitor voltage at 5 s: 4.9663 V
Maximum error against exact solution: 9.282e-10 V
Time constant R*C = 1.0 s (voltage reaches 63.2% of 5.0 V = 3.16 V at this time)
```
*In words:* the capacitor charges almost to the 5 V supply (4.97 V after 5 s). The numerical answer differs from the exact formula by less than a billionth of a volt. The **time constant** RC = 1 s tells how fast it charges: after 1 s it holds 63.2% of the supply voltage (3.16 V).

## 7. Graph and interpretation
**`Task_18_rc_circuit.png`:** the voltage rises steeply at first and then flattens near 5 V (the charging current shrinks as the capacitor fills). The solid `solve_ivp` curve and the dashed exact curve lie on top of each other, so they cannot be told apart, which shows the solver is accurate.

**`Task_18_sir_epidemic.png`:** see section 9.

## 8. Parameter change
**(a) Capacitance 0.001 F → 0.002 F** (time constant 1 s → 2 s)
| C (F) | RC (s) | V at 1 s | V at 2 s | V at 5 s |
|---|---|---|---|---|
| 0.001 | 1.0 | 3.161 | 4.323 | 4.966 |
| 0.002 | 2.0 | 1.967 | 3.161 | 4.590 |

*Explanation:* a bigger capacitor holds more charge, so it charges more slowly. With C = 0.002 F the circuit takes 2 s (not 1 s) to reach 63.2% (3.161 V).

**(b) Solver accuracy**
| rtol | Function calls | Largest error (V) |
|---|---|---|
| 10⁻³ | 56 | 6.64×10⁻⁴ |
| 10⁻⁶ | 122 | 8.67×10⁻⁷ |
| 10⁻⁹ | 386 | 9.28×10⁻¹⁰ |

*Explanation:* demanding more accuracy makes the solver work harder (more function evaluations) and the error shrinks by about the same factor as the tolerance.

## 9. Related real-world case: an epidemic (SIR model)
**Assumptions** (simulated)
- Town of N = 10,000; at the start 10 people are infected (I), 9,990 are susceptible (S) and none have recovered (R).
- Each infected person transmits at rate β and recovers at rate γ = 0.1 per day. The basic reproduction number is R₀ = β/γ.
- Two scenarios: β = 0.3 (R₀ = 3, no precautions) and β = 0.15 (R₀ = 1.5, for example mask-wearing and distancing).

**Output**
| β | R₀ | Peak infected | Peak day | Infected by day 160 |
|---|---|---|---|---|
| 0.3 | 3.0 | 3,008 | 38.2 | 9,405 |
| 0.15 | 1.5 | 637 | 114.0 | 5,259 |

The program also checks that S + I + R equals 10,000 at all times (nobody is created or lost).

**Interpretation (graph):** with no precautions, the infection grows rapidly: the red curve peaks at about **3,000 people infected at the same time on day 38**, and by day 160 about 9,400 of the 10,000 (94%) have been infected, while the blue susceptible curve collapses. When transmission is halved, the peak falls by about 79% (from 3,008 to 637) and comes about 76 days later, and fewer people are infected by day 160 (the second epidemic is still ending at that time). This is the "flatten the curve" idea: it keeps the number of simultaneous patients low enough for hospitals to cope. The model is a simplified illustration with made-up numbers, not a prediction for a real disease.

## 10. Conclusion
`solve_ivp` solves single equations and systems of equations accurately without the user choosing step sizes. A tolerance controls the accuracy, and the same function handles circuits, epidemics, chemical reactions and mechanical systems.

**Key points to explain to the lecturer**
- Write the equations as a function f(t, y), give the starting values, call `solve_ivp`.
- The solver picks its own steps; `rtol` and `atol` set the accuracy.
- Systems of linked equations (such as S, I, R) are solved together.

# Task 20: Random Numbers and Monte Carlo Methods

Program: `code/Task_20_monte_carlo.py` | Saved output: `results/Task_20_output.txt`
Graphs: `results/Task_20_pi_estimate.png`, `results/Task_20_overload_convergence.png`, `results/Task_20_project_duration.png`

## 1. Objective
To estimate quantities and probabilities by repeated random sampling (Monte Carlo simulation).

## 2. Mathematical concept (in simple words)
In a **Monte Carlo method** we repeat a random experiment many times on the computer and use the results to estimate an answer. If an event has probability p, then after N simulations the fraction of times it happens approaches p as N grows. The error shrinks roughly like 1/√N, so 100 times more simulations give about 10 times less noise.

Classic example: throw random points into a unit square. The part inside the quarter circle x² + y² ≤ 1 covers π/4 of the square, so **π ≈ 4 × (points inside / total points)**. If 7,850 of 10,000 points fall inside, π ≈ 4 × 0.785 = 3.14.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | N = 100 up to 1,000,000 random points in the unit square (seed 1) |
| 2 (PDF problem) | Server capacity 1000; demand is normal with mean 850 and standard deviation 120; N = 100,000 simulations (seed 42) |
| 3 (parameter changes) | Capacity 1100; standard deviation 150; N = 100, 1,000, 100,000 with five different seeds |
| 4 (my real-world case) | A software project with three tasks in sequence — Design (5, 7, 12 days), Build (10, 14, 25), Testing (3, 5, 10) — as (fastest, most likely, slowest); deadline 35 days; N = 100,000 (simulated) |

## 4. Mathematical operations
- Random numbers from `np.random.default_rng(seed)`: `random()` (uniform), `normal()`, `triangular()`.
- Counting how often a condition is true and dividing by N (the mean of a True/False array).
- Running probability `np.cumsum(overloaded) / np.arange(1, N + 1)`.
- Percentiles (`np.percentile`) and the exact normal-distribution tail `scipy.stats.norm.sf` for checking.

## 5. How the program works
A random generator with a fixed **seed** makes the "random" numbers repeatable, so results can be reproduced. For the server problem, 100,000 random demand values are generated; each value above the capacity is an "overload", and the fraction of overloads is the estimated probability.

## 6. Output and what it means
**Part 1 – estimating π**
| Points N | Estimate of π | Error |
|---|---|---|
| 100 | 3.12000 | 0.02159 |
| 1,000 | 3.12800 | 0.01359 |
| 10,000 | 3.13160 | 0.00999 |
| 100,000 | 3.15240 | 0.01081 |
| 1,000,000 | 3.14259 | 0.00100 |

*In words:* with more random points the estimate gets closer to π = 3.14159, but not in a perfectly steady way (the error with 100,000 points is slightly larger than with 10,000, which is just chance). On average the error decreases like 1/√N. The graph `Task_20_pi_estimate.png` shows 2,000 points: blue ones fall inside the quarter circle and red ones outside; the ratio gives the π estimate.

**Part 2 – server overload**
```
Estimated overload probability: 10.6160%
Number of overload cases: 10616 out of 100000
Exact probability (normal distribution): 10.5650%
Simulation error: 0.0510%
```
*In words:* demand exceeds the capacity of 1000 in about **10.6% of the scenarios**, roughly one day in nine. The exact value from the normal distribution is 10.57%, so the simulation is very close (0.05% error).

## 7. Graph and interpretation
**`Task_20_overload_convergence.png`:** the blue line is the running estimate of the overload probability against the number of simulations (log scale). At the start (10–100 simulations) it jumps around and even shows 0; after about 1,000 simulations it stays near 0.10, and after 100,000 it lies almost exactly on the red dashed line, which marks the exact value 10.57%. This shows that more simulations give a more reliable estimate.

## 8. Parameter change
**(a) Capacity and spread** (N = 100,000)
| Capacity | Std dev | Simulated | Exact |
|---|---|---|---|
| 1000 | 120 | 10.616% | 10.565% |
| **1100** | 120 | 1.912% | 1.861% |
| 1000 | **150** | 15.839% | 15.866% |

*Explanation:* raising the capacity by 10% (1000 → 1100) cuts the overload risk from 10.6% to 1.9%. More unpredictable demand (std 150 instead of 120) raises the risk from 10.6% to 15.8%, even though the average demand is unchanged.

**(b) Number of simulations** (five different seeds each)
| N | Estimates | Spread |
|---|---|---|
| 100 | 17%, 3%, 8%, 9%, 10% | 14.0% |
| 1,000 | 9.7%, 8.7%, 10.9%, 11.6%, 11.1% | 2.9% |
| 100,000 | 10.50%, 10.33%, 10.61%, 10.64%, 10.61% | 0.31% |

*Explanation:* with only 100 simulations the answer varies from 3% to 17% depending on the seed, which is useless; with 100,000 it varies by only 0.3%. More simulations mean less randomness in the answer.

## 9. Related real-world case: will the project finish on time?
**Assumptions** (simulated)
- Three tasks run one after another; each duration is uncertain and described by (fastest, most likely, slowest) days in a triangular distribution.
- The deadline is 35 days. We simulate 100,000 projects and add the three durations in each one.

**Output**
```
Plan using the 'most likely' times: 26 days
Simulated average duration:         30.33 days
Shortest / longest in simulation:   19.2 / 45.1 days
Probability of finishing after 35 days: 12.27%
Duration needed for 50% / 80% / 90% / 95% confidence: 30.1 / 33.6 / 35.5 / 37.0 days
If Build's slowest case drops from 25 to 18 days: P(late) 12.27% -> 0.41%, 90% confidence 35.5 -> 31.5 days
```
**Interpretation:** the simple plan adds the "most likely" times and says **26 days**, but the average simulated duration is **30.3 days**, because every task is more likely to run late than early (long upper tails). There is a **12% chance of missing the 35-day deadline**, and a manager who wants 90% confidence should promise 35.5 days, not 26. The histogram (`Task_20_project_duration.png`) is skewed to the right, with the red dashed deadline line and the green 90%-confidence line. Reducing the worst-case build time from 25 to 18 days cuts the risk of lateness from 12.3% to 0.4%, which shows where managers should focus their effort. A single-number plan hides all of this risk information.

## 10. Conclusion
Monte Carlo simulation gives estimates for problems that are hard to solve exactly. The answer improves as the number of simulations grows, and the results include risk information (probabilities and percentiles), not only averages.

**Key points to explain to the lecturer**
- Random sampling plus counting gives probabilities: overloaded cases ÷ total cases.
- The seed makes random results repeatable.
- More simulations mean less noise (error ∝ 1/√N); the simulation agrees with the exact answer, which validates the method.

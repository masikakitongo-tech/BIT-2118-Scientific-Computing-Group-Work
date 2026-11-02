# Task 19: Numerical Optimization

Program: `code/Task_19_optimization.py` | Saved output: `results/Task_19_output.txt` | Graph: `results/Task_19_production_plan.png`

## 1. Objective
To find the inputs that give the smallest cost (or the largest profit) subject to limits, using `scipy.optimize.minimize`.

## 2. Mathematical concept (in simple words)
**Optimization** looks for the input values that **minimise or maximise an objective function**. Real problems usually have **constraints**, for example "at least 1000 units of capacity" or "no more than 100 labour-hours", and **bounds** such as x ≥ 0. To *maximise* something with `minimize`, we minimise its negative.

Example: f(x) = (x − 3)² + 2 is smallest when the squared term is 0, so the minimum is at x = 3 with value 2.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | f(x) = (x − 3)² + 2, starting at x = 0 |
| 2 (PDF problem) | Two server types: cost 12 and 18 per unit, capacity 100 and 170 per unit; need at least 1000 capacity; start at (5, 3) |
| 3 (parameter changes) | Cost of Type B 18 → 22; required capacity 1000 → 1500 |
| 4 (my real-world case) | A furniture workshop: profit 40 per table and 30 per chair (KES thousand); 100 labour-hours and 240 units of wood per week; a table uses 2 hours and 3 wood, a chair 1 hour and 4 wood (simulated) |

## 4. Mathematical operations
- Objective function: cost = 12x + 18y.
- Inequality constraint: 100x + 170y − 1000 ≥ 0 (written as `type: "ineq"`, where the function must be ≥ 0).
- Bounds: x ≥ 0 and y ≥ 0.
- Method `SLSQP` (a solver for constrained problems).
- A search over whole-number combinations to find the best plan when only whole servers are allowed.

## 5. How the program works
`minimize(cost, x0, method="SLSQP", bounds=..., constraints=...)` starts at x0 and moves towards lower cost while keeping the constraints satisfied. Because it treats x and y as continuous (e.g. 5.882 servers), the program also tries every whole-number pair in a range and keeps the cheapest valid one.

## 6. Output and what it means
**Part 1:** the minimum is found at x = 3.000000 with f = 2.000000, as in the PDF.

**Part 2 – cheapest server plan**
```
Optimization success: True
Type A allocation: 0.000
Type B allocation: 5.882
Total capacity: 1000.00
Minimum planning cost: 105.88
Best nearby integer solution: (108, 0, 6, 1020)
Cost per unit of capacity: A = 0.12 | B = 0.1059 -> Type B is cheaper per unit of capacity
```
*In words:* the cheapest way to get 1000 units of capacity is to use **only Type B servers** (5.88 units, cost 105.88), because each unit of capacity costs 0.106 with Type B and 0.12 with Type A. The capacity ends up exactly 1000, so the constraint is "tight": the cheapest plan uses no more capacity than required. When whole servers are required, the best plan is **6 Type B servers**, capacity 1020 and cost 108.

## 7. Parameter change
| Cost A | Cost B | Required | Units A | Units B | Min cost | Whole servers (cost, A, B) |
|---|---|---|---|---|---|---|
| 12 | 18 | 1000 | 0.000 | 5.882 | 105.88 | (108, 0, 6) |
| 12 | **22** | 1000 | **10.000** | 0.000 | 120.00 | (120, 10, 0) |
| 12 | 18 | **1500** | 0.000 | 8.824 | 158.82 | (162, 0, 9) |

*Explanation:* when Type B becomes more expensive (22), its cost per unit of capacity (0.129) is now higher than that of Type A (0.12), so the optimal plan **switches completely** to Type A servers (10 of them, cost 120). When more capacity is needed (1500), the plan stays with Type B but costs more (158.82, or 162 with 9 whole servers). A small change in a parameter can change the whole solution.

## 8. Graph and interpretation
**`Task_19_production_plan.png`:** the blue shaded region contains all the weekly plans (tables x and chairs y) that fit within the labour and wood limits. The two straight lines are the limits themselves. The dashed black line connects all plans that give the same profit as the best one, and the red dot is the best plan, in the corner where the two limits cross. Any plan with a higher profit lies on a line further from the origin, completely outside the shaded region, so it is not possible.

## 9. Related real-world case: a furniture workshop maximising profit
**Output**
```
Tables per week: 32.00
Chairs per week: 36.00
Maximum weekly profit: KES 2360.00 thousand
Labour used: 100.0 of 100 hours | wood used: 240.0 of 240 units
Best whole-number plan (profit, tables, chairs): (2360, 32, 36)
```
**Interpretation:** the workshop should make **32 tables and 36 chairs per week** for a maximum profit of KES 2,360 thousand (KES 2.36 million). This uses all 100 labour-hours and all 240 units of wood, so both resources limit the plan. The solution happens to be whole numbers, and a brute-force search of all whole-number plans confirms that nothing is better.

**Parameter changes**
| Profit/table | Profit/chair | Labour hours | Tables | Chairs | Profit |
|---|---|---|---|---|---|
| 40 | 30 | 100 | 32 | 36 | 2,360 |
| 40 | **60** | 100 | 0 | 60 | 3,600 |
| 40 | 30 | **120** | 48 | 24 | 2,640 |

*Explanation:* if chairs earn 60 instead of 30, the workshop should build **only chairs** (60 per week, profit 3,600). If 20 extra labour-hours become available, it can make more tables (48) and fewer chairs (24), and the profit rises by 280.

## 10. Conclusion
Optimization finds the best allocation of limited resources. Writing the objective, the constraints and the bounds clearly is the main job; `minimize` does the searching. A whole-number check is needed when fractional answers are not allowed.

**Key points to explain to the lecturer**
- Objective function = what we want to minimise; constraints = limits we must obey.
- To maximise, minimise the negative of the objective.
- The best solution is often at a "corner" where constraints meet.

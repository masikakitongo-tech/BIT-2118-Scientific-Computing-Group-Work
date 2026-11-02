# Task 18: Numerical Solution of ODEs Using SciPy (solve_ivp)
#
# Part 1 - the lecturer's small example: exponential decay dy/dt = -k y
# Part 2 - the lecturer's RC-circuit problem (original solution code)
# Part 3 - changing the capacitance and the solver's accuracy settings
# Part 4 - a related real-world case (an epidemic: the SIR model)

from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example - exponential decay
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - exponential decay dy/dt = -k y ===")
# Example: the amount of a drug in the blood. y(0) = 100 mg, k = 0.3 per hour.
k_decay, y0 = 0.3, 100.0


def decay(t, y):
    return -k_decay * y


sol = solve_ivp(decay, (0, 10), [y0], t_eval=[0, 2, 5, 10], rtol=1e-9, atol=1e-12)
exact_vals = y0 * np.exp(-k_decay * sol.t)
print(f"{'t (h)':>6} {'solve_ivp':>11} {'Exact':>9}")
for t, num, ex in zip(sol.t, sol.y[0], exact_vals):
    print(f"{t:>6.0f} {num:>11.4f} {ex:>9.4f}")
assert np.allclose(sol.y[0], exact_vals, rtol=1e-6)
print("Self-check passed: the numerical solution matches y0 * exp(-k t)")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's RC-circuit problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Charging an RC circuit ===")

# RC charging circuit:
# dV/dt = (Vs - V)/(R*C)
Vs = 5.0          # supply voltage (V)
R = 1000.0        # resistance (ohms)
C = 0.001         # capacitance (farads)
V0 = 0.0          # initial capacitor voltage

def rc_circuit(t, V):
    return [(Vs - V[0]) / (R * C)]

t_eval = np.linspace(0, 5, 200)

solution = solve_ivp(
    rc_circuit,
    (0, 5),
    [V0],
    t_eval=t_eval,
    rtol=1e-9,
    atol=1e-11
)

# Exact RC charging curve for validation
exact = Vs * (1 - np.exp(-solution.t / (R * C)))

print("Solver success:", solution.success)
print(f"Capacitor voltage at 5 s: {solution.y[0, -1]:.4f} V")
print(f"Maximum error against exact solution: {np.max(np.abs(solution.y[0]-exact)):.3e} V")
print(f"Time constant R*C = {R * C} s (voltage reaches 63.2% of {Vs} V = {0.632 * Vs:.2f} V at this time)")

plt.plot(solution.t, solution.y[0], label="solve_ivp")
plt.plot(solution.t, exact, linestyle="--", label="Exact")
plt.xlabel("Time (s)")
plt.ylabel("Capacitor voltage (V)")
plt.title("RC circuit charging")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_18_rc_circuit.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_18_rc_circuit.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")

# (a) Double the capacitance: 0.001 F -> 0.002 F (time constant 1 s -> 2 s).
print("(a) Capacitor voltage (V) at different times for different capacitances:")
print(f"{'C (F)':>8} {'RC (s)':>7} {'V at 1 s':>9} {'V at 2 s':>9} {'V at 5 s':>9}")
for cap in (0.001, 0.002):
    def rc_c(t, V, cap=cap):
        return [(Vs - V[0]) / (R * cap)]
    s = solve_ivp(rc_c, (0, 5), [V0], t_eval=[1, 2, 5], rtol=1e-9, atol=1e-11)
    print(f"{cap:>8} {R * cap:>7.1f} {s.y[0, 0]:>9.3f} {s.y[0, 1]:>9.3f} {s.y[0, 2]:>9.3f}")

# (b) Change the solver's accuracy settings.
print("\n(b) Different accuracy settings (original circuit):")
print(f"{'rtol':>8} {'Function calls':>15} {'Largest error (V)':>19}")
for rtol, atol in ((1e-3, 1e-6), (1e-6, 1e-9), (1e-9, 1e-11)):
    s = solve_ivp(rc_circuit, (0, 5), [V0], t_eval=t_eval, rtol=rtol, atol=atol)
    err = np.max(np.abs(s.y[0] - Vs * (1 - np.exp(-s.t / (R * C)))))
    print(f"{rtol:>8.0e} {s.nfev:>15} {err:>19.2e}")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - an epidemic (SIR model)
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A town of N = 10,000 people. At the start 10 people are infected (I),
#     the rest are Susceptible (S) and nobody has Recovered (R).
#   * Each infected person infects others at rate beta = 0.3 per day, and
#     recovers at rate gamma = 0.1 per day, so R0 = beta / gamma = 3.
#   * Three linked ODEs (solve_ivp can solve several at once):
#         dS/dt = -beta S I / N
#         dI/dt =  beta S I / N - gamma I
#         dR/dt =  gamma I
print("\n=== PART 4: Epidemic spread (SIR model) ===")
N_POP = 10_000.0


def run_sir(beta, gamma, days=160):
    def sir(t, y):
        S, I, Rec = y
        return [-beta * S * I / N_POP,
                beta * S * I / N_POP - gamma * I,
                gamma * I]

    days_eval = np.linspace(0, days, days * 4 + 1)
    return solve_ivp(sir, (0, days), [N_POP - 10, 10, 0],
                     t_eval=days_eval, rtol=1e-8, atol=1e-10)


results = {}
print(f"{'beta':>5} {'R0':>4} {'Peak infected':>14} {'Peak day':>9} {'Infected by day 160':>20}")
for beta in (0.3, 0.15):
    sir_sol = run_sir(beta, 0.1)
    results[beta] = sir_sol
    S_, I_, R_ = sir_sol.y
    peak_i = int(np.argmax(I_))
    ever_infected = N_POP - S_[-1]
    print(f"{beta:>5} {beta / 0.1:>4.1f} {I_[peak_i]:>14.0f} {sir_sol.t[peak_i]:>9.1f} {ever_infected:>20.0f}")
    # Self-check: nobody is created or destroyed, so S + I + R must stay equal to N.
    assert np.allclose(S_ + I_ + R_, N_POP, atol=1e-4)
print("Self-check passed: S + I + R equals the population at every time")

fig, ax = plt.subplots()
for beta, style in ((0.3, "-"), (0.15, "--")):
    S_, I_, R_ = results[beta].y
    t_ = results[beta].t
    if beta == 0.3:
        ax.plot(t_, S_, "tab:blue", linestyle=style, label="Susceptible (beta = 0.3)")
        ax.plot(t_, R_, "tab:green", linestyle=style, label="Recovered (beta = 0.3)")
    ax.plot(t_, I_, "tab:red", linestyle=style, label=f"Infected (beta = {beta})")
ax.set_xlabel("Time (days)")
ax.set_ylabel("Number of people")
ax.set_title("SIR epidemic model solved with solve_ivp")
ax.legend()
ax.grid(True)
plt.savefig(RESULTS_DIR / "Task_18_sir_epidemic.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_18_sir_epidemic.png")

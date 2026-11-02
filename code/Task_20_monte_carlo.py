# Task 20: Random Numbers and Monte Carlo Methods
#
# Part 1 - the lecturer's small example: estimating pi with random points
# Part 2 - the lecturer's server-overload problem (original solution code)
# Part 3 - changing the capacity, the spread, and the number of simulations
# Part 4 - a related real-world case (risk of a project finishing late)

from pathlib import Path

import numpy as np
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example - estimate pi
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - estimating pi ===")
print("PDF arithmetic: 7,850 of 10,000 points inside ->", 4 * 7850 / 10000)

# Throw N random points into the unit square [0,1] x [0,1]. The quarter circle
# x^2 + y^2 <= 1 covers pi/4 of the square, so  pi ~ 4 x (inside / total).
print(f"{'Points N':>10} {'Estimate of pi':>15} {'Error':>10}")
for n_points in (100, 1_000, 10_000, 100_000, 1_000_000):
    rng_pi = np.random.default_rng(1)
    px = rng_pi.random(n_points)
    py = rng_pi.random(n_points)
    inside_count = np.count_nonzero(px ** 2 + py ** 2 <= 1.0)
    estimate = 4 * inside_count / n_points
    print(f"{n_points:>10,} {estimate:>15.5f} {abs(estimate - np.pi):>10.5f}")
assert abs(estimate - np.pi) < 0.01
print("Self-check passed: with a million points the estimate is within 0.01 of pi")

# Picture of the method with 2,000 points
rng_pi = np.random.default_rng(1)
px, py = rng_pi.random(2000), rng_pi.random(2000)
is_inside = px ** 2 + py ** 2 <= 1.0
plt.figure(figsize=(5.5, 5.5))
plt.scatter(px[is_inside], py[is_inside], s=6, color="tab:blue", label="Inside quarter circle")
plt.scatter(px[~is_inside], py[~is_inside], s=6, color="tab:red", label="Outside")
angle = np.linspace(0, np.pi / 2, 100)
plt.plot(np.cos(angle), np.sin(angle), "k-")
plt.gca().set_aspect("equal")
plt.title(f"Monte Carlo estimate of pi = {4 * is_inside.mean():.3f} (2,000 points)")
plt.legend(loc="upper right", fontsize=8)
plt.savefig(RESULTS_DIR / "Task_20_pi_estimate.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_20_pi_estimate.png")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's server-overload problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Probability that a server is overloaded ===")

rng = np.random.default_rng(42)

capacity = 1000.0
mean_demand = 850.0
std_demand = 120.0
N = 100_000

# Random demand scenarios
demand = rng.normal(mean_demand, std_demand, N)

overloaded = demand > capacity
overload_probability = overloaded.mean()

print(f"Estimated overload probability: {overload_probability:.4%}")
print(f"Number of overload cases: {overloaded.sum()} out of {N}")

# Running probability to show convergence
running_probability = np.cumsum(overloaded) / np.arange(1, N + 1)

indices = np.unique(
    np.logspace(1, np.log10(N), 200).astype(int)
) - 1

# Exact answer from the normal distribution, for checking the simulation.
exact_probability = norm.sf(capacity, loc=mean_demand, scale=std_demand)
print(f"Exact probability (normal distribution): {exact_probability:.4%}")
print(f"Simulation error: {abs(overload_probability - exact_probability):.4%}")
assert abs(overload_probability - exact_probability) < 0.005
print("Self-check passed: the simulation agrees with the exact value")

plt.semilogx(
    indices + 1,
    running_probability[indices]
)
plt.axhline(exact_probability, color="red", linestyle="--", label="Exact probability")
plt.xlabel("Number of simulations")
plt.ylabel("Estimated overload probability")
plt.title("Monte Carlo estimate of server-overload risk")
plt.legend()
plt.grid(True)
plt.savefig(RESULTS_DIR / "Task_20_overload_convergence.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_20_overload_convergence.png")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")


def overload_estimate(cap, mean, std, n, seed):
    sample = np.random.default_rng(seed).normal(mean, std, n)
    return np.mean(sample > cap)


# (a) Change the capacity and the demand spread.
print("(a) Capacity and spread (N = 100,000):")
print(f"{'Capacity':>9} {'Std dev':>8} {'Simulated':>10} {'Exact':>8}")
for cap, std in ((1000, 120), (1100, 120), (1000, 150)):
    sim = overload_estimate(cap, 850, std, 100_000, 42)
    exact_p = norm.sf(cap, loc=850, scale=std)
    print(f"{cap:>9} {std:>8} {sim:>10.3%} {exact_p:>8.3%}")

# (b) Change the number of simulations: small N gives noisy answers.
print("\n(b) Number of simulations N (five different random seeds each):")
for n_sim in (100, 1_000, 100_000):
    estimates = [overload_estimate(1000, 850, 120, n_sim, seed) for seed in range(5)]
    print(f"    N = {n_sim:>7,}: " + ", ".join(f"{e:.3%}" for e in estimates)
          + f"   (spread {max(estimates) - min(estimates):.3%})")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - will the project finish on time?
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A software project has three tasks done one after another.
#     Each duration is uncertain, described by (fastest, most likely, slowest) days:
#         Design (5, 7, 12)     Build (10, 14, 25)     Testing (3, 5, 10)
#   * The deadline is 35 days.
#   * Monte Carlo: draw a random duration for each task (triangular distribution),
#     add them, and repeat 100,000 times.
print("\n=== PART 4: Risk of a project finishing late ===")
rng_proj = np.random.default_rng(2024)
N_PROJECT = 100_000
DEADLINE = 35.0

tasks = {"Design": (5, 7, 12), "Build": (10, 14, 25), "Testing": (3, 5, 10)}
total = np.zeros(N_PROJECT)
for name, (fast, likely, slow) in tasks.items():
    total += rng_proj.triangular(fast, likely, slow, N_PROJECT)

planned = sum(likely for _, likely, _ in tasks.values())
p_late = np.mean(total > DEADLINE)
p50, p80, p90, p95 = np.percentile(total, [50, 80, 90, 95])

print(f"Plan using the 'most likely' times: {planned} days")
print(f"Simulated average duration:         {total.mean():.2f} days")
print(f"Shortest / longest in simulation:   {total.min():.1f} / {total.max():.1f} days")
print(f"Probability of finishing after {DEADLINE:.0f} days: {p_late:.2%}")
print(f"Duration needed for 50% / 80% / 90% / 95% confidence: "
      f"{p50:.1f} / {p80:.1f} / {p90:.1f} / {p95:.1f} days")
expected_mean = sum((a + b + c) / 3 for a, b, c in tasks.values())   # exact mean of triangular
assert abs(total.mean() - expected_mean) < 0.1
print(f"Self-check passed: simulated mean is close to the exact mean {expected_mean:.2f} days")

# Parameter change: the build team reduces its worst case from 25 to 18 days.
faster = np.zeros(N_PROJECT)
rng_proj2 = np.random.default_rng(2024)
for name, (fast, likely, slow) in tasks.items():
    if name == "Build":
        slow = 18
    faster += rng_proj2.triangular(fast, likely, slow, N_PROJECT)
print(f"\nIf Build's slowest case drops from 25 to 18 days: "
      f"P(late) {p_late:.2%} -> {np.mean(faster > DEADLINE):.2%}, "
      f"90% confidence {p90:.1f} -> {np.percentile(faster, 90):.1f} days")

plt.figure()
plt.hist(total, bins=60, color="tab:blue", alpha=0.75)
plt.axvline(DEADLINE, color="red", linestyle="--", label=f"Deadline = {DEADLINE:.0f} days")
plt.axvline(p90, color="green", linestyle=":", label=f"90% confidence = {p90:.1f} days")
plt.xlabel("Total project duration (days)")
plt.ylabel("Number of simulations")
plt.title("Monte Carlo simulation of project duration")
plt.legend()
plt.savefig(RESULTS_DIR / "Task_20_project_duration.png", dpi=150, bbox_inches="tight")
plt.close()
print("Graph saved: results/Task_20_project_duration.png")

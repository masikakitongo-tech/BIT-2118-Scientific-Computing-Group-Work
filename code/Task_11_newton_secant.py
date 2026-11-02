# Task 11: Root Finding - Newton-Raphson and Secant Methods
#
# Part 1 - the lecturer's small example: Newton's method for f(x) = x^2 - 2
# Part 2 - the lecturer's financial problem: internal rate of return (IRR)
# Part 3 - changing the starting guess and a cash flow
# Part 4 - a related real-world case (the true interest rate of an instalment plan)

from scipy.optimize import root_scalar

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - Newton for f(x) = x^2 - 2 ===")
# Newton-Raphson:  x_new = x - f(x) / f'(x)      with f(x) = x^2 - 2, f'(x) = 2x
x = 1.5                                  # starting guess x0
print(f"x0 = {x:.10f}")
for step in range(1, 5):
    x = x - (x ** 2 - 2) / (2 * x)
    print(f"x{step} = {x:.10f}   error = {abs(x - 2 ** 0.5):.2e}")
assert abs(x - 2 ** 0.5) < 1e-12
print("Self-check passed: x1 = 1.4167 as in the PDF, and the method reaches sqrt(2)")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's financial problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Internal rate of return (IRR) ===")

# Initial investment followed by annual cash inflows
cash_flows = [-10000, 3000, 3500, 4000, 2500]

def npv(rate):
    return sum(
        cf / (1 + rate)**t
        for t, cf in enumerate(cash_flows)
    )

def d_npv(rate):
    return sum(
        -t * cf / (1 + rate)**(t + 1)
        for t, cf in enumerate(cash_flows)
        if t > 0
    )

newton = root_scalar(
    npv,
    fprime=d_npv,
    x0=0.10,
    method="newton",
    xtol=1e-12
)

secant = root_scalar(
    npv,
    x0=0.05,
    x1=0.20,
    method="secant",
    xtol=1e-12
)

print(f"IRR using Newton-Raphson: {newton.root:.6%}")
print(f"IRR using Secant method:  {secant.root:.6%}")
print(f"NPV at Newton solution:   {npv(newton.root):.6f}")
print("Iterations: Newton =", newton.iterations, "| Secant =", secant.iterations)
assert abs(newton.root - secant.root) < 1e-9
print("Self-check passed: both methods agree and NPV is about 0")

# ---------------------------------------------------------------------------
# PART 3: Parameter changes
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")


def find_irr(flows, x0=0.10):
    """Return (newton_result, secant_result) for a list of cash flows."""
    def f(rate):
        return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))

    def df(rate):
        return sum(-t * cf / (1 + rate) ** (t + 1)
                   for t, cf in enumerate(flows) if t > 0)

    n = root_scalar(f, fprime=df, x0=x0, method="newton", xtol=1e-12)
    s = root_scalar(f, x0=x0 / 2, x1=x0 * 2, method="secant", xtol=1e-12)
    return n, s


# (a) Different starting guesses.
print("(a) Different starting guesses (Newton, secant uses x0/2 and 2*x0):")
print(f"{'x0':>6} {'Newton IRR':>12} {'Newton iter':>12} {'Secant IRR':>12} {'Secant iter':>12}")
for guess in (0.01, 0.10, 0.50):
    n, s = find_irr(cash_flows, x0=guess)
    print(f"{guess:>6} {n.root:>12.6%} {n.iterations:>12} {s.root:>12.6%} {s.iterations:>12}")

# (b) Change the last cash inflow from 2500 to 3500.
better_flows = [-10000, 3000, 3500, 4000, 3500]
n_better, _ = find_irr(better_flows)
print(f"\n(b) Last inflow changed from 2500 to 3500:")
print(f"    IRR before: {newton.root:.4%}   IRR after: {n_better.root:.4%}")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - the true interest rate of an instalment plan
# ---------------------------------------------------------------------------
# Assumptions (simulated):
#   * A shop sells a laptop for KES 50,000 cash, or 12 monthly instalments of
#     KES 4,600. The shop never says what interest rate that is.
#   * The monthly rate r is the one that makes the present value of the 12
#     instalments equal to the cash price, i.e. NPV(r) = 0 for the cash flows
#     [-50000, +4600, +4600, ... (12 times)].
print("\n=== PART 4: True interest rate of an instalment plan ===")
cash_price = 50_000
instalment = 4_600
months = 12
plan = [-cash_price] + [instalment] * months

n_plan, s_plan = find_irr(plan, x0=0.02)
monthly = n_plan.root
yearly_nominal = 12 * monthly
yearly_effective = (1 + monthly) ** 12 - 1
total_paid = instalment * months

print(f"Monthly interest rate (Newton): {monthly:.4%}   (Secant: {s_plan.root:.4%})")
print(f"Nominal annual rate (12 x monthly): {yearly_nominal:.2%}")
print(f"Effective annual rate (compounded): {yearly_effective:.2%}")
print(f"Total paid: KES {total_paid:,} | extra over cash price: KES {total_paid - cash_price:,}")

# Check the answer: discounting the instalments at this rate gives the cash price.
present_value = sum(instalment / (1 + monthly) ** t for t in range(1, months + 1))
print(f"Present value of the instalments at that rate: KES {present_value:,.2f}")
assert abs(present_value - cash_price) < 1e-4
print("Self-check passed: the discounted instalments equal the cash price")

# Parameter change: a cheaper instalment of KES 4,400 lowers the rate.
cheaper = [-cash_price] + [4_400] * months
n_cheaper, _ = find_irr(cheaper, x0=0.02)
print(f"\nIf the instalment were KES 4,400: monthly rate = {n_cheaper.root:.4%}, "
      f"effective annual rate = {(1 + n_cheaper.root) ** 12 - 1:.2%}")

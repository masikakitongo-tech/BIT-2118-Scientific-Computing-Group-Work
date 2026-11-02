# Task 3: Mathematical Functions and Vectorization
#
# Part 1 - the lecturer's small example   (sin of [0, pi/2, pi])
# Part 2 - the lecturer's network-latency problem (original solution code)
# Part 3 - changing an input (number of readings) and observing the timings
# Part 4 - a related real-world case (brightening a 1000 x 1000 image)
#
# NOTE: timing results differ a little every time the program is run,
# because they depend on how busy the computer is.

import numpy as np
import timeit

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example from the PDF ===")
x_small = np.array([0, np.pi / 2, np.pi])
print("x           =", x_small)
print("sin(x)      =", np.sin(x_small), "  (approximately [0, 1, 0])")

# Identity from the PDF: sin^2(x) + cos^2(x) = 1 for EVERY x.
# We test it on one million values with a single vectorized expression.
x_big = np.linspace(0, 100, 1_000_000)
y = np.sin(x_big) ** 2 + np.cos(x_big) ** 2
print("sin^2 + cos^2 on 1,000,000 values: smallest =", y.min(),
      " largest =", y.max())
print("Largest distance from 1:", np.max(np.abs(y - 1)))
assert np.allclose(y, 1.0), "The identity should hold for every value"
print("Self-check passed: the identity holds for all 1,000,000 values")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's network-latency problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Network latency - loop versus vectorization ===")

# Generate simulated network latency readings in milliseconds
rng = np.random.default_rng(42)
latency_ms = rng.uniform(5, 250, 1_000_000)

# Method 1: Using a normal Python loop
def loop_version():
    squared = []

    for value in latency_ms:
        seconds = value / 1000.0
        squared.append(seconds ** 2)

    return squared

# Method 2: Using NumPy vectorization
def vectorized_version():
    seconds = latency_ms / 1000.0
    return seconds ** 2

# Measure execution time
loop_time = timeit.timeit(loop_version, number=1)

vector_time = timeit.timeit(
    vectorized_version, number=3
) / 3

# Obtain the calculated results
result = vectorized_version()

# Display results
print("First five squared latency values:", result[:5])

print(f"Loop time: {loop_time:.4f} seconds")
print(f"Vectorized time: {vector_time:.4f} seconds")

print(f"Approximate speed-up: {loop_time/vector_time:.1f}x")

# Self-check: both methods must give the same numbers
assert np.allclose(loop_version(), result), "Loop and vectorized results differ"
print("Self-check passed: loop and vectorized results are identical")

# ---------------------------------------------------------------------------
# PART 3: Parameter change - fewer readings
# ---------------------------------------------------------------------------
# We repeat the same experiment with 1,000,000 / 500,000 / 100,000 readings.
print("\n=== PART 3: Parameter change - number of readings ===")

def compare_speed(n_readings):
    """Time the loop and the vectorized method on n_readings latencies."""
    data = np.random.default_rng(42).uniform(5, 250, n_readings)

    def loop():
        out = []
        for value in data:
            out.append((value / 1000.0) ** 2)
        return out

    def vec():
        return (data / 1000.0) ** 2

    t_loop = timeit.timeit(loop, number=1)
    t_vec = timeit.timeit(vec, number=3) / 3
    return t_loop, t_vec

print(f"{'Readings':>10} {'Loop (s)':>10} {'Vectorized (s)':>15} {'Speed-up':>10}")
for n in (1_000_000, 500_000, 100_000):
    t_loop, t_vec = compare_speed(n)
    print(f"{n:>10,} {t_loop:>10.4f} {t_vec:>15.5f} {t_loop / t_vec:>9.1f}x")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - brightening a photograph (gamma correction)
# ---------------------------------------------------------------------------
# Assumptions:
#   * The image is greyscale, 1000 x 1000 = 1,000,000 pixels.
#   * Each pixel is a brightness from 0 (black) to 255 (white).
#   * The pixel values are SIMULATED random numbers (a dark photo, 0-120).
#   * Gamma correction  new = 255 * (old / 255) ** gamma  with gamma = 0.6
#     makes dark images brighter (gamma < 1 brightens, gamma > 1 darkens).
print("\n=== PART 4: Image brightening (gamma correction) ===")
GAMMA = 0.6
image = np.random.default_rng(7).integers(0, 121, size=(1000, 1000))

def brighten_loop(img):
    """Process one pixel at a time with a Python loop."""
    out = []
    for pixel in img.ravel():             # ravel() = flatten to 1-D
        out.append(255 * (pixel / 255) ** GAMMA)
    return out

def brighten_vectorized(img):
    """Process every pixel with a single NumPy expression."""
    return 255 * (img / 255) ** GAMMA

t_loop = timeit.timeit(lambda: brighten_loop(image), number=1)
t_vec = timeit.timeit(lambda: brighten_vectorized(image), number=3) / 3
bright = brighten_vectorized(image)

assert np.allclose(np.array(brighten_loop(image)).reshape(image.shape), bright)
print("Self-check passed: loop and vectorized images are identical")

print(f"Mean brightness before: {image.mean():.1f} (scale 0-255)")
print(f"Mean brightness after:  {bright.mean():.1f} (scale 0-255)")
print(f"Brightest pixel before: {image.max()}   after: {bright.max():.1f}")
print(f"Loop time: {t_loop:.4f} s | Vectorized time: {t_vec:.4f} s "
      f"| Speed-up: {t_loop / t_vec:.1f}x")

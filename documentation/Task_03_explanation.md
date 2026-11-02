# Task 3: Mathematical Functions and Vectorization

Program: `code/Task_03_vectorization.py` | Saved output: `results/Task_03_output.txt`

## 1. Objective
To understand vectorization and compare normal Python loops with NumPy operations.

## 2. Mathematical concept (in simple words)
**Vectorization** means applying a mathematical operation to many values at the same time. For example, `sin²(x) + cos²(x) = 1` for every `x`. Instead of looping through x₁, x₂, …, xₙ, NumPy evaluates the whole array in one expression, and the code is shorter and usually much faster.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | x = [0, π/2, π]; then one million values of x between 0 and 100 |
| 2 (PDF problem) | One million simulated network latencies, uniformly random between 5 and 250 ms (`np.random.default_rng(42)` makes them repeatable) |
| 3 (parameter change) | The number of readings changed: 1,000,000 → 500,000 → 100,000 |
| 4 (my real-world case) | A simulated 1000 × 1000 greyscale image (1,000,000 pixels with brightness 0–120) and gamma = 0.6 |

## 4. Mathematical operations
- `sin(x)` and `cos(x)` on whole arrays, and the identity sin²x + cos²x = 1.
- Unit conversion: seconds = milliseconds ÷ 1000.
- Squaring: seconds².
- Gamma correction (Part 4): new brightness = 255 × (old ÷ 255)^0.6.
- Timing with `timeit.timeit()`.

## 5. How the program works
Two methods are compared:
1. **Loop version:** a normal Python `for` loop handles one reading at a time and appends the answer to a list.
2. **Vectorized version:** `(latency_ms / 1000.0) ** 2` handles all one million readings in one line.

`timeit` measures how long each takes. An `assert np.allclose(...)` self-check confirms that both methods give identical numbers.

## 6. Output and what it means
**Part 1 – PDF example**
```
sin(x) = [0.0000000e+00 1.0000000e+00 1.2246468e-16]   (approximately [0, 1, 0])
Largest distance from 1: 2.220446049250313e-16
```
*In words:* sin(π) should be exactly 0, but the computer gives 1.2×10⁻¹⁶ because π cannot be stored exactly (this is the floating-point error from Task 4). For the identity, every one of the one million answers is 1 to within 0.0000000000000002.

**Part 2 – latency problem** (one run; your timings will differ a little)
```
First five squared latency values: [0.03787665 0.01266192 0.04637842 0.03092504 0.00078812]
Loop time: 0.2247 seconds
Vectorized time: 0.0042 seconds
Approximate speed-up: 54.0x
```
*In words:* the first latency was about 194.6 ms = 0.1946 s, and 0.1946² = 0.0379, which matches the first value. NumPy did the same work about 50 times faster than the loop.

## 7. Parameter change: number of readings
| Readings | Loop (s) | Vectorized (s) | Speed-up |
|---|---|---|---|
| 1,000,000 | 0.1752 | 0.00478 | 36.7× |
| 500,000 | 0.0900 | 0.00249 | 36.1× |
| 100,000 | 0.0151 | 0.00063 | 24.0× |

*Explanation:* halving the data from 1,000,000 to 500,000 readings roughly halves both times (0.175 → 0.090 s for the loop). The work grows in proportion to the amount of data. The vectorized method stays much faster in every case. For very small arrays the advantage is smaller, because the fixed set-up cost matters more. (The exact numbers change every run.)

## 8. Related real-world case: brightening a dark photograph (image processing)
**Assumptions**
- The image is greyscale and 1000 × 1000 = 1,000,000 pixels; each pixel is a brightness from 0 (black) to 255 (white).
- The pixels are **simulated** random values from 0 to 120, representing an under-exposed photo.
- Gamma correction `new = 255 × (old/255)^0.6` brightens dark images (gamma < 1 brightens; gamma > 1 darkens).

**Output**
```
Mean brightness before: 60.0 (scale 0-255)
Mean brightness after:  101.2 (scale 0-255)
Brightest pixel before: 120   after: 162.2
Loop time: 0.2404 s | Vectorized time: 0.0241 s | Speed-up: 10.0x
```
**Interpretation:** the average brightness rose from 60 to about 101, so the picture is clearly brighter. The vectorized code processed the million pixels about 10 times faster than the loop. Image and video software repeats this kind of calculation on millions of pixels, so vectorization is essential.

## 9. Conclusion
Vectorization simplifies numerical calculations and can improve performance when working with large datasets. The loop and vectorized results are identical, so vectorization saves time without changing the answer.

**Key points to explain to the lecturer**
- A loop works on one value at a time; NumPy works on the whole array.
- The speed-up was between about 10× and 55× in my runs; it changes from run to run.
- Doubling the data roughly doubles the time, for both methods.

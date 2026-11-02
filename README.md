# BIT 2118 Scientific Computing – Group Work (Tasks 2–20)

Individual GitHub submission for the BIT 2118 *Scientific Computing* group work.
Every task from the lecturer's assignment sheet is implemented in Python (NumPy, SciPy and Matplotlib), run and tested, and explained in plain English.

| | |
|---|---|
| **Student name** | *Masika kitongo Jeremiah* |
| **Registration number** | *BSCCS/2024/55350* |
| **Group** | *Group* |

---

## 1. What this project contains

For **each task (2 to 20)** the repository has:

1. a **Python program** in `code/` that contains
   - **Part 1** – the small worked example from the lecturer's PDF,
   - **Part 2** – the lecturer's real-world problem, with the original solution code kept unchanged,
   - **Part 3** – a **parameter change** (one or more inputs modified) to see how the result changes,
   - **Part 4** – a **different but related real-world case**, with its own assumptions, input data, output and interpretation;
2. an **explanation document** in `documentation/` that identifies the input values and the mathematical operations, explains the output in simple words, interprets the graphs, records the parameter-change results, and documents the related real-world case;
3. the **saved program output** and **graphs** in `results/`.

This follows instructions B–E of the assignment sheet.

## 2. Tasks

| Task | Topic | Program (`code/`) | Explanation (`documentation/`) | Graphs (`results/`) |
|---|---|---|---|---|
| 2 | NumPy arrays and numerical computation | `Task_02_numpy_arrays.py` | `Task_02_explanation.md` | – |
| 3 | Mathematical functions and vectorization | `Task_03_vectorization.py` | `Task_03_explanation.md` | – |
| 4 | Floating-point arithmetic and numerical errors | `Task_04_numerical_errors.py` | `Task_04_explanation.md` | – |
| 5 | Matrix algebra and matrix operations | `Task_05_matrix_algebra.py` | `Task_05_explanation.md` | `Task_05_matrix_transformations.png` |
| 6 | Solution of systems of linear equations | `Task_06_linear_systems.py` | `Task_06_explanation.md` | – |
| 7 | Gaussian elimination and LU decomposition | `Task_07_gaussian_lu.py` | `Task_07_explanation.md` | – |
| 8 | Iterative methods for linear systems | `Task_08_iterative_linear.py` | `Task_08_explanation.md` | `Task_08_convergence.png`, `Task_08_plate_temperature.png` |
| 9 | Eigenvalues and eigenvectors | `Task_09_eigenvalues.py` | `Task_09_explanation.md` | – |
| 10 | Root finding: bisection and fixed-point | `Task_10_bisection_fixed_point.py` | `Task_10_explanation.md` | `Task_10_equilibrium_temperature.png`, `Task_10_break_even.png` |
| 11 | Root finding: Newton-Raphson and secant | `Task_11_newton_secant.py` | `Task_11_explanation.md` | – |
| 12 | Polynomial and nonlinear equation solving | `Task_12_nonlinear_equations.py` | `Task_12_explanation.md` | – |
| 13 | Interpolation | `Task_13_interpolation.py` | `Task_13_explanation.md` | `Task_13_temperature_interpolation.png`, `Task_13_sensor_calibration.png` |
| 14 | Curve fitting and approximation | `Task_14_curve_fitting.py` | `Task_14_explanation.md` | `Task_14_response_time_fit.png`, `Task_14_residuals.png`, `Task_14_user_growth.png` |
| 15 | Numerical differentiation | `Task_15_numerical_differentiation.py` | `Task_15_explanation.md` | `Task_15_gps_speed.png`, `Task_15_step_size_error.png`, `Task_15_car_acceleration.png` |
| 16 | Numerical integration | `Task_16_numerical_integration.py` | `Task_16_explanation.md` | `Task_16_energy_area.png` |
| 17 | ODEs: Euler method | `Task_17_euler_ode.py` | `Task_17_explanation.md` | `Task_17_cooling.png`, `Task_17_step_sizes.png`, `Task_17_logistic_growth.png` |
| 18 | Numerical solution of ODEs using SciPy | `Task_18_scipy_ode.py` | `Task_18_explanation.md` | `Task_18_rc_circuit.png`, `Task_18_sir_epidemic.png` |
| 19 | Numerical optimization | `Task_19_optimization.py` | `Task_19_explanation.md` | `Task_19_production_plan.png` |
| 20 | Random numbers and Monte Carlo methods | `Task_20_monte_carlo.py` | `Task_20_explanation.md` | `Task_20_pi_estimate.png`, `Task_20_overload_convergence.png`, `Task_20_project_duration.png` |

The text output of each program is saved as `results/Task_XX_output.txt`.

## 3. Folder structure

```
BIT-2118-Scientific-Computing-Group-Work/
├── README.md                  <- this file
├── requirements.txt           <- libraries and versions used
├── run_all.py                 <- runs every task, saves outputs, checks for errors
├── check_libraries.py         <- quick check that NumPy, SciPy and Matplotlib are installed
├── test.py                    <- first "Hello" test of the Python setup
├── code/                      <- Task_02 ... Task_20 Python programs
├── documentation/             <- Task_02 ... Task_20 explanation documents
└── results/                   <- saved outputs (.txt) and graphs (.png)
```

## 4. Setup

**Requirements:** Python 3.14.5, NumPy 2.5.1, SciPy 1.18.0 and Matplotlib 3.11.2 (these are the versions the programs were written and tested with).

1. Install Python from <https://www.python.org/downloads/> if it is not installed.
2. Open a terminal in the project folder.
3. Install the libraries:

```bash
pip install -r requirements.txt
```

4. Check that everything is installed:

```bash
python check_libraries.py
```

You should see the three version numbers and the message *"All scientific computing libraries are working!"*.

## 5. How to run

**Run one task** (for example Task 6):

```bash
python code/Task_06_linear_systems.py
```

The program prints its results in the terminal. Tasks that draw graphs save them as PNG files in `results/` (no window opens), so open the picture files to see the graphs.

**Run everything at once** and check that every task works:

```bash
python run_all.py
```

This runs Tasks 2–20, saves each output as `results/Task_XX_output.txt`, and prints a PASS/FAIL table. To run only some tasks, list their numbers:

```bash
python run_all.py 5 6 7
```

## 6. How the work was tested

- **Every task was actually run** (all 19 programs pass in `run_all.py`, including when started from a different folder), and the numbers in the explanation documents were copied from those runs.
- Each program contains **self-checks** (`assert` statements) that compare results with a known answer, for example with the exact algebraic solution, with the PDF's stated result, or with a second method. If a check fails, the program stops with an error.
- `run_all.py` also confirms that the graphs that every graph-producing task should create exist in `results/`.

## 7. Notes

- **The lecturer's code is kept.** In every program, Part 2 contains the lecturer's solution code from the assignment sheet. Only two small changes were made: `plt.show()` was replaced by `plt.savefig(...)` so that graphs are saved into `results/`, and long print statements that were broken across two lines in the PDF were written on one line.
- **Data in the real-world cases are simulated.** All numbers in Part 4 of each task (sensor readings, prices, populations and so on) are invented for illustration, and the assumptions are written at the top of each Part 4 and in its documentation.
- **Timings vary.** Tasks 3 and 7 measure how long calculations take, so those numbers change a little each time the program is run.
- **Random numbers are repeatable.** Programs that use random numbers fix the random seed, so the same results appear each time (apart from the timings).
- **File names** follow the assignment sheet (for example `Task_05_matrix_algebra.py`).

## 8. Submission

The assignment states that the group discusses the work together but each student submits an **individual GitHub repository**, and the repository link and documentation are uploaded on VLMS. A step-by-step guide for creating and publishing this repository is in `documentation/GitHub_Submission_Guide.md`.

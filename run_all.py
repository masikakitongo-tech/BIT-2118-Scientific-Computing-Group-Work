"""Run every task program, save its output, and check that it worked.

Usage (from the project folder):
    python run_all.py            # run Tasks 2-20
    python run_all.py 5 6 7      # run only Tasks 5, 6 and 7

For each task this script:
  1. runs code/Task_XX_*.py in a separate Python process,
  2. saves everything the program printed to results/Task_XX_output.txt,
  3. checks that the program finished without an error, and
  4. checks that the graphs the task should create exist in results/.

The graphs are saved as PNG files by the programs themselves, so no window
ever pops up and the whole project can be tested automatically.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
CODE_DIR = PROJECT / "code"
RESULTS_DIR = PROJECT / "results"

# Tasks that must produce at least one PNG graph (the PDF asks for a graph
# in Tasks 8, 10, 13, 14, 15, 17, 18 and 20; Tasks 5, 16 and 19 also draw one).
TASKS_WITH_GRAPHS = {5, 8, 10, 13, 14, 15, 16, 17, 18, 19, 20}


def find_scripts(selected):
    """Return {task_number: path} for the task programs in the code folder."""
    scripts = {}
    for path in sorted(CODE_DIR.glob("Task_*.py")):
        number = int(path.stem.split("_")[1])
        if not selected or number in selected:
            scripts[number] = path
    return scripts


def run_task(number, path):
    """Run one task program. Return (passed, seconds, notes)."""
    env = dict(os.environ)
    env["MPLBACKEND"] = "Agg"            # never open graph windows
    env["PYTHONIOENCODING"] = "utf-8"    # same text encoding on every computer

    start = time.perf_counter()
    done = subprocess.run(
        [sys.executable, "-I", str(path)],
        capture_output=True, text=True, encoding="utf-8",
        cwd=PROJECT, env=env, timeout=600,
    )
    seconds = time.perf_counter() - start

    # Save what the program printed (plus any error text) for the report.
    output_file = RESULTS_DIR / f"Task_{number:02d}_output.txt"
    text = done.stdout
    if done.stderr:
        text += "\n--- messages on the error channel ---\n" + done.stderr
    output_file.write_text(text, encoding="utf-8")

    notes = []
    passed = done.returncode == 0
    if not passed:
        notes.append(f"exit code {done.returncode}")
        notes.append(done.stderr.strip().splitlines()[-1] if done.stderr.strip() else "")

    if number in TASKS_WITH_GRAPHS:
        graphs = sorted(RESULTS_DIR.glob(f"Task_{number:02d}_*.png"))
        if graphs:
            notes.append(f"{len(graphs)} graph(s)")
        else:
            passed = False
            notes.append("MISSING graph")

    return passed, seconds, ", ".join(n for n in notes if n)


def main():
    selected = {int(a) for a in sys.argv[1:] if a.isdigit()}
    RESULTS_DIR.mkdir(exist_ok=True)
    scripts = find_scripts(selected)
    if not scripts:
        print("No matching task programs found in", CODE_DIR)
        return 1

    print(f"Running {len(scripts)} task program(s) with {sys.executable}\n")
    print(f"{'Task':<6}{'Result':<8}{'Time':>8}  Notes")
    failures = 0
    for number, path in scripts.items():
        passed, seconds, notes = run_task(number, path)
        failures += 0 if passed else 1
        print(f"{number:<6}{'PASS' if passed else 'FAIL':<8}{seconds:>7.1f}s  {notes}")

    print()
    if failures:
        print(f"{failures} task(s) FAILED. Open results/Task_XX_output.txt for details.")
        return 1
    print("All selected tasks ran successfully. Outputs saved in results/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Task 5: Matrix Algebra and Matrix Operations
#
# Part 1 - the lecturer's small example   (A x with A=[[1,2],[3,4]], x=[5,6])
# Part 2 - the lecturer's graphics problem (rotate and scale a square)
# Part 3 - changing the angle and scale factors
# Part 4 - a related real-world case (a robot converting sensor points to a map)

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")                    # save graphs to files, no window needed
import matplotlib.pyplot as plt

# Graphs are saved in the "results" folder next to the "code" folder.
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example from the PDF ===")
A_small = np.array([[1, 2],
                    [3, 4]])
x_small = np.array([5, 6])

# Matrix-vector product: row 1 -> 1*5 + 2*6 = 17, row 2 -> 3*5 + 4*6 = 39
print("A @ x =", A_small @ x_small, "  (PDF: [17, 39])")
assert np.array_equal(A_small @ x_small, [17, 39])

B_small = np.array([[0, 1],
                    [1, 0]])
print("Matrix addition A + B:\n", A_small + B_small)
print("Matrix multiplication A @ B:\n", A_small @ B_small)
print("Determinant of A:", np.linalg.det(A_small), " (1*4 - 2*3 = -2)")

A_inverse = np.linalg.inv(A_small)       # exists because the determinant is not 0
print("Inverse of A:\n", A_inverse)
print("A @ inverse(A):\n", np.round(A_small @ A_inverse, 10))
assert np.allclose(A_small @ A_inverse, np.eye(2))
print("Self-check passed: A times its inverse is the identity matrix")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's graphics problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Rotate and scale a square ===")

# Four corners of a square: each row is [x, y]
points = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0]
])

angle = np.deg2rad(45)

rotation = np.array([
    [np.cos(angle), -np.sin(angle)],
    [np.sin(angle),  np.cos(angle)]
])

scale = np.array([
    [2.0, 0.0],
    [0.0, 1.5]
])

# Combined transformation
transformation = rotation @ scale

# Row-vector form requires multiplication by transpose
transformed_points = points @ transformation.T

print("Original points:\n", points)
print("Transformation matrix:\n", transformation)
print("Transformed points:\n", transformed_points)
print("Determinant:", np.linalg.det(transformation))


def polygon_area(p):
    """Area of a polygon from its corners (shoelace formula)."""
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


print("Area of original square:   ", polygon_area(points))
print("Area of transformed shape: ", polygon_area(transformed_points))
# The determinant tells us how much the shape's area is multiplied.
assert np.isclose(polygon_area(transformed_points), abs(np.linalg.det(transformation)))
print("Self-check passed: new area = |determinant| x old area")

# ---------------------------------------------------------------------------
# PART 3: Parameter change - different angle and scale factors
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter changes ===")


def make_transformation(angle_degrees, scale_x, scale_y):
    """Return (rotation @ scale) for the given angle and scale factors."""
    a = np.deg2rad(angle_degrees)
    rot = np.array([[np.cos(a), -np.sin(a)],
                    [np.sin(a),  np.cos(a)]])
    sc = np.array([[scale_x, 0.0],
                   [0.0, scale_y]])
    return rot @ sc


print(f"{'Angle':>6} {'Scale x':>8} {'Scale y':>8} {'Determinant':>12} "
      f"{'New area':>9}  Corner (1,1) moves to")
for ang, sx, sy in [(45, 2.0, 1.5), (90, 2.0, 1.5), (45, 3.0, 1.5), (0, 2.0, 1.5)]:
    T = make_transformation(ang, sx, sy)
    moved = points @ T.T
    print(f"{ang:>6} {sx:>8} {sy:>8} {np.linalg.det(T):>12.3f} "
          f"{polygon_area(moved):>9.3f}  {np.round(moved[2], 3)}")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - a robot builds a map
# ---------------------------------------------------------------------------
# Assumptions:
#   * A small robot stands at (2 m, 1 m) in the room, facing 30 degrees
#     anticlockwise from the room's x-axis.
#   * Its distance sensor reports four obstacles as [forward, left] distances
#     in the robot's OWN frame (metres). The numbers are simulated.
#   * To draw a room map we must convert them to the room's frame:
#         world point = rotation (matrix multiplication) + robot position (addition)
print("\n=== PART 4: Robot sensor points -> room map ===")
robot_position = np.array([2.0, 1.0])
heading = np.deg2rad(30)

obstacles_robot = np.array([
    [1.0,  0.0],
    [2.0,  0.5],
    [3.0, -1.0],
    [1.5,  1.5]
])

R = np.array([
    [np.cos(heading), -np.sin(heading)],
    [np.sin(heading),  np.cos(heading)]
])

obstacles_world = obstacles_robot @ R.T + robot_position

print("Obstacles in robot frame (m):\n", obstacles_robot)
print("Obstacles in room frame (m):\n", np.round(obstacles_world, 3))

# Checks: a rotation matrix keeps distances unchanged, has determinant 1 and
# its inverse is simply its transpose.
dist_before = np.linalg.norm(obstacles_robot, axis=1)
dist_after = np.linalg.norm(obstacles_world - robot_position, axis=1)
print("Distance robot->obstacle before:", np.round(dist_before, 3))
print("Distance robot->obstacle after: ", np.round(dist_after, 3))
print("Determinant of rotation matrix:", round(np.linalg.det(R), 6))
assert np.allclose(dist_before, dist_after)
assert np.allclose(R @ R.T, np.eye(2))

# Convert back to the robot frame to prove the transformation can be undone.
back = (obstacles_world - robot_position) @ R
assert np.allclose(back, obstacles_robot)
print("Self-check passed: distances kept, R x R^T = I, and the map converts back")

# ---------------------------------------------------------------------------
# GRAPH: left = PDF square, right = robot map
# ---------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

closed = lambda p: np.vstack([p, p[0]])          # repeat first corner to close shape
ax1.plot(*closed(points).T, "o-", label="Original square")
ax1.plot(*closed(transformed_points).T, "s-", label="Rotated 45 deg and scaled")
ax1.set_title("Task 5: rotation and scaling of a square")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_aspect("equal")
ax1.grid(True)
ax1.legend()

ax2.scatter(*obstacles_world.T, color="red", label="Obstacles (room frame)")
ax2.scatter(*robot_position, color="blue", s=80, label="Robot")
ax2.arrow(robot_position[0], robot_position[1],
          0.8 * np.cos(heading), 0.8 * np.sin(heading),
          head_width=0.1, color="blue")
for i, (px, py) in enumerate(obstacles_world, start=1):
    ax2.annotate(f"O{i}", (px, py), textcoords="offset points", xytext=(5, 5))
ax2.set_title("Robot sensor points converted to a room map")
ax2.set_xlabel("x (m)")
ax2.set_ylabel("y (m)")
ax2.set_aspect("equal")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig(RESULTS_DIR / "Task_05_matrix_transformations.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nGraph saved: results/Task_05_matrix_transformations.png")

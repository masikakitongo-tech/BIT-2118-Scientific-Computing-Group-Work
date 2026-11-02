# Task 5: Matrix Algebra and Matrix Operations

Program: `code/Task_05_matrix_algebra.py` | Saved output: `results/Task_05_output.txt` | Graph: `results/Task_05_matrix_transformations.png`

## 1. Objective
To use matrices to add, multiply and transform data, and to see how a matrix can rotate and scale a set of 2-D points in a graphics program.

## 2. Mathematical concept (in simple words)
A **matrix** is a table of numbers in rows and columns.
- **Addition** adds matching entries.
- **Multiplication** combines each row of the first matrix with each column of the second: cᵢⱼ = Σ aᵢₖ bₖⱼ.
- The **determinant** is one number that shows whether a square matrix can be reversed (it must not be 0) and how much it multiplies areas.
- The **inverse** A⁻¹ undoes A, so A × A⁻¹ = I (the identity matrix).

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF example) | A = [[1, 2], [3, 4]] and x = [5, 6]; extra matrix B = [[0, 1], [1, 0]] |
| 2 (PDF problem) | The four corners of a unit square; rotation by 45°; scaling by 2.0 (x) and 1.5 (y) |
| 3 (parameter change) | Angles 45°, 90°, 0° and scale factors (2.0, 1.5) and (3.0, 1.5) |
| 4 (my real-world case) | A robot at (2, 1) m facing 30°, and four obstacles measured in the robot's own frame (simulated) |

## 4. Mathematical operations
- Matrix–vector product A·x, matrix addition, matrix multiplication (`@`).
- Determinant (`np.linalg.det`) and inverse (`np.linalg.inv`).
- Rotation matrix [[cos θ, −sin θ], [sin θ, cos θ]] and scaling matrix [[sx, 0], [0, sy]].
- Combined transformation T = Rotation × Scale. Because the points are stored as rows, the program uses `points @ T.T`.
- Polygon area (shoelace formula) to prove that the new area equals |determinant|.

## 5. How the program works
1. Part 1 repeats the PDF example and checks it with `assert`.
2. Part 2 builds the rotation and scaling matrices, multiplies them into one matrix, then transforms all four corners with one matrix multiplication.
3. Part 3 puts this into a function so different angles and scale factors can be tried.
4. Part 4 converts robot sensor points into room coordinates, and checks that distances are unchanged and that the transformation can be reversed.
5. A graph of the square and of the robot map is saved to `results/`.

## 6. Output and what it means
**Part 1 – PDF example**
```
A @ x = [17 39]   (PDF: [17, 39])
Determinant of A: -2.0000000000000004  (1*4 - 2*3 = -2)
Inverse of A: [[-2.   1. ] [ 1.5 -0.5]]
```
*In words:* row 1 gives 1×5 + 2×6 = 17 and row 2 gives 3×5 + 4×6 = 39, exactly as in the PDF. The determinant is −2, which is not 0, so A has an inverse; multiplying A by its inverse gives the identity matrix. (The tiny ‑2.0000000000000004 is the floating-point error from Task 4.)

**Part 2 – rotate and scale a square**
```
Transformed points: (0,0) (1.414,1.414) (0.354,2.475) (-1.061,1.061)
Determinant: 3.000000000000001
Area of original square: 1.0   Area of transformed shape: 3.0
```
*In words:* the square's corner (1, 1) moves to about (0.354, 2.475). The determinant 3 equals 2.0 × 1.5, so the shape's area becomes three times larger. Rotation by itself does not change area; only the scaling does.

## 7. Graph and interpretation
`Task_05_matrix_transformations.png`
- **Left:** the blue unit square sits in the corner at the origin. The orange shape is the same square after being stretched into a 2 × 1.5 rectangle and rotated 45°, so it looks like a tilted rectangle. It is clearly bigger (area 3 instead of 1) but the point (0, 0) stays where it was, because matrix multiplication always keeps the origin fixed.
- **Right:** the red dots are the obstacles on the room map and the blue arrow shows the direction the robot faces.

## 8. Parameter change
| Angle | Scale x | Scale y | Determinant | New area | Corner (1,1) moves to |
|---|---|---|---|---|---|
| 45° (PDF) | 2.0 | 1.5 | 3.000 | 3.000 | (0.354, 2.475) |
| **90°** | 2.0 | 1.5 | 3.000 | 3.000 | (−1.5, 2.0) |
| 45° | **3.0** | 1.5 | **4.500** | 4.500 | (1.061, 3.182) |
| **0°** | 2.0 | 1.5 | 3.000 | 3.000 | (2.0, 1.5) |

*Explanation:* changing the **angle** moves the shape to a different place but keeps the determinant (3) and the area the same. Changing the **scale factor** from 2.0 to 3.0 changes the determinant to 3.0 × 1.5 = 4.5, and the area follows. With angle 0° there is no rotation, so the corner (1, 1) simply becomes (2.0, 1.5).

## 9. Related real-world case: a robot converts sensor points into a room map
**Assumptions**
- The robot is at (2 m, 1 m) and faces 30° anticlockwise from the room's x-axis.
- Its sensor reports four obstacles as [forward, left] distances in the robot's own frame. The values are **simulated**.
- Room position = rotation (matrix multiplication) + robot position (matrix addition).

**Output**
```
Obstacles in room frame (m):
 [[2.866 1.5  ]
  [3.482 2.433]
  [5.098 1.634]
  [2.549 3.049]]
Distance robot->obstacle before: [1.    2.062 3.162 2.121]
Distance robot->obstacle after:  [1.    2.062 3.162 2.121]
Determinant of rotation matrix: 1.0
```
**Interpretation:** every obstacle is now given in room coordinates, so they can be drawn on one map. The distances from the robot to each obstacle are unchanged (rotation does not stretch anything) and the determinant is 1. Converting back to the robot frame returns the original numbers, which the program verifies. Graphics, robotics and navigation systems rely on exactly this idea.

## 10. Conclusion
Matrices provide a compact way to transform many points consistently. One matrix multiplication moved all four corners of the square, and the determinant told us in advance how the area would change.

**Key points to explain to the lecturer**
- `@` is matrix multiplication; `*` would multiply entry by entry (a different operation).
- The determinant of a rotation is 1 (no change in area); for scaling it is the product of the scale factors.
- A matrix with determinant 0 has no inverse.

# Task 9: Eigenvalues and Eigenvectors

Program: `code/Task_09_eigenvalues.py` | Saved output: `results/Task_09_output.txt`

## 1. Objective
To find eigenvalues and eigenvectors of a matrix and use them to measure which nodes of a network are the most influential.

## 2. Mathematical concept (in simple words)
For a square matrix A, an **eigenvector** v is a non-zero vector whose *direction* is not changed by A. It only gets stretched, squashed or flipped: **A v = λ v**. The number λ (lambda) is the **eigenvalue**; it tells how much the vector is stretched. For example, if Av = 3v then applying A triples the length of v.

## 3. Input values
| Part | Input |
|---|---|
| 1 (PDF idea) | A = [[2, 1], [1, 2]] and v = [1, 1] |
| 2 (PDF problem) | The adjacency matrix of a 4-node network: A–B, A–C, B–C, B–D, C–D |
| 3 (parameter change) | One extra link, A–D |
| 4 (my real-world case) | Four web pages with links A→B, A→C, B→C, C→A, D→C and a damping factor 0.85 |

## 4. Mathematical operations
- `np.linalg.eig(A)` returns all eigenvalues and eigenvectors.
- The **dominant** eigenvalue is the largest one; its eigenvector gives the importance of each node. The vector is made positive and scaled to sum to 1 (`centrality = v / v.sum()`).
- Verification: the size of A·v − λ·v should be about 0.
- Part 4 also uses **power iteration**: repeatedly multiplying a starting vector by the matrix.

## 5. How the program works
The adjacency matrix has a 1 where two nodes are connected. A node is important if it is connected to other important nodes, and this "importance of neighbours" idea is exactly what the dominant eigenvector measures.

## 6. Output and what it means
**Part 1 – small example:** the eigenvalues of [[2, 1], [1, 2]] are 3 and 1. Multiplying [1, 1] by A gives [3, 3] = 3 × [1, 1], so [1, 1] is an eigenvector with eigenvalue 3. (The program prints the vectors scaled to length 1, i.e. ±0.7071.)

**Part 2 – network influence**
```
Dominant eigenvalue: 2.5615528128088276
Eigenvector-based importance:
A: 0.2192
B: 0.2808
C: 0.2808
D: 0.2192
Verification error: 2.69e-15
```
*In words:* nodes **B and C** are the most influential (28.1% each) because each is connected to three other nodes, while A and D have only two links each (21.9%). The verification error is about 10⁻¹⁵, so A·v = λ·v holds. The "importance scores" add up to 100%.

## 7. Parameter change: add the link A–D
```
Dominant eigenvalue: 2.5616 -> 3.0000
Node    Before   After
A       0.2192  0.2500
B       0.2808  0.2500
C       0.2808  0.2500
D       0.2192  0.2500
```
*Explanation:* every node is now connected to every other node, so the network is perfectly balanced and all four nodes are equally important (25%). The dominant eigenvalue increases from 2.56 to 3.00, because the network is more strongly connected. Adding a link where it was missing made the weaker nodes more important and the stronger nodes relatively less important.

## 8. Related real-world case: ranking web pages (the PageRank idea)
**Assumptions**
- Four pages A, B, C, D with links A→B, A→C, B→C, C→A, D→C.
- A surfer follows a random link 85% of the time (damping 0.85) and jumps to a random page 15% of the time.
- The rank of each page is the dominant eigenvector (eigenvalue 1) of the "Google matrix", scaled to add up to 1.

**Output**
```
Dominant eigenvalue of the Google matrix: 1.0
Page    Eigenvector  Power iteration
A            0.3725           0.3725
B            0.1958           0.1958
C            0.3941           0.3941
D            0.0375           0.0375
Most important page: C
```
**Interpretation:** **Page C is the most important** (39.4%) because three pages link to it. Page A is nearly as important (37.3%) because C, which is important, links only to A. Page B gets 19.6%, and page D has the lowest rank (3.75%): nobody links to it, so it only receives the 15% random-jump share, 0.15 ÷ 4 = 0.0375. The two methods (eigenvector and power iteration) agree, which confirms the result.

## 9. Conclusion
Eigenvectors reveal structure that is hard to see directly. The dominant eigenvector of a network's matrix ranks its nodes, and this is the idea behind Google's PageRank.

**Key points to explain to the lecturer**
- A v = λ v: the direction of v stays the same, only its length changes by λ.
- The dominant eigenvector ranks the nodes of a network.
- Adding links changes both the eigenvalue and the ranking.

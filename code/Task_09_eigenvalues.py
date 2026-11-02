# Task 9: Eigenvalues and Eigenvectors
#
# Part 1 - the lecturer's small idea: A v = lambda v
# Part 2 - the lecturer's network problem (which node is most influential?)
# Part 3 - changing the network by adding one link
# Part 4 - a related real-world case (ranking web pages, Google PageRank idea)

import numpy as np

# ---------------------------------------------------------------------------
# PART 1: Lecturer's small example
# ---------------------------------------------------------------------------
print("=== PART 1: Small example - A v = lambda v ===")
A_small = np.array([[2., 1.],
                    [1., 2.]])
values, vectors = np.linalg.eig(A_small)
print("Eigenvalues:", values)
print("Eigenvectors (as columns):\n", vectors)

v = np.array([1., 1.])                   # a vector whose direction should not change
print("A @ [1, 1] =", A_small @ v, "= 3 * [1, 1] ->  eigenvalue 3")
assert np.allclose(A_small @ v, 3 * v)
print("Self-check passed: A v = 3 v, so 3 is an eigenvalue with eigenvector [1, 1]")

# ---------------------------------------------------------------------------
# PART 2: Lecturer's network problem (original solution code)
# ---------------------------------------------------------------------------
print("\n=== PART 2: Which network node is most influential? ===")

# Adjacency matrix for a small undirected network.
# Node order: A, B, C, D
A = np.array([
    [0., 1., 1., 0.],
    [1., 0., 1., 1.],
    [1., 1., 0., 1.],
    [0., 1., 1., 0.]
])

eigenvalues, eigenvectors = np.linalg.eig(A)

# Dominant eigenvalue/eigenvector
index = np.argmax(np.real(eigenvalues))
dominant_value = np.real(eigenvalues[index])
dominant_vector = np.abs(np.real(eigenvectors[:, index]))
centrality = dominant_vector / dominant_vector.sum()

nodes = ["A", "B", "C", "D"]

print("Dominant eigenvalue:", dominant_value)
print("Eigenvector-based importance:")
for node, score in zip(nodes, centrality):
    print(f"{node}: {score:.4f}")

# Verify Av = lambda*v
v = np.real(eigenvectors[:, index])
print("Verification error:",
      np.linalg.norm(A @ v - dominant_value * v))

# ---------------------------------------------------------------------------
# PART 3: Parameter change - add a direct link between A and D
# ---------------------------------------------------------------------------
print("\n=== PART 3: Parameter change - add a link A-D ===")
A_new = A.copy()
A_new[0, 3] = A_new[3, 0] = 1.0          # the matrix must stay symmetric

vals_new, vecs_new = np.linalg.eig(A_new)
idx_new = np.argmax(np.real(vals_new))
cent_new = np.abs(np.real(vecs_new[:, idx_new]))
cent_new = cent_new / cent_new.sum()

print(f"Dominant eigenvalue: {dominant_value:.4f} -> {np.real(vals_new[idx_new]):.4f}")
print(f"{'Node':<6}{'Before':>8}{'After':>8}")
for node, before, after in zip(nodes, centrality, cent_new):
    print(f"{node:<6}{before:>8.4f}{after:>8.4f}")

# ---------------------------------------------------------------------------
# PART 4: Related real-world case - ranking web pages (PageRank idea)
# ---------------------------------------------------------------------------
# Assumptions:
#   * Four web pages A, B, C, D. Links: A->B, A->C, B->C, C->A, D->C.
#   * A surfer follows a random link 85% of the time (damping = 0.85) and
#     jumps to a random page 15% of the time.
#   * Page rank = the dominant eigenvector (eigenvalue 1) of the "Google
#     matrix", scaled so the ranks add up to 1.
print("\n=== PART 4: PageRank of four web pages ===")
pages = ["A", "B", "C", "D"]

# Column j describes where a surfer on page j goes next.
# A links to B and C -> half goes to each; B, C and D each link to one page.
link_matrix = np.array([
    [0.0, 0.0, 1.0, 0.0],      # chance of arriving at A
    [0.5, 0.0, 0.0, 0.0],      # chance of arriving at B
    [0.5, 1.0, 0.0, 1.0],      # chance of arriving at C
    [0.0, 0.0, 0.0, 0.0]       # chance of arriving at D (nobody links to D)
])
damping = 0.85
n_pages = len(pages)
google = damping * link_matrix + (1 - damping) / n_pages * np.ones((n_pages, n_pages))

# Method 1: eigenvector of the Google matrix
vals_g, vecs_g = np.linalg.eig(google)
k = np.argmax(np.real(vals_g))
rank_eig = np.abs(np.real(vecs_g[:, k]))
rank_eig = rank_eig / rank_eig.sum()

# Method 2: power iteration (repeatedly multiply a starting guess by the matrix)
rank_power = np.ones(n_pages) / n_pages
for _ in range(200):
    rank_power = google @ rank_power

print("Dominant eigenvalue of the Google matrix:", round(np.real(vals_g[k]), 6))
print(f"{'Page':<6}{'Eigenvector':>13}{'Power iteration':>17}")
for page, r1, r2 in zip(pages, rank_eig, rank_power):
    print(f"{page:<6}{r1:>13.4f}{r2:>17.4f}")
assert np.allclose(rank_eig, rank_power, atol=1e-8)
print("Self-check passed: both methods give the same ranking")
best = pages[int(np.argmax(rank_eig))]
print(f"Most important page: {best}")

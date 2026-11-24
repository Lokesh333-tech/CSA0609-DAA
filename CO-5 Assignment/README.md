# Design and Analysis of Algorithms – Assignment 5 (CO5)

**Assignment title:** Search, Complexity and Approximation Engineering  
**Source:** Uploaded `DAA_Assignment_5_Answers.pdf` (23 pages)  
**Language:** Python 3  
**Software / IDE:** Python 3 and Visual Studio Code  
**Libraries:** Python standard library only

## Objective

Implement the assignment's search and optimisation techniques, record backtracking instrumentation, compare search orders, investigate adversarial inputs, and evaluate approximation methods for Set Cover and Bin Packing.

## Sections implemented

### A1 – Constraint-Aware Search: Graph Colouring
- Models the five-service conflict graph from the assignment.
- Tries two server-group colours in the specified vertex order.
- Records accepted assignments, rejected conflicts, undo operations and the final colouring.
- Final colouring: S1=1, S2=2, S3=2, S4=1, S5=2.

### A2 – Subset-Sum Backtracking and Pruning
- Uses the set `{4, 7, 9, 12, 15}` with target 20.
- Uses include/exclude recursion and suffix sums.
- Demonstrates overshoot pruning and the bound that the remaining values cannot reach the target.
- Includes the assignment's warning that these positive-integer pruning rules are not valid unchanged for negative values.

### B1 – Instrumented Graph Colouring
- Implements the assignment's input-order Version 1 and most-constrained-first Version 2.
- Records search nodes, candidate attempts, rejected branches, backtracks and maximum depth.
- Runs the seven validation/boundary tests and the four comparison graphs (trace graph, hidden K4, wheel W7 and Petersen graph).
- Reproduces the key comparison results: G2 nodes 3,628 vs 16; G3 nodes 316 vs 40.

### B2 – Adversarial Graphs
- Compares a 12-vertex path with a 12-vertex graph containing four lightly constrained pairs followed by a hidden K4.
- Runs both input ordering and heuristic ordering with three colours.
- Confirms the input-order hard graph takes 21,772 nodes, while the heuristic exposes the K4 early.

### B3 – Exact vs Greedy Set Cover
- Runs exact combination search and greedy maximum-new-coverage selection on all three assignment instances.
- Demonstrates the Big/L/R counterexample: exact cover uses 2 centres while greedy uses 3.
- Repeats the fixed-seed scalability experiments for 8/8 through 20/32 zones/centres and reports combinations, greedy evaluations and elapsed times.

### B4 – First-Fit Decreasing Bin Packing
- Implements First-Fit Decreasing (FFD) and a small-input exact branch-and-bound solver.
- Tests the 12-workload sample with capacity 100.
- Tests the assignment's counterexample with capacity 10 and workloads `[7, 5, 4, 4, 3, 3, 2, 2]`; FFD uses 4 servers while the exact optimum is 3.
- Runs reproducible production-scale tests for 1,000, 5,000 and 20,000 workloads.

## How to run in VS Code

1. Open the folder containing `daa_assignment5.py`.
2. Select **Terminal → New Terminal**.
3. Run all sections:

   ```bash
   python daa_assignment5.py
   ```

4. Run an individual section:

   ```bash
   python daa_assignment5.py --task B1
   ```

   Valid section names: `A1`, `A2`, `B1`, `B2`, `B3`, `B4`.

The combined terminal screenshot and individual section screenshots are included in this package.

## Result

The complete script executed successfully and printed `ASSIGNMENT 5 EXECUTION COMPLETED`. All embedded validation assertions passed, including graph-colouring boundary cases, the 21,772-node B2 adversarial case, the Set Cover greedy counterexample, and the FFD 4-versus-3 server counterexample.

## Notes

- The implementation follows the problem definitions, graphs, sets, capacities and test data stated in the supplied assignment.
- Runtime measurements are environment-dependent; fixed random seeds make the generated workloads and instances reproducible.
- The exact Bin Packing solver is intended only for small validation inputs. The 20,000-workload production-scale test uses FFD.

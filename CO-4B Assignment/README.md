# Design and Analysis of Algorithms – Assignment 4B

**Source:** Uploaded `DAA_Assignment_4B.pdf` (13 pages).  
**Language:** Python 3.x  
**Libraries:** Python standard library only  
**IDE:** Visual Studio Code (VS Code)

## Objective

Implement and validate the six assignment tasks in the same order and using the same input data, algorithm terminology, and expected outcomes described in the supplied PDF.

## Task-wise implementation

### Task 1 – Word Wrap as a Document-Layout Engine
- Implements suffix dynamic programming with `DP[n] = 0`.
- Uses squared unused-space penalty for every non-final line and zero penalty for the final line.
- Reconstructs the line arrangement using a next-break array.
- Tests widths 16, 20 and 24, an exact-width word, and a word longer than the width.
- Expected minimum penalties from the PDF: 246, 39 and 81.

### Task 2 – Greedy vs Dynamic Programming
- Implements Fractional Knapsack by descending value-to-weight ratio.
- Implements 0/1 Knapsack using a DP table and a ratio-greedy comparison heuristic.
- Uses A(10,60), B(20,100), C(30,120), capacity 50.
- Expected results: fractional value 240; 0/1 ratio-greedy A+B = 160; 0/1 DP B+C = 220.
- Reports greedy quality as 72.73% of the DP optimum.

### Task 3 – Routing Engine Under Changing Network Conditions
- Implements Dijkstra for the base eight-vertex, twelve-road undirected network.
- Converts each undirected road to two directed arcs and adds B→E with weight −6 for Bellman–Ford.
- Adds E→B with weight −1 to test reachable negative-cycle detection.
- Implements Floyd–Warshall distance calculation and Warshall Boolean reachability.
- Matches the PDF's base distances from A: 0, 4, 3, 9, 11, 14, 15, 17; Stage B gives E distance −2; Stage C detects a reachable negative cycle.

### Task 4 – Smart Manufacturing: Assembly-Line Scheduling
- Implements two-line assembly scheduling with DP costs and predecessor decisions.
- Reconstructs the selected line at each station.
- Tests the baseline input, the transfer-time change `t1[3] = 15`, and a 10-unit increase to Line 1, Station 3.
- Includes the three-line DP extension described in the assignment.

### Task 5 – Minimum Spanning Tree Algorithms
- Implements Kruskal using Disjoint Set Union, Prim using a growing tree, and Borůvka using cheapest outgoing component edges.
- Runs all three on the same graph; each returns seven edges with total cost 21.
- Performs the tie stress test by making A–B and A–C both weight 3. The selected edge sets can differ while the MST cost remains 21.

### Task 6 – Last-Mile Delivery TSP
- Implements Held–Karp subset DP with predecessor reconstruction.
- Uses the PDF's hub plus six delivery-location cost matrix.
- Expected route: Hub → F → E → D → C → B → A → Hub, cost 60.
- Independently validates a smaller hub-plus-four-location instance using all 24 permutations; both methods return 46.
- Prints endpoint-state growth and explains why exact Held–Karp is unsuitable for 200 delivery locations.

## How to run

Run all six tasks:

```bash
python daa_assignment4b.py
```

Run a single task (replace 1 with any task number from 1 to 6):

```bash
python daa_assignment4b.py --task 1
```

In VS Code:
1. Open the folder containing `daa_assignment4b.py`.
2. Select **Terminal → New Terminal**.
3. Run one of the commands above.
4. The final line should read `ASSIGNMENT 4B EXECUTION COMPLETED`.

## Execution result

The complete program was executed successfully. The captured terminal output is included as `execution_output.png`.

## Notes

- The implementation follows the assignment's stated test data and expected results.
- The Dijkstra implementation uses a linear scan to select the next minimum tentative-distance vertex, so its time complexity is O(V² + E), rather than the heap-based O((V+E) log V) variant.
- The two-line assembly DP follows the station and transfer costs in the PDF. The three-line case is presented as the requested engineering extension, not as a separate numerical test because the PDF does not provide three-line input data.

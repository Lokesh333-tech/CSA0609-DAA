# Design and Analysis of Algorithms – Assignment 4A

**Source:** Uploaded `DAA_Assignment_4A_Answers.pdf` (13 pages).

**Objective:** Implement and execute the algorithm designs in Tasks 1–6: greedy methods, dynamic programming, pseudocode repair, and shortest-path algorithms.

**Software Used:** Python 3.x  
**IDE / Tool:** Visual Studio Code (VS Code)

## Task-wise implementation

1. **Task 1 – Algorithm Design Review**
   - Implements Fractional Knapsack.
   - Calculates each item's value-to-weight ratio, sorts in descending order, and takes a whole item or the fraction that fits.
   - Demonstration input is included in the source because the answer PDF explains the algorithm but does not specify a concrete item dataset for this task.

2. **Task 2 – Job Sequencing with Deadlines**
   - Sorts jobs by descending profit.
   - Places each job in the latest available slot not exceeding its deadline.
   - Tests the original example and the changed case where job B's profit becomes 90.

3. **Task 3 – Dynamic Programming: 0/1 Knapsack**
   - Builds the DP table using include/exclude decisions.
   - Reconstructs the selected items for P(2,12), Q(3,20), R(4,25), S(5,30), capacity 7.

4. **Task 4 – Pseudocode Forensics: WordBreak**
   - Repairs the decision condition by requiring both `dp[j] == True` and dictionary membership of the ending substring.
   - Tests the failing case `text = "ab"`, dictionary `{"b"}` and regression case `text = "apple"`, dictionary `{"app", "le"}`.

5. **Task 5 – Dijkstra, Bellman-Ford and Floyd-Warshall**
   - Dijkstra computes single-source shortest paths for non-negative edges using the assignment's A-to-E trace.
   - Bellman-Ford demonstrates shortest paths with a negative edge and checks for a reachable negative cycle.
   - Floyd-Warshall computes the all-pairs distance matrix.

6. **Task 6 – Energy-Aware Job Scheduling**
   - Implements Weighted Interval Scheduling using finish-time ordering, predecessor indices `p(i)`, and a DP recurrence.
   - Reproduces the eight-job example and the adversarial example where B, C, D and E produce 240, outperforming job A's value of 100.

## How to run in VS Code

1. Open the folder containing `daa_assignment4a.py`.
2. Select **Terminal → New Terminal**.
3. Execute:

   `python daa_assignment4a.py`

4. The terminal should finish with `ALL ASSIGNMENT 4A TESTS COMPLETED`.

## Result

The program executed successfully. Fractional Knapsack loaded the full capacity and returned value 240 for its demonstration data. Job Sequencing reproduced schedules `[C, A, D]` with profit 180 and `[B, A, D]` with profit 210 after changing B's profit. 0/1 Knapsack selected Q and R for value 45. WordBreak rejected the faulty input and accepted the valid `app + le` segmentation. Dijkstra returned distances A=0, B=4, C=6, D=7, E=10; Bellman-Ford handled a negative edge without a reachable negative cycle; Floyd-Warshall produced the all-pairs matrix. Weighted Interval Scheduling selected J2, J5, J7 and J8 for value 200, and selected B, C, D and E for value 240 in the adversarial case.

**Note:** Where the assignment PDF provides no concrete input dataset (notably Task 1), a clearly identified demonstration dataset is used to exercise the algorithm. The code's implementation details and reported complexities should be read alongside the explanations in the supplied answer PDF.

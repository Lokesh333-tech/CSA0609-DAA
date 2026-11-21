# Design and Analysis of Algorithms – Assignment 2 (CO2)

**Title:** Experimental Analysis and Implementation of Sorting, Searching, Geometric, and Exhaustive Algorithms

**Objective:** To implement and investigate the algorithms covered in Questions 1–7 of DAA Assignment 2. The program compares sorting algorithms under different input arrangements, measures sequential-search and string-matching operations, evaluates brute-force geometric algorithms, solves a small humanitarian airlift selection problem using exhaustive search, and validates a divide-and-conquer redesign for the closest-pair problem.

**Software Used:** Python 3.13

**Tools:** Visual Studio Code (VS Code), Integrated Terminal

**Algorithms / Concepts Used:**
- Q1: Selection Sort, Bubble Sort with early stopping, and Insertion Sort
- Q2: Sequential Search
- Q3: Brute-Force String Matching
- Q4: Brute-Force Closest Pair using Euclidean distance
- Q5: Brute-Force Convex Hull using the supporting-line / cross-product test
- Q6: Exhaustive Search for the 0/1 Knapsack-style humanitarian airlift problem
- Q7: Divide-and-Conquer Closest Pair redesign and validation against brute force

**Implementation Details:**
- Q1 uses the three exact input arrangements listed in the assignment: nearly sorted, reverse ordered, and already sorted. It reports key comparisons and swaps/shifts separately.
- Q2 tests successful searches at the first, middle, and last positions, plus an unsuccessful search, for list sizes 10, 100, and 1,000.
- Q3 tests early mismatch, repeated-prefix mismatch, and successful matching cases. It reports alignment counts, character comparisons, and match offsets.
- Q4 calculates the closest pair for the assignment's five-point example and prints the exact unique-pair counts for 10, 100, 1,000, and 10,000 drones.
- Q5 tests an interior-point set, a collinear-edge challenge, and a triangle using the cross-product supporting-line principle.
- Q6 enumerates every subset of the four packages and reports the optimal feasible selection for capacity 7.
- Q7 implements a divide-and-conquer closest-pair method with x/y-sorted point lists, compares its result with brute force for manageable test sizes, and runs the redesigned method on 10,000 points.

**How to Run:**
1. Open the assignment folder in VS Code.
2. Ensure Python 3.13 is installed.
3. Open the VS Code Integrated Terminal.
4. Run: `python daa_assignment2.py`

**Result:** Successfully implemented the algorithms for Questions 1–7, generated operation-count evidence for the specified test cases, identified the growth of brute-force methods, and validated the divide-and-conquer closest-pair redesign against the brute-force reference on smaller datasets.

**Note:** Operation counts are the primary evidence. Any execution times depend on the computer, Python version, and background system workload. The 10,000-point brute-force closest-pair value is reported as the exact mathematical pair-count baseline; the program does not waste time executing all 49,995,000 distance calculations for that demonstration size.

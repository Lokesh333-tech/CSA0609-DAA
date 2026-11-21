# Design and Analysis of Algorithms – Assignment 3 (CO3)

**Basis:** The uploaded `DAA_Assignment_3_CO3_Answers.pdf` (8 pages).

**Objective:** Implement the algorithms and worked examples covered in Questions 1–6, and verify their outputs using deterministic test data.

**Software:** Python 3.x  
**IDE:** Visual Studio Code (VS Code)

## Question-wise implementation

1. **Q1 – Decomposition and Elimination in Ordered Data**
   - Tournament divide-and-conquer method to find minimum and maximum.
   - Binary search on a sorted array, including successful and unsuccessful searches.
   - The 8-element tournament example reports 10 comparisons, compared with 14 for independent scans.

2. **Q2 – Quality of Decomposition in Sorting**
   - Merge Sort with comparison counting.
   - Quick Sort using the last element as pivot, with comparison and swap counts.
   - Both algorithms sort the supplied example `[38, 27, 43, 3, 9, 82, 10]`.

3. **Q3 – Karatsuba Multiplication**
   - Recursive three-product Karatsuba multiplication.
   - Verifies `1234 × 5678 = 7,006,652` against conventional multiplication.

4. **Q4 – Strassen's Matrix Multiplication**
   - Computes all seven Strassen products M1–M7 for the 2×2 example in the PDF.
   - Reconstructs the result and checks it against conventional matrix multiplication.

5. **Q5 – Closest Pair Using Divide and Conquer**
   - Includes brute-force and divide-and-conquer implementations.
   - Compares their minimum distances on identical deterministic datasets of 10, 100 and 1,000 points.
   - Prints the exact brute-force pair-count baseline for 10,000 points.

6. **Q6 – Advanced Divide-and-Conquer Mini-Investigations**
   - Part A: deterministic Median of Medians selection, using groups of five.
   - Part B: Meet-in-the-Middle Subset Sum for `[3, 5, 7, 10]` with target 15.

## How to execute in VS Code

1. Open the folder containing `daa_assignment3.py`.
2. Open **Terminal → New Terminal**.
3. Run:

   `python daa_assignment3.py`

4. Confirm that the final line reads `ALL ASSIGNMENT TESTS COMPLETED`.

## Result

The implementations ran successfully. The sorting algorithms produced the same sorted output; Karatsuba matched conventional multiplication; Strassen matched conventional 2×2 matrix multiplication; closest-pair results agreed with brute force for all validation sizes; Median of Medians selected the pivot 9 for the supplied example; and Meet-in-the-Middle found the subset `{5, 10}` for target 15.

**Note:** The assignment PDF's theoretical complexities and worked examples are preserved as the reference. Operation counts shown by the program are from these implementations and may differ from illustrative theoretical counts. Wall-clock timing is not reported because it depends on the execution environment.

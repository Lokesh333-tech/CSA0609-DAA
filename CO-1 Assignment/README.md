# Design and Analysis of Algorithms – Assignment 1

**Title:** Design, Analyse and Validate an Efficient Search Strategy for a Large-Scale Student Record System

**Objective:** To design, implement, test and compare three different strategies for retrieving a student record using its unique registration number. The approaches are iterative linear search, recursive binary search and hash-based lookup. Their preprocessing costs and search performance are considered for datasets containing 1,000, 10,000, 100,000 and 1,000,000 records.

**Software Used:** Python 3.13

**Tools:** Visual Studio Code (VS Code) / Python terminal

**Algorithms Used:**
- Iterative Linear Search
- Recursive Binary Search
- Hash-Based Search using a Python dictionary

**Implementation Details:**
- Linear search scans an unsorted list sequentially and does not require preprocessing.
- Binary search operates on an ascending sorted list. Sorting is measured separately from the search operation.
- Hash search builds a registration-number index (dictionary) once and reuses it for lookups. Index construction is measured separately.
- The program tests both an existing registration number and a missing registration number for each dataset size.
- Median execution times from repeated runs are printed. The timing values depend on the computer and system load.

**Complexity Summary:**
- Linear search: O(n) worst-case search time.
- Recursive binary search: O(log n) search time after O(n log n) sorting, if sorting is required.
- Hash-based search: expected O(n) index construction and expected O(1) lookup; worst-case lookup can be O(n).

**How to Run:**
1. Open the assignment folder in VS Code.
2. Ensure Python 3.13 is installed.
3. Open the terminal in the folder.
4. Run: `python daa_assignment1.py`

**Result:** Successfully implemented and tested iterative linear search, recursive binary search and hash-based lookup for the four required dataset sizes. The program validates successful and unsuccessful searches and reports preprocessing and search execution times separately.

"""
Design and Analysis of Algorithms – Assignment 1
Student Record Retrieval: Linear Search, Recursive Binary Search, and Hash Lookup.

Run:
    python daa_assignment1.py
"""

import random
import statistics
import time


def linear_search(records, target):
    """Iterative sequential search. Returns index, or -1 if absent."""
    for index, registration_number in enumerate(records):
        if registration_number == target:
            return index
    return -1


def recursive_binary_search(sorted_records, target, low=0, high=None):
    """Recursive binary search on an ascending sorted list."""
    if high is None:
        high = len(sorted_records) - 1

    if low > high:
        return -1

    middle = (low + high) // 2
    if sorted_records[middle] == target:
        return middle
    if target < sorted_records[middle]:
        return recursive_binary_search(sorted_records, target, low, middle - 1)
    return recursive_binary_search(sorted_records, target, middle + 1, high)


def build_hash_index(records):
    """Build a registration-number-to-record-position dictionary."""
    return {registration_number: index
            for index, registration_number in enumerate(records)}


def median_time_ms(function, repeats=3):
    """Return median wall-clock execution time in milliseconds."""
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


def run_benchmark():
    random.seed(42)
    sizes = (1_000, 10_000, 100_000, 1_000_000)

    print("DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 1")
    print("Student Record Retrieval Benchmark")
    print("-" * 104)
    print(f"{'Records':>10} | {'Linear ms':>11} | {'Sort ms':>10} | "
          f"{'Binary ms':>11} | {'Hash build ms':>14} | {'Hash ms':>10} | {'Correct':>7}")
    print("-" * 104)

    for n in sizes:
        # Unique registration numbers; shuffle for the unsorted linear-search input.
        records = list(range(100000, 100000 + n))
        random.shuffle(records)

        # Select the last element so linear search performs n comparisons.
        target = records[-1]
        missing_target = 999999999

        # Preprocessing is measured separately and is not hidden in search time.
        sort_ms = median_time_ms(lambda: sorted(records))
        sorted_records = sorted(records)

        hash_build_ms = median_time_ms(lambda: build_hash_index(records))
        hash_index = build_hash_index(records)

        linear_ms = median_time_ms(lambda: linear_search(records, target))
        binary_ms = median_time_ms(
            lambda: recursive_binary_search(sorted_records, target))
        hash_ms = median_time_ms(lambda: hash_index.get(target))

        # Validate successful and unsuccessful searches for all three methods.
        correct = (
            linear_search(records, target) != -1
            and linear_search(records, missing_target) == -1
            and recursive_binary_search(sorted_records, target) != -1
            and recursive_binary_search(sorted_records, missing_target) == -1
            and hash_index.get(target) is not None
            and hash_index.get(missing_target) is None
        )

        print(f"{n:10,} | {linear_ms:11.4f} | {sort_ms:10.4f} | "
              f"{binary_ms:11.4f} | {hash_build_ms:14.4f} | "
              f"{hash_ms:10.4f} | {str(correct):>7}")

    print("-" * 104)
    print("Validation: PASS means present and absent registration numbers were checked.")
    print("Note: Timings are machine-dependent; preprocessing is reported separately.")
    print("Complexities: Linear O(n); Binary O(log n) after O(n log n) sorting;")
    print("              Hash expected O(1) lookup after expected O(n) index construction.")


if __name__ == "__main__":
    run_benchmark()

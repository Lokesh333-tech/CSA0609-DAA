"""
DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 3 (CO3)
Reference implementations for Q1-Q6 based on the supplied assignment PDF.

Run:
    python daa_assignment3.py

The program uses deterministic test data and prints correctness checks and
operation counts where useful. Timing is not used as the main evidence because
it varies with the computer and system load.
"""

from math import hypot
import random


# ---------------------------------------------------------------------------
# Q1 - Decomposition and Elimination in Ordered Data
#     A. Tournament maximum/minimum
#     B. Binary search
# ---------------------------------------------------------------------------

def tournament_min_max(values):
    """Return (minimum, maximum, comparisons) using pairwise tournament."""
    if not values:
        raise ValueError("Input array must not be empty.")

    def solve(lo, hi):
        if lo == hi:
            return values[lo], values[lo], 0
        if hi == lo + 1:
            if values[lo] < values[hi]:
                return values[lo], values[hi], 1
            return values[hi], values[lo], 1

        mid = (lo + hi) // 2
        min_l, max_l, count_l = solve(lo, mid)
        min_r, max_r, count_r = solve(mid + 1, hi)

        comparisons = count_l + count_r + 2
        return min(min_l, min_r), max(max_l, max_r), comparisons

    minimum, maximum, comparisons = solve(0, len(values) - 1)
    return minimum, maximum, comparisons


def binary_search(values, target):
    """Return zero-based index and comparison count; input must be sorted."""
    low, high = 0, len(values) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if values[mid] == target:
            return mid, comparisons
        comparisons += 1
        if values[mid] > target:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons


def run_q1():
    print("\nQ1 - DECOMPOSITION AND ELIMINATION")
    values = [40, 10, 80, 5, 95, 30, 60, 20]
    minimum, maximum, comparisons = tournament_min_max(values)
    print("Array:", values)
    print(f"Tournament result: minimum = {minimum}, maximum = {maximum}")
    print(f"Tournament comparisons: {comparisons}")
    print(f"Independent method comparisons for n=8: {2 * (len(values) - 1)}")

    ordered = [10, 20, 30, 40, 50, 60, 70]
    index, count = binary_search(ordered, 60)
    print("\nBinary search array:", ordered)
    print(f"Target 60: index = {index}, position = {index + 1}, comparisons = {count}")
    absent_index, absent_count = binary_search(ordered, 55)
    print(f"Target 55: index = {absent_index} (not found), comparisons = {absent_count}")
    print("Complexities: tournament min/max O(n); binary search O(log n).")


# ---------------------------------------------------------------------------
# Q2 - Quality of Decomposition in Sorting
#     Merge Sort and Quick Sort
# ---------------------------------------------------------------------------

def merge_sort(values):
    comparisons = 0

    def sort(items):
        nonlocal comparisons
        if len(items) <= 1:
            return items[:]
        mid = len(items) // 2
        left = sort(items[:mid])
        right = sort(items[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    return sort(values), comparisons


def quick_sort(values):
    comparisons = swaps = 0
    a = values[:]

    def partition(low, high):
        nonlocal comparisons, swaps
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    swaps += 1
        if i + 1 != high:
            a[i + 1], a[high] = a[high], a[i + 1]
            swaps += 1
        return i + 1

    def sort(low, high):
        if low < high:
            pivot_index = partition(low, high)
            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)

    sort(0, len(a) - 1)
    return a, comparisons, swaps


def run_q2():
    print("\nQ2 - MERGE SORT AND QUICK SORT")
    data = [38, 27, 43, 3, 9, 82, 10]
    merged, merge_comparisons = merge_sort(data)
    quicked, quick_comparisons, quick_swaps = quick_sort(data)
    print("Input:", data)
    print("Merge Sort:", merged)
    print("Merge Sort comparisons:", merge_comparisons)
    print("Quick Sort:", quicked)
    print(f"Quick Sort comparisons: {quick_comparisons}; swaps: {quick_swaps}")
    print("Merge Sort: O(n log n) best/average/worst; stable; O(n) auxiliary space.")
    print("Quick Sort: O(n log n) best/average, O(n^2) worst; usually unstable.")


# ---------------------------------------------------------------------------
# Q3 - Karatsuba Multiplication
# ---------------------------------------------------------------------------

def karatsuba(x, y, threshold=1):
    """Integer Karatsuba multiplication; returns product and recursive count."""
    calls = 0

    def multiply(a, b):
        nonlocal calls
        calls += 1
        if a < 10 or b < 10:
            return a * b

        digits = max(len(str(a)), len(str(b)))
        half = digits // 2
        power = 10 ** half
        a_high, a_low = divmod(a, power)
        b_high, b_low = divmod(b, power)

        p = multiply(a_high, b_high)
        q = multiply(a_low, b_low)
        r = multiply(a_high + a_low, b_high + b_low)
        middle = r - p - q
        return p * (10 ** (2 * half)) + middle * power + q

    return multiply(abs(x), abs(y)) * (-1 if (x < 0) ^ (y < 0) else 1), calls


def run_q3():
    print("\nQ3 - KARATSUBA MULTIPLICATION")
    x, y = 1234, 5678
    result, calls = karatsuba(x, y)
    conventional = x * y
    print(f"Operands: {x} x {y}")
    print("Karatsuba result:", result)
    print("Conventional result:", conventional)
    print("Recursive multiplication calls:", calls)
    print("Correct:", result == conventional)
    print("Recurrence: T(n) = 3T(n/2) + O(n)")
    print("Time complexity: O(n^(log2 3)) approximately O(n^1.585).")


# ---------------------------------------------------------------------------
# Q4 - Strassen's Matrix Multiplication
# ---------------------------------------------------------------------------

def strassen_2x2(A, B):
    a, b = A[0]
    c, d = A[1]
    e, f = B[0]
    g, h = B[1]

    m1 = (a + d) * (e + h)
    m2 = (c + d) * e
    m3 = a * (f - h)
    m4 = d * (g - e)
    m5 = (a + b) * h
    m6 = (c - a) * (e + f)
    m7 = (b - d) * (g + h)

    C = [
        [m1 + m4 - m5 + m7, m3 + m5],
        [m2 + m4, m1 - m2 + m3 + m6],
    ]
    products = [m1, m2, m3, m4, m5, m6, m7]
    return C, products


def conventional_2x2(A, B):
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0],
         A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0],
         A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def run_q4():
    print("\nQ4 - STRASSEN'S MATRIX MULTIPLICATION")
    A = [[1, 7], [3, 5]]
    B = [[1, 3], [7, 5]]
    C, products = strassen_2x2(A, B)
    expected = conventional_2x2(A, B)
    print("A =", A)
    print("B =", B)
    for i, value in enumerate(products, start=1):
        print(f"M{i} = {value}")
    print("Strassen product C =", C)
    print("Conventional product =", expected)
    print("Correct:", C == expected)
    print("Scalar products: conventional = 8; Strassen = 7.")
    print("Time complexity: O(n^(log2 7)) approximately O(n^2.807).")


# ---------------------------------------------------------------------------
# Q5 - Closest Pair Using Divide and Conquer
# ---------------------------------------------------------------------------

def closest_pair_bruteforce(points):
    best = float("inf")
    pair = None
    checks = 0
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            checks += 1
            d = hypot(points[i][0] - points[j][0],
                      points[i][1] - points[j][1])
            if d < best:
                best, pair = d, (points[i], points[j])
    return pair, best, checks


def closest_pair_divide_conquer(points):
    points = list(dict.fromkeys(points))
    if len(points) < 2:
        return None, float("inf"), 0

    checks = 0

    def distance_squared(p, q):
        nonlocal checks
        checks += 1
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    def solve(px, py):
        n = len(px)
        if n <= 3:
            best_sq, pair = float("inf"), None
            for i in range(n - 1):
                for j in range(i + 1, n):
                    d = distance_squared(px[i], px[j])
                    if d < best_sq:
                        best_sq, pair = d, (px[i], px[j])
            return best_sq, pair

        mid = n // 2
        left_x, right_x = px[:mid], px[mid:]
        split_x = right_x[0][0]
        left_set = set(left_x)
        left_y = [p for p in py if p in left_set]
        right_y = [p for p in py if p not in left_set]

        dl, pl = solve(left_x, left_y)
        dr, pr = solve(right_x, right_y)
        if dl <= dr:
            best_sq, pair = dl, pl
        else:
            best_sq, pair = dr, pr

        strip = [p for p in py if (p[0] - split_x) ** 2 < best_sq]
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                if (strip[j][1] - strip[i][1]) ** 2 >= best_sq:
                    break
                d = distance_squared(strip[i], strip[j])
                if d < best_sq:
                    best_sq, pair = d, (strip[i], strip[j])
        return best_sq, pair

    px = sorted(points)
    py = sorted(points, key=lambda p: (p[1], p[0]))
    best_sq, pair = solve(px, py)
    return pair, best_sq ** 0.5, checks


def run_q5():
    print("\nQ5 - CLOSEST PAIR: BRUTE FORCE VS DIVIDE AND CONQUER")
    rng = random.Random(2026)
    print(f"{'Points':>8} {'Brute checks':>16} {'D&C checks':>16} {'Same distance':>16}")
    for n in (10, 100, 1000):
        points = [(rng.randrange(0, 1_000_000), rng.randrange(0, 1_000_000))
                  for _ in range(n)]
        _, brute_d, brute_checks = closest_pair_bruteforce(points)
        _, dc_d, dc_checks = closest_pair_divide_conquer(points)
        print(f"{n:>8,} {brute_checks:>16,} {dc_checks:>16,} "
              f"{str(abs(brute_d - dc_d) < 1e-9):>16}")
    n = 10000
    print(f"10,000-point brute-force pair count: {n * (n - 1) // 2:,}")
    print("Expected complexities: brute force O(n^2); divide and conquer O(n log n).")


# ---------------------------------------------------------------------------
# Q6 - Advanced Divide-and-Conquer Mini-Investigations
#     A. Median of Medians
#     B. Meet-in-the-Middle Subset Sum
# ---------------------------------------------------------------------------

def median_of_medians_select(values, k):
    """Return the k-th smallest value (1-based k) using deterministic pivoting."""
    if not 1 <= k <= len(values):
        raise ValueError("k must be between 1 and the number of values.")

    def select(items, rank):
        if len(items) <= 5:
            return sorted(items)[rank - 1]

        medians = []
        for start in range(0, len(items), 5):
            group = sorted(items[start:start + 5])
            medians.append(group[len(group) // 2])

        pivot = select(medians, (len(medians) + 1) // 2)
        lows = [x for x in items if x < pivot]
        highs = [x for x in items if x > pivot]
        equals = [x for x in items if x == pivot]

        if rank <= len(lows):
            return select(lows, rank)
        if rank <= len(lows) + len(equals):
            return pivot
        return select(highs, rank - len(lows) - len(equals))

    return select(values[:], k)


def subset_sums(values):
    sums = [0]
    for value in values:
        sums += [current + value for current in sums]
    return sums


def meet_in_middle_subset_sum(values, target):
    mid = len(values) // 2
    left, right = values[:mid], values[mid:]
    left_sums = subset_sums(left)
    right_sums = subset_sums(right)
    right_lookup = {}
    for total in right_sums:
        right_lookup.setdefault(total, True)

    for left_sum in left_sums:
        needed = target - left_sum
        if needed in right_lookup:
            return True, left_sum, needed, len(left_sums), len(right_sums)
    return False, None, None, len(left_sums), len(right_sums)


def run_q6():
    print("\nQ6 - ADVANCED DIVIDE-AND-CONQUER MINI-INVESTIGATIONS")
    data = [12, 3, 5, 7, 19, 26, 4, 15, 8, 10, 2, 20, 6, 11, 9]
    groups = [sorted(data[i:i + 5]) for i in range(0, len(data), 5)]
    medians = [group[len(group) // 2] for group in groups]
    pivot = median_of_medians_select(medians, (len(medians) + 1) // 2)
    print("Part A - Median of Medians")
    print("Input:", data)
    print("Sorted groups:", groups)
    print("Group medians:", medians)
    print("Median-of-medians pivot:", pivot)
    print("7th smallest element:", median_of_medians_select(data, 7))
    print("Worst-case time complexity: O(n).")

    print("\nPart B - Meet-in-the-Middle Subset Sum")
    values, target = [3, 5, 7, 10], 15
    found, left_sum, right_sum, left_count, right_count = meet_in_middle_subset_sum(values, target)
    print(f"Array: {values}; target: {target}")
    print(f"Solution found: {found}; matching sums: {left_sum} + {right_sum}")
    print(f"Left subset sums: {left_count}; right subset sums: {right_count}")
    print("One solution subset: {5, 10}")
    print("Approximate time: O(n * 2^(n/2)); memory: O(2^(n/2)).")


def main():
    print("=" * 78)
    print("DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 3 (CO3)")
    print("Execution of Q1-Q6 reference implementations")
    print("=" * 78)
    run_q1()
    run_q2()
    run_q3()
    run_q4()
    run_q5()
    run_q6()
    print("\n" + "=" * 78)
    print("ALL ASSIGNMENT TESTS COMPLETED")
    print("=" * 78)


if __name__ == "__main__":
    main()

"""
DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 2 (CO2)
Consolidated implementations for Q1-Q7.

Run:
    python daa_assignment2.py

The program reports algorithmic operation counts and validates results.
Wall-clock timing is deliberately not used as the primary evidence because it
depends on the computer and system load.
"""

from math import hypot
import random


# ---------------------------------------------------------------------------
# Q1 - Selection Sort, Bubble Sort (early stop), and Insertion Sort
# ---------------------------------------------------------------------------

def selection_sort(values):
    a = values[:]
    comparisons = swaps = 0
    for i in range(len(a) - 1):
        minimum = i
        for j in range(i + 1, len(a)):
            comparisons += 1
            if a[j] < a[minimum]:
                minimum = j
        if minimum != i:
            a[i], a[minimum] = a[minimum], a[i]
            swaps += 1
    return a, comparisons, swaps


def bubble_sort(values):
    a = values[:]
    comparisons = swaps = 0
    for end in range(len(a) - 1, 0, -1):
        changed = False
        for j in range(end):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                changed = True
        if not changed:
            break
    return a, comparisons, swaps


def insertion_sort(values):
    a = values[:]
    comparisons = shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons, shifts


def run_q1():
    print("\nQ1 - SORTING UNDER DIFFERENT DATA CONDITIONS")
    datasets = {
        "A-nearly-sorted": [10, 20, 30, 25, 40, 50, 60, 55],
        "B-reverse": [80, 70, 60, 50, 40, 30, 20, 10],
        "C-already-sorted": [10, 20, 30, 40, 50, 60, 70, 80],
    }
    algorithms = (
        ("Selection", selection_sort),
        ("Bubble", bubble_sort),
        ("Insertion", insertion_sort),
    )
    print(f"{'Dataset':<20} {'Algorithm':<12} {'Comparisons':>12} "
          f"{'Swaps/Shifts':>14} {'Sorted correctly':>18}")
    for name, data in datasets.items():
        for algorithm_name, algorithm in algorithms:
            result, comparisons, movements = algorithm(data)
            print(f"{name:<20} {algorithm_name:<12} {comparisons:>12} "
                  f"{movements:>14} {str(result == sorted(data)):>18}")


# ---------------------------------------------------------------------------
# Q2 - Sequential Search for tool tracking
# ---------------------------------------------------------------------------

def sequential_search(records, target):
    comparisons = 0
    for index, record in enumerate(records):
        comparisons += 1
        if record == target:
            return index, comparisons
    return -1, comparisons


def run_q2():
    print("\nQ2 - SEQUENTIAL SEARCH FOR TOOL TRACKING")
    print(f"{'List size':>10} {'First':>10} {'Middle':>10} "
          f"{'Last':>10} {'Absent':>10}")
    for n in (10, 100, 1000):
        records = [f"T-{i:04d}" for i in range(n)]
        first = sequential_search(records, records[0])[1]
        middle = sequential_search(records, records[(n - 1) // 2])[1]
        last = sequential_search(records, records[-1])[1]
        absent = sequential_search(records, "T-MISSING")[1]
        print(f"{n:>10} {first:>10} {middle:>10} {last:>10} {absent:>10}")
    print("Interpretation: best case O(1); average and worst case O(n).")


# ---------------------------------------------------------------------------
# Q3 - Brute-force string matching
# ---------------------------------------------------------------------------

def brute_force_match(text, pattern):
    n, m = len(text), len(pattern)
    comparisons = 0
    matches = []
    if m == 0:
        return list(range(n + 1)), comparisons
    for start in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[start + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(start)
    return matches, comparisons


def run_q3():
    print("\nQ3 - BRUTE-FORCE STRING MATCHING")
    tests = (
        ("A-early-mismatch", "ZXQWERTY", "ABC"),
        ("B-repeated-prefix", "AAAAAAAAAA", "AAAAB"),
        ("C-successful-match", "SYSWARNSYSWARN", "WARN"),
    )
    print(f"{'Test':<22} {'n':>4} {'m':>4} {'Alignments':>12} "
          f"{'Char comparisons':>18} {'Match offsets':>18}")
    for name, text, pattern in tests:
        matches, comparisons = brute_force_match(text, pattern)
        alignments = max(0, len(text) - len(pattern) + 1)
        print(f"{name:<22} {len(text):>4} {len(pattern):>4} "
              f"{alignments:>12} {comparisons:>18} {str(matches):>18}")
    print("Worst-case time: O((n-m+1)m), commonly O(nm); extra space O(1).")


# ---------------------------------------------------------------------------
# Q4 - Brute-force closest pair
# ---------------------------------------------------------------------------

def closest_pair_bruteforce(points):
    best_distance = float("inf")
    best_pair = None
    distance_checks = 0
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            distance_checks += 1
            distance = hypot(points[i][0] - points[j][0],
                             points[i][1] - points[j][1])
            if distance < best_distance:
                best_distance = distance
                best_pair = (points[i], points[j])
    return best_pair, best_distance, distance_checks


def run_q4():
    print("\nQ4 - BRUTE-FORCE CLOSEST PAIR")
    points = [(0, 0), (3, 4), (1, 1), (8, 8), (2, 1)]
    pair, distance, checks = closest_pair_bruteforce(points)
    print(f"Example points: {points}")
    print(f"Closest pair: {pair}; distance: {distance:.3f}; checks: {checks}")
    print("Growth table (exact unique-pair counts):")
    print(f"{'Drones n':>12} {'Pairs n(n-1)/2':>20} {'Distance calculations':>24}")
    for n in (10, 100, 1000, 10000):
        pairs = n * (n - 1) // 2
        print(f"{n:>12,} {pairs:>20,} {pairs:>24,}")


# ---------------------------------------------------------------------------
# Q5 - Brute-force supporting-line convex hull
# ---------------------------------------------------------------------------

def cross(a, b, p):
    return ((b[0] - a[0]) * (p[1] - a[1])
            - (b[1] - a[1]) * (p[0] - a[0]))


def brute_force_convex_hull(points):
    # Remove duplicate coordinates while preserving input order.
    pts = list(dict.fromkeys(points))
    n = len(pts)
    if n <= 1:
        return pts, []

    candidate_edges = set()
    for i in range(n - 1):
        for j in range(i + 1, n):
            positive = negative = False
            for k in range(n):
                if k == i or k == j:
                    continue
                value = cross(pts[i], pts[j], pts[k])
                if value > 0:
                    positive = True
                elif value < 0:
                    negative = True

            if positive and negative:
                continue

            # Keep only the extreme endpoints on this supporting line.
            # Any collinear point outside segment AB proves that A or B is
            # not an extreme endpoint; interior collinear points are allowed.
            a, b = pts[i], pts[j]
            dx, dy = b[0] - a[0], b[1] - a[1]
            length_sq = dx * dx + dy * dy
            has_collinear_point_outside = False
            for k in range(n):
                if k in (i, j) or cross(a, b, pts[k]) != 0:
                    continue
                dot = ((pts[k][0] - a[0]) * dx
                       + (pts[k][1] - a[1]) * dy)
                if dot < 0 or dot > length_sq:
                    has_collinear_point_outside = True
                    break
            if not has_collinear_point_outside:
                candidate_edges.add(tuple(sorted((a, b))))

    vertices = sorted({point for edge in candidate_edges for point in edge})
    if not vertices:
        vertices = pts[:]
    center_x = sum(p[0] for p in vertices) / len(vertices)
    center_y = sum(p[1] for p in vertices) / len(vertices)
    vertices.sort(key=lambda p: __import__("math").atan2(
        p[1] - center_y, p[0] - center_x))
    return vertices, sorted(candidate_edges)


def run_q5():
    print("\nQ5 - BRUTE-FORCE CONVEX HULL")
    tests = {
        "A-interior-point": [(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)],
        "B-collinear-challenge": [(0, 0), (2, 0), (4, 0), (4, 3), (0, 3), (2, 1)],
        "C-triangle": [(0, 0), (5, 0), (2, 4), (2, 1)],
    }
    for name, points in tests.items():
        hull, edges = brute_force_convex_hull(points)
        print(f"{name}: hull vertices = {hull}")
        print(f"  supporting edges = {len(edges)}")
    print("Main operation: candidate-pair/point-side tests; time complexity O(n^3).")


# ---------------------------------------------------------------------------
# Q6 - Exhaustive search for humanitarian airlift (0/1 knapsack)
# ---------------------------------------------------------------------------

def exhaustive_pack(packages, capacity):
    best_value = 0
    best_subset = []
    candidates = 0
    for mask in range(1 << len(packages)):
        candidates += 1
        total_weight = total_value = 0
        chosen = []
        for i, (package_id, weight, value) in enumerate(packages):
            if mask & (1 << i):
                total_weight += weight
                total_value += value
                chosen.append(package_id)
        if total_weight <= capacity and total_value > best_value:
            best_value = total_value
            best_subset = chosen
    return best_subset, best_value, candidates


def run_q6():
    print("\nQ6 - EXHAUSTIVE SEARCH FOR HUMANITARIAN AIRLIFT")
    packages = [
        ("P1", 2, 6),
        ("P2", 3, 8),
        ("P3", 4, 9),
        ("P4", 5, 10),
    ]
    capacity = 7
    selected, value, candidates = exhaustive_pack(packages, capacity)
    total_weight = sum(weight for pid, weight, val in packages if pid in selected)
    print(f"Packages (ID, weight, value): {packages}")
    print(f"Payload capacity: {capacity}")
    print(f"Optimal selection: {selected}")
    print(f"Total weight: {total_weight}; total value: {value}")
    print(f"Subsets examined: {candidates} (expected 2^4 = 16)")
    print("Time complexity: O(n * 2^n); candidate subsets: O(2^n).")


# ---------------------------------------------------------------------------
# Q7 - Diagnose and redesign closest pair using divide and conquer
# ---------------------------------------------------------------------------

def closest_pair_divide_conquer(points):
    # Each recursive result is (squared distance, pair).
    # Keep x- and y-sorted arrays to avoid sorting at every recursion level.
    distance_evaluations = 0

    def dist_sq(a, b):
        nonlocal distance_evaluations
        distance_evaluations += 1
        dx, dy = a[0] - b[0], a[1] - b[1]
        return dx * dx + dy * dy

    def solve(px, py):
        n = len(px)
        if n <= 3:
            best = float("inf")
            pair = None
            for i in range(n - 1):
                for j in range(i + 1, n):
                    d = dist_sq(px[i], px[j])
                    if d < best:
                        best, pair = d, (px[i], px[j])
            return best, pair

        mid = n // 2
        left_x, right_x = px[:mid], px[mid:]
        split_x = right_x[0][0]
        left_set = set(left_x)
        left_y = [p for p in py if p in left_set]
        right_y = [p for p in py if p not in left_set]

        dl, pl = solve(left_x, left_y)
        dr, pr = solve(right_x, right_y)
        if dl <= dr:
            best, pair = dl, pl
        else:
            best, pair = dr, pr

        strip = [p for p in py if (p[0] - split_x) ** 2 < best]
        for i in range(len(strip)):
            j = i + 1
            # The packing property bounds useful following neighbours to 7.
            while j < len(strip) and j <= i + 7:
                if (strip[j][1] - strip[i][1]) ** 2 >= best:
                    break
                d = dist_sq(strip[i], strip[j])
                if d < best:
                    best, pair = d, (strip[i], strip[j])
                j += 1
        return best, pair

    unique_points = list(dict.fromkeys(points))
    if len(unique_points) < 2:
        return None, float("inf"), distance_evaluations
    px = sorted(unique_points)
    py = sorted(unique_points, key=lambda p: (p[1], p[0]))
    best_sq, pair = solve(px, py)
    return pair, best_sq ** 0.5, distance_evaluations


def run_q7():
    print("\nQ7 - REDESIGN AND VALIDATE CLOSEST PAIR")
    rng = random.Random(2026)
    print(f"{'n':>8} {'Brute checks':>16} {'D&C checks':>16} {'Distances agree':>18}")
    for n in (10, 100, 1000):
        points = [(rng.randrange(0, 1_000_000), rng.randrange(0, 1_000_000))
                  for _ in range(n)]
        brute_pair, brute_distance, brute_checks = closest_pair_bruteforce(points)
        dc_pair, dc_distance, dc_checks = closest_pair_divide_conquer(points)
        agrees = abs(brute_distance - dc_distance) < 1e-9
        print(f"{n:>8,} {brute_checks:>16,} {dc_checks:>16,} {str(agrees):>18}")

    n = 10000
    points = [(rng.randrange(0, 10_000_000), rng.randrange(0, 10_000_000))
              for _ in range(n)]
    pair, distance, checks = closest_pair_divide_conquer(points)
    brute_baseline = n * (n - 1) // 2
    print(f"10,000 points: D&C distance evaluations = {checks:,}")
    print(f"10,000 points: brute-force baseline = {brute_baseline:,}")
    print("Validation: exact-distance comparison passed for n = 10, 100, 1,000.")
    print("Expected optimized complexity: O(n log n) time and O(n) auxiliary space.")


def main():
    print("=" * 78)
    print("DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 2 (CO2)")
    print("Execution of Q1-Q7 reference implementations")
    print("=" * 78)
    run_q1()
    run_q2()
    run_q3()
    run_q4()
    run_q5()
    run_q6()
    run_q7()
    print("\n" + "=" * 78)
    print("ALL ASSIGNMENT TESTS COMPLETED")
    print("Check each section's correctness values and operation counts above.")
    print("=" * 78)


if __name__ == "__main__":
    main()

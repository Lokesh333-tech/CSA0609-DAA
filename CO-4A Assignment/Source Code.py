"""
DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 4A
Implementations based on the supplied 13-page answer PDF.

Run:
    python daa_assignment4a.py
"""

from math import inf


# ---------------------------------------------------------------------------
# TASK 1 - Fractional Knapsack (Greedy)
# ---------------------------------------------------------------------------

def fractional_knapsack(items, capacity):
    """
    items: list of dictionaries with id, weight, value
    Returns selected fractions, total loaded weight, and total value.
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    for item in items:
        if item["weight"] <= 0:
            raise ValueError("Every item weight must be positive.")

    ordered = sorted(items,
                     key=lambda item: item["value"] / item["weight"],
                     reverse=True)
    remaining = capacity
    total_value = 0.0
    fractions = {item["id"]: 0.0 for item in items}

    for item in ordered:
        if remaining == 0:
            break
        weight = item["weight"]
        if weight <= remaining:
            fractions[item["id"]] = 1.0
            remaining -= weight
            total_value += item["value"]
        else:
            fraction = remaining / weight
            fractions[item["id"]] = fraction
            total_value += fraction * item["value"]
            remaining = 0

    return fractions, capacity - remaining, total_value


def run_task1():
    print("\nTASK 1 - FRACTIONAL KNAPSACK")
    items = [
        {"id": "P1", "weight": 10, "value": 60},
        {"id": "P2", "weight": 20, "value": 100},
        {"id": "P3", "weight": 30, "value": 120},
    ]
    fractions, loaded_weight, total_value = fractional_knapsack(items, 50)
    print("Items (ID, weight, value):", [(x["id"], x["weight"], x["value"]) for x in items])
    print("Vehicle capacity:", 50)
    print("Fractions selected:", {k: round(v, 2) for k, v in fractions.items()})
    print("Total loaded weight:", round(loaded_weight, 2))
    print("Maximum total value:", round(total_value, 2))
    print("Strategy: descending value-to-weight ratio; take a fraction when needed.")
    print("Time complexity: O(n log n) due to sorting.")


# ---------------------------------------------------------------------------
# TASK 2 - Job Sequencing with Deadlines (Greedy)
# ---------------------------------------------------------------------------

def job_sequencing(jobs):
    """Schedule unit-time jobs by descending profit in the latest free slot."""
    if not jobs:
        return [], 0
    if any(job["deadline"] < 1 for job in jobs):
        raise ValueError("Deadlines must be at least 1.")

    max_deadline = max(job["deadline"] for job in jobs)
    schedule = [None] * (max_deadline + 1)  # slots are 1-based
    total_profit = 0

    for job in sorted(jobs, key=lambda item: item["profit"], reverse=True):
        slot = min(job["deadline"], max_deadline)
        while slot >= 1 and schedule[slot] is not None:
            slot -= 1
        if slot >= 1:
            schedule[slot] = job["id"]
            total_profit += job["profit"]

    return schedule[1:], total_profit


def run_task2():
    print("\nTASK 2 - JOB SEQUENCING WITH DEADLINES")
    jobs = [
        {"id": "A", "deadline": 2, "profit": 80},
        {"id": "B", "deadline": 1, "profit": 35},
        {"id": "C", "deadline": 2, "profit": 60},
        {"id": "D", "deadline": 3, "profit": 40},
        {"id": "E", "deadline": 1, "profit": 25},
    ]
    schedule, profit = job_sequencing(jobs)
    print("Jobs (ID, deadline, profit):",
          [(j["id"], j["deadline"], j["profit"]) for j in jobs])
    print("Final schedule [slot 1, slot 2, slot 3]:", schedule)
    print("Total profit:", profit)

    changed_jobs = [dict(job) for job in jobs]
    for job in changed_jobs:
        if job["id"] == "B":
            job["profit"] = 90
    changed_schedule, changed_profit = job_sequencing(changed_jobs)
    print("After changing B profit to 90:", changed_schedule)
    print("New total profit:", changed_profit)
    print("Greedy rule: descending profit; assign each job to the latest free feasible slot.")


# ---------------------------------------------------------------------------
# TASK 3 - 0/1 Knapsack (Dynamic Programming)
# ---------------------------------------------------------------------------

def zero_one_knapsack(items, capacity):
    """Return maximum value, selected IDs, and DP table."""
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = items[i - 1]["weight"]
        value = items[i - 1]["value"]
        for w in range(1, capacity + 1):
            if weight > w:
                dp[i][w] = dp[i - 1][w]
            else:
                exclude = dp[i - 1][w]
                include = value + dp[i - 1][w - weight]
                dp[i][w] = max(exclude, include)

    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(items[i - 1]["id"])
            w -= items[i - 1]["weight"]
    selected.reverse()
    return dp[n][capacity], selected, dp


def run_task3():
    print("\nTASK 3 - 0/1 KNAPSACK")
    items = [
        {"id": "P", "weight": 2, "value": 12},
        {"id": "Q", "weight": 3, "value": 20},
        {"id": "R", "weight": 4, "value": 25},
        {"id": "S", "weight": 5, "value": 30},
    ]
    capacity = 7
    best_value, selected, dp = zero_one_knapsack(items, capacity)
    print("Items (ID, weight, value):",
          [(x["id"], x["weight"], x["value"]) for x in items])
    print("Capacity:", capacity)
    print("Selected items:", selected)
    print("Total selected weight:", sum(x["weight"] for x in items if x["id"] in selected))
    print("Maximum value:", best_value)
    print("DP row values at capacity 7:", [row[capacity] for row in dp])
    print("Time complexity: O(n * Capacity); space complexity: O(n * Capacity).")


# ---------------------------------------------------------------------------
# TASK 4 - Word Break (Dynamic Programming / Pseudocode Repair)
# ---------------------------------------------------------------------------

def word_break(text, dictionary):
    """
    dp[i] is True if text[:i] can be segmented.
    Correct transition requires both dp[j] and dictionary membership.
    """
    n = len(text)
    dp = [False] * (n + 1)
    previous = [-1] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and text[j:i] in dictionary:
                dp[i] = True
                previous[i] = j
                break

    if not dp[n]:
        return False, []
    words = []
    end = n
    while end > 0:
        start = previous[end]
        words.append(text[start:end])
        end = start
    words.reverse()
    return True, words


def run_task4():
    print("\nTASK 4 - WORDBREAK DEFECT AND REPAIR")
    bad_text, bad_dictionary = "ab", {"b"}
    bad_result, _ = word_break(bad_text, bad_dictionary)
    print(f"Failing input: text = {bad_text!r}, dictionary = {sorted(bad_dictionary)}")
    print("Corrected result (expected False):", bad_result)

    good_text, good_dictionary = "apple", {"app", "le"}
    good_result, words = word_break(good_text, good_dictionary)
    print(f"Regression input: text = {good_text!r}, dictionary = {sorted(good_dictionary)}")
    print("Corrected result (expected True):", good_result)
    print("Segmentation:", words)
    print("Repair condition: dp[j] is True AND text[j:i] belongs to the dictionary.")


# ---------------------------------------------------------------------------
# TASK 5 - Dijkstra, Bellman-Ford and Floyd-Warshall
# ---------------------------------------------------------------------------

def dijkstra(graph, source):
    """Single-source shortest paths for non-negative edge weights."""
    dist = {v: inf for v in graph}
    pred = {v: None for v in graph}
    visited = set()
    dist[source] = 0

    while True:
        candidates = [v for v in graph if v not in visited and dist[v] < inf]
        if not candidates:
            break
        u = min(candidates, key=lambda v: dist[v])
        visited.add(u)
        for v, weight in graph[u]:
            if v not in visited and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pred[v] = u
    return dist, pred


def bellman_ford(vertices, edges, source):
    """Return distances, predecessors and reachable-negative-cycle flag."""
    dist = {v: inf for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0

    for _ in range(len(vertices) - 1):
        changed = False
        for u, v, weight in edges:
            if dist[u] != inf and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pred[v] = u
                changed = True
        if not changed:
            break

    for u, v, weight in edges:
        if dist[u] != inf and dist[u] + weight < dist[v]:
            return dist, pred, True
    return dist, pred, False


def floyd_warshall(vertices, edges):
    """All-pairs shortest paths; supports negative edges, not negative cycles."""
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    dist = [[inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, weight in edges:
        i, j = index[u], index[v]
        dist[i][j] = min(dist[i][j], weight)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != inf and dist[k][j] != inf:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


def run_task5():
    print("\nTASK 5 - DIJKSTRA, BELLMAN-FORD AND FLOYD-WARSHALL")
    vertices = ["A", "B", "C", "D", "E"]
    edges = [
        ("A", "B", 4), ("A", "C", 7),
        ("B", "C", 2), ("B", "D", 6),
        ("C", "D", 1), ("C", "E", 8),
        ("D", "E", 3),
    ]
    graph = {v: [] for v in vertices}
    for u, v, weight in edges:
        graph[u].append((v, weight))

    dist, pred = dijkstra(graph, "A")
    print("Dijkstra source A distances:", dist)
    print("Dijkstra predecessors:", pred)
    print("Shortest path cost A to E:", dist["E"])

    negative_edges = [
        ("S", "A", 4), ("S", "B", 5),
        ("A", "B", -2), ("B", "C", 3), ("A", "C", 4),
    ]
    bf_dist, bf_pred, has_negative_cycle = bellman_ford(
        ["S", "A", "B", "C"], negative_edges, "S")
    print("Bellman-Ford distances from S:", bf_dist)
    print("Bellman-Ford reachable negative cycle:", has_negative_cycle)

    matrix = floyd_warshall(vertices, edges)
    print("Floyd-Warshall all-pairs distance matrix (A-E):")
    for row in matrix:
        print(["INF" if value == inf else int(value) for value in row])
    print("Complexities: Dijkstra O((V+E) log V) with a priority queue;")
    print("Bellman-Ford O(VE); Floyd-Warshall O(V^3).")


# ---------------------------------------------------------------------------
# TASK 6 - Energy-Aware Job Scheduling (Weighted Interval Scheduling)
# ---------------------------------------------------------------------------

def weighted_job_scheduling(jobs):
    """
    Jobs contain id, start, finish, value.
    Sort by finish time; p[i] is last compatible 1-based earlier job.
    """
    ordered = sorted(jobs, key=lambda job: job["finish"])
    n = len(ordered)
    p = [0] * n

    for i in range(n):
        for j in range(i - 1, -1, -1):
            if ordered[j]["finish"] <= ordered[i]["start"]:
                p[i] = j + 1
                break

    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        include_value = ordered[i - 1]["value"] + dp[p[i - 1]]
        exclude_value = dp[i - 1]
        dp[i] = max(include_value, exclude_value)

    selected = []
    i = n
    while i >= 1:
        include_value = ordered[i - 1]["value"] + dp[p[i - 1]]
        if include_value > dp[i - 1]:
            selected.append(ordered[i - 1]["id"])
            i = p[i - 1]
        else:
            i -= 1
    selected.reverse()
    return selected, dp[n], ordered, p, dp


def run_task6():
    print("\nTASK 6 - ENERGY-AWARE WEIGHTED JOB SCHEDULING")
    jobs = [
        {"id": "J1", "start": 1, "finish": 3, "value": 20},
        {"id": "J2", "start": 2, "finish": 5, "value": 50},
        {"id": "J3", "start": 4, "finish": 6, "value": 30},
        {"id": "J4", "start": 6, "finish": 8, "value": 40},
        {"id": "J5", "start": 5, "finish": 9, "value": 60},
        {"id": "J6", "start": 8, "finish": 10, "value": 30},
        {"id": "J7", "start": 9, "finish": 11, "value": 50},
        {"id": "J8", "start": 11, "finish": 13, "value": 40},
    ]
    selected, total, ordered, p, dp = weighted_job_scheduling(jobs)
    print("Selected jobs:", selected)
    print("Maximum total energy-saving value:", total)
    print("Sorted jobs:", [job["id"] for job in ordered])
    print("p(i) values:", p)
    print("DP values:", dp)

    adversarial = [
        {"id": "A", "start": 1, "finish": 10, "value": 100},
        {"id": "B", "start": 1, "finish": 3, "value": 60},
        {"id": "C", "start": 3, "finish": 5, "value": 60},
        {"id": "D", "start": 5, "finish": 7, "value": 60},
        {"id": "E", "start": 7, "finish": 10, "value": 60},
    ]
    adv_selected, adv_total, _, _, _ = weighted_job_scheduling(adversarial)
    print("Adversarial selected jobs:", adv_selected)
    print("Adversarial maximum value:", adv_total)
    print("A highest-value-first greedy choice gives 100; DP finds B,C,D,E = 240.")
    print("Time complexity: O(n^2) for the shown p(i) search and O(n) DP.")


def main():
    print("=" * 78)
    print("DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 4A")
    print("Execution of Tasks 1-6")
    print("=" * 78)
    run_task1()
    run_task2()
    run_task3()
    run_task4()
    run_task5()
    run_task6()
    print("\n" + "=" * 78)
    print("ALL ASSIGNMENT 4A TESTS COMPLETED")
    print("=" * 78)


if __name__ == "__main__":
    main()

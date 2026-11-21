"""
DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 4B
Python reference implementation for all six tasks in the supplied PDF.

Run all tasks:
    python daa_assignment4b.py

Run one task:
    python daa_assignment4b.py --task 1
    python daa_assignment4b.py --task 2
    ...
    python daa_assignment4b.py --task 6

Python standard library only.
"""

from math import inf
from itertools import combinations, permutations
import argparse


# ---------------------------------------------------------------------------
# TASK 1 - WORD WRAP USING DYNAMIC PROGRAMMING
# ---------------------------------------------------------------------------

def word_wrap(words, width):
    """Return minimum penalty, reconstructed lines, and suffix DP table."""
    if width <= 0:
        raise ValueError("Line width must be positive.")
    if any(len(word) > width for word in words):
        too_long = [word for word in words if len(word) > width]
        raise ValueError(f"Word(s) longer than line width {width}: {too_long}")

    n = len(words)
    dp = [inf] * (n + 1)
    next_break = [None] * (n + 1)
    dp[n] = 0

    for i in range(n - 1, -1, -1):
        line_length = 0
        for j in range(i, n):
            line_length += len(words[j]) + (1 if j > i else 0)
            if line_length > width:
                break
            penalty = 0 if j == n - 1 else (width - line_length) ** 2
            candidate = penalty + dp[j + 1]
            if candidate < dp[i]:
                dp[i] = candidate
                next_break[i] = j + 1

    lines = []
    i = 0
    while i < n:
        j = next_break[i]
        if j is None:
            raise ValueError("No valid line arrangement exists.")
        line = " ".join(words[i:j])
        slack = width - len(line)
        penalty = 0 if j == n else slack ** 2
        lines.append((line, slack, penalty))
        i = j

    return dp[0], lines, dp


def run_task1():
    print("\nTASK 1 - WORD WRAP AS A DOCUMENT-LAYOUT ENGINE")
    sentence = ("Dynamic programming helps organise words into readable "
                "document lines with minimum unused space penalty")
    words = sentence.split()
    print("Input sentence:", sentence)
    for width in (16, 20, 24):
        total, lines, dp = word_wrap(words, width)
        print(f"\nWIDTH {width}: minimum penalty={total}")
        print("Suffix DP:", dp)
        for number, (line, slack, penalty) in enumerate(lines, 1):
            print(f"  line {number}: {line} | unused={slack} | penalty={penalty}")

    print("\nBOUNDARY TEST (word length exactly equals W)")
    exact_total, exact_lines, _ = word_wrap(["exact"], 5)
    print("Input=['exact'], W=5 ->", exact_lines, "total penalty=", exact_total)

    print("OVER-WIDTH TEST")
    try:
        word_wrap(["toolong"], 5)
    except ValueError as exc:
        print("Rejected safely:", exc)
    print("Time complexity: O(n^2); space complexity: O(n).")


# ---------------------------------------------------------------------------
# TASK 2 - FRACTIONAL GREEDY VS 0/1 KNAPSACK DP
# ---------------------------------------------------------------------------

def fractional_knapsack(items, capacity):
    """Items are (name, weight, value); items may be divided."""
    selected = []
    total_value = 0.0
    remaining = capacity
    for name, weight, value in sorted(items, key=lambda x: x[2] / x[1], reverse=True):
        if remaining <= 0:
            break
        amount = min(weight, remaining)
        fraction = amount / weight
        gain = value * fraction
        selected.append((name, fraction, amount, gain))
        total_value += gain
        remaining -= amount
    return total_value, selected


def knapsack_01(items, capacity):
    """Items are (name, weight, value); each item is taken or rejected."""
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, (_, weight, value) in enumerate(items, 1):
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if weight <= c:
                dp[i][c] = max(dp[i][c], value + dp[i - 1][c - weight])

    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            name, weight, _ = items[i - 1]
            chosen.append(name)
            c -= weight
    chosen.reverse()
    return dp[n][capacity], chosen, dp


def ratio_greedy_01(items, capacity):
    """A comparison heuristic: sort by ratio, but never take a fraction."""
    chosen = []
    total_weight = 0
    total_value = 0
    for name, weight, value in sorted(items, key=lambda x: x[2] / x[1], reverse=True):
        if total_weight + weight <= capacity:
            chosen.append(name)
            total_weight += weight
            total_value += value
    return total_value, chosen, total_weight


def run_task2():
    print("\nTASK 2 - GREEDY VS DYNAMIC PROGRAMMING")
    items = [("A", 10, 60), ("B", 20, 100), ("C", 30, 120)]
    capacity = 50
    print("Items (name, weight, value):", items, "| capacity =", capacity)

    frac_value, frac_selected = fractional_knapsack(items, capacity)
    print("\nFractional Knapsack selections:")
    for name, fraction, weight, gain in frac_selected:
        print(f"  {name}: {fraction * 100:.2f}% | weight={weight:g} | value={gain:g}")
    print("Fractional greedy total value:", frac_value)

    greedy_value, greedy_items, greedy_weight = ratio_greedy_01(items, capacity)
    dp_value, dp_items, _ = knapsack_01(items, capacity)
    print("\n0/1 ratio-greedy:", greedy_items, "| weight =", greedy_weight,
          "| value =", greedy_value)
    print("0/1 Dynamic Programming:", dp_items, "| weight =",
          sum(w for name, w, _ in items if name in dp_items),
          "| value =", dp_value)
    print("Greedy quality:", f"{greedy_value / dp_value * 100:.2f}% of DP optimum")
    print("First blocking greedy commitment: taking A leaves capacity 20,")
    print("which cannot fit C; DP instead selects B + C for value 220.")
    print("Fractional greedy: O(n log n); 0/1 DP: O(nW) time and O(nW) space.")


# ---------------------------------------------------------------------------
# TASK 3 - ROUTING UNDER CHANGING NETWORK CONDITIONS
# ---------------------------------------------------------------------------

def make_undirected_adjacency(vertices, edges):
    adj = {v: [] for v in vertices}
    for u, v, weight in edges:
        adj[u].append((v, weight))
        adj[v].append((u, weight))
    return adj


def dijkstra(vertices, edges, source):
    if any(weight < 0 for _, _, weight in edges):
        raise ValueError("Dijkstra requires non-negative edge weights.")
    adj = make_undirected_adjacency(vertices, edges)
    dist = {v: inf for v in vertices}
    pred = {v: None for v in vertices}
    done = set()
    order = []
    dist[source] = 0

    while len(done) < len(vertices):
        candidates = [v for v in vertices if v not in done]
        u = min(candidates, key=lambda v: dist[v])
        if dist[u] == inf:
            break
        done.add(u)
        order.append(u)
        for v, weight in adj[u]:
            if v not in done and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pred[v] = u
    return dist, pred, order


def bellman_ford(vertices, directed_edges, source):
    dist = {v: inf for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0

    for _ in range(len(vertices) - 1):
        changed = False
        for u, v, weight in directed_edges:
            if dist[u] != inf and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pred[v] = u
                changed = True
        if not changed:
            break

    negative_cycle = any(
        dist[u] != inf and dist[u] + weight < dist[v]
        for u, v, weight in directed_edges
    )
    return dist, pred, negative_cycle


def floyd_warshall(vertices, directed_edges):
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    dist = [[inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, weight in directed_edges:
        i, j = index[u], index[v]
        dist[i][j] = min(dist[i][j], weight)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != inf and dist[k][j] != inf:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


def warshall_reachability(vertices, directed_edges):
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    reach = [[False] * n for _ in range(n)]
    for i in range(n):
        reach[i][i] = True
    for u, v, _ in directed_edges:
        reach[index[u]][index[v]] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    return reach


def run_task3():
    print("\nTASK 3 - ROUTING ENGINE UNDER CHANGING NETWORK CONDITIONS")
    vertices = list("ABCDEFGH")
    roads = [
        ("A", "B", 4), ("A", "C", 3), ("B", "C", 2), ("B", "D", 5),
        ("C", "D", 7), ("C", "E", 8), ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 3), ("E", "G", 4), ("F", "H", 5), ("G", "H", 2),
    ]
    dist, pred, order = dijkstra(vertices, roads, "A")
    print("STAGE A - Dijkstra on the base undirected network")
    print("Finalisation order:", " -> ".join(order))
    for v in vertices:
        path = []
        cur = v
        while cur is not None:
            path.append(cur)
            cur = pred[cur]
        path.reverse()
        print(f"  {v}: distance={dist[v]:g}, path={' -> '.join(path)}")

    # Represent each undirected base road by two directed arcs, then add B -> E.
    directed = []
    for u, v, weight in roads:
        directed.extend([(u, v, weight), (v, u, weight)])
    directed.append(("B", "E", -6))

    print("\nSTAGE B - Add directed negative edge B -> E (-6)")
    bf_dist, _, neg = bellman_ford(vertices, directed, "A")
    print("Bellman-Ford distances:", {k: (v if v != inf else "INF") for k, v in bf_dist.items()})
    print("Reachable negative cycle:", neg)
    print("Expected E distance from A: -2")

    print("\nSTAGE C - Add return edge E -> B (-1)")
    cycle_edges = directed + [("E", "B", -1)]
    _, _, cycle = bellman_ford(vertices, cycle_edges, "A")
    print("Reachable negative cycle detected:", cycle)

    print("\nSTAGE D - Floyd-Warshall and Warshall on base graph")
    base_arcs = []
    for u, v, weight in roads:
        base_arcs.extend([(u, v, weight), (v, u, weight)])
    matrix = floyd_warshall(vertices, base_arcs)
    reach = warshall_reachability(vertices, base_arcs)
    print("Distance matrix:")
    for row in matrix:
        print(["INF" if x == inf else int(x) for x in row])
    print("Reachability from A:", reach[0])
    print("Complexities: Dijkstra O(V^2 + E) with linear minimum scan; Bellman-Ford O(VE);")
    print("Floyd-Warshall and Warshall: O(V^3) time, O(V^2) space.")


# ---------------------------------------------------------------------------
# TASK 4 - TWO-LINE ASSEMBLY-LINE SCHEDULING
# ---------------------------------------------------------------------------

def assembly_line(a1, a2, t1, t2, entry1, entry2, exit1, exit2):
    """Return minimum completion time, line route, and DP decision trace."""
    n = len(a1)
    f1, f2 = [0] * n, [0] * n
    p1, p2 = [1] * n, [2] * n
    trace = []

    f1[0] = entry1 + a1[0]
    f2[0] = entry2 + a2[0]

    for j in range(1, n):
        stay1 = f1[j - 1] + a1[j]
        transfer1 = f2[j - 1] + t2[j - 1] + a1[j]
        stay2 = f2[j - 1] + a2[j]
        transfer2 = f1[j - 1] + t1[j - 1] + a2[j]

        if stay1 <= transfer1:
            f1[j], p1[j] = stay1, 1
        else:
            f1[j], p1[j] = transfer1, 2

        if stay2 <= transfer2:
            f2[j], p2[j] = stay2, 2
        else:
            f2[j], p2[j] = transfer2, 1

        trace.append((j + 1, stay1, transfer1, "stay" if p1[j] == 1 else "transfer",
                      stay2, transfer2, "stay" if p2[j] == 2 else "transfer"))

    total1, total2 = f1[-1] + exit1, f2[-1] + exit2
    last_line = 1 if total1 <= total2 else 2
    total = min(total1, total2)
    route = [0] * n
    route[-1] = last_line
    for j in range(n - 1, 0, -1):
        route[j - 1] = p1[j] if route[j] == 1 else p2[j]
    return total, route, f1, f2, trace


def run_task4():
    print("\nTASK 4 - SMART MANUFACTURING: ASSEMBLY LINE SCHEDULING")
    a1 = [7, 9, 3, 4, 8, 4]
    a2 = [8, 5, 6, 4, 5, 7]
    t1 = [2, 3, 1, 3, 4]  # transfer from line 1 to line 2
    t2 = [2, 1, 2, 2, 1]  # transfer from line 2 to line 1
    baseline = assembly_line(a1, a2, t1, t2, 2, 4, 3, 2)
    total, route, f1, f2, trace = baseline
    print("BASELINE")
    print("Line 1 DP:", f1)
    print("Line 2 DP:", f2)
    print("Station decisions:")
    for row in trace:
        print(" ", row)
    print("Minimum production time:", total)
    print("Line route:", route)

    changed_t1 = t1[:]
    changed_t1[2] = 15
    changed = assembly_line(a1, a2, changed_t1, t2, 2, 4, 3, 2)
    print("\nCHANGE A - Increase transfer t1[3] from 3 to 15")
    print("New minimum time:", changed[0], "| new route:", changed[1])

    changed_a1 = a1[:]
    changed_a1[2] += 10
    disrupted = assembly_line(changed_a1, a2, t1, t2, 2, 4, 3, 2)
    print("\nCHANGE B - Increase Line 1, Station 3 processing time by 10")
    print("New minimum time:", disrupted[0], "| new route:", disrupted[1])

    print("\nTHREE-LINE EXTENSION")
    print("For three lines, each destination state compares staying with transfers")
    print("from either of the other two lines; store the predecessor line per station.")


# ---------------------------------------------------------------------------
# TASK 5 - MINIMUM SPANNING TREE: KRUSKAL, PRIM AND BORUVKA
# ---------------------------------------------------------------------------

def kruskal(vertices, edges):
    parent = {v: v for v in vertices}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    result = []
    for u, v, weight in sorted(edges, key=lambda x: x[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            result.append((u, v, weight))
            if len(result) == len(vertices) - 1:
                break
    return result, sum(e[2] for e in result)


def prim(vertices, edges, start):
    adj = {v: [] for v in vertices}
    for u, v, weight in edges:
        adj[u].append((weight, v))
        adj[v].append((weight, u))
    used = {start}
    result = []
    while len(used) < len(vertices):
        candidates = sorted(
            (weight, u, v)
            for u in used
            for weight, v in adj[u]
            if v not in used
        )
        if not candidates:
            break
        weight, u, v = candidates[0]
        used.add(v)
        result.append((u, v, weight))
    return result, sum(e[2] for e in result)


def boruvka(vertices, edges):
    parent = {v: v for v in vertices}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    result = []
    while len({find(v) for v in vertices}) > 1:
        cheapest = {}
        for u, v, weight in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                continue
            if ru not in cheapest or weight < cheapest[ru][2]:
                cheapest[ru] = (u, v, weight)
            if rv not in cheapest or weight < cheapest[rv][2]:
                cheapest[rv] = (u, v, weight)

        changed = False
        for u, v, weight in sorted(set(cheapest.values()), key=lambda x: x[2]):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                result.append((u, v, weight))
                changed = True
        if not changed:
            break
    return result, sum(e[2] for e in result)


def run_task5():
    print("\nTASK 5 - THREE GREEDY ENGINEERS: MST ALGORITHMS")
    vertices = list("ABCDEFGH")
    edges = [
        ("A", "B", 4), ("A", "C", 3), ("B", "C", 2), ("B", "D", 5),
        ("C", "D", 7), ("C", "E", 8), ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 3), ("E", "G", 4), ("F", "H", 5), ("G", "H", 2),
    ]

    for name, result in (
        ("Kruskal", kruskal(vertices, edges)),
        ("Prim", prim(vertices, edges, "A")),
        ("Boruvka", boruvka(vertices, edges)),
    ):
        selected, cost = result
        print(f"{name}: {selected} | edges={len(selected)} | cost={cost}")

    print("\nMULTIPLE-MST STRESS TEST")
    tied_edges = [(u, v, (3 if (u, v) in {("A", "B"), ("A", "C")} else w))
                  for u, v, w in edges]
    for name, result in (
        ("Kruskal", kruskal(vertices, tied_edges)),
        ("Prim", prim(vertices, tied_edges, "A")),
        ("Boruvka", boruvka(vertices, tied_edges)),
    ):
        print(f"{name} with tied A-B/A-C weights: {result[0]} | cost={result[1]}")
    print("An MST is valid when it has V-1 edges, spans all vertices, is acyclic,")
    print("and has minimum cost; tied graphs can have more than one valid MST.")


# ---------------------------------------------------------------------------
# TASK 6 - LAST-MILE DELIVERY TSP USING HELD-KARP DP
# ---------------------------------------------------------------------------

def held_karp(cost):
    """Return minimum tour cost, closed route, and number of DP states."""
    n = len(cost)
    m = n - 1
    dp = {}
    parent = {}

    for j in range(1, n):
        dp[(1 << (j - 1), j)] = cost[0][j]

    for size in range(2, m + 1):
        for group in combinations(range(1, n), size):
            mask = sum(1 << (j - 1) for j in group)
            for j in group:
                previous_mask = mask ^ (1 << (j - 1))
                best_cost, best_previous = min(
                    (dp[(previous_mask, k)] + cost[k][j], k)
                    for k in group if k != j
                )
                dp[(mask, j)] = best_cost
                parent[(mask, j)] = best_previous

    full = (1 << m) - 1
    total, last = min((dp[(full, j)] + cost[j][0], j) for j in range(1, n))

    route = [last]
    mask = full
    current = last
    while mask.bit_count() > 1:
        previous = parent[(mask, current)]
        mask ^= 1 << (current - 1)
        current = previous
        route.append(current)
    route = [0] + route[::-1] + [0]
    return total, route, len(dp)


def tour_cost(route, cost):
    return sum(cost[route[i]][route[i + 1]] for i in range(len(route) - 1))


def exhaustive_tsp(cost):
    """Independent exhaustive validation; vertex zero is the hub."""
    n = len(cost)
    best_cost = inf
    best_route = None
    for order in permutations(range(1, n)):
        route = (0,) + order + (0,)
        value = tour_cost(route, cost)
        if value < best_cost:
            best_cost, best_route = value, route
    return best_cost, best_route


def run_task6():
    print("\nTASK 6 - LAST-MILE DELIVERY ROUTE OPTIMISATION")
    labels = ["Hub", "A", "B", "C", "D", "E", "F"]
    cost = [
        [0, 10, 15, 20, 18, 12, 16],
        [10, 0, 9, 10, 8, 11, 14],
        [15, 9, 0, 7, 9, 13, 10],
        [20, 10, 7, 0, 6, 8, 12],
        [18, 8, 9, 6, 0, 5, 9],
        [12, 11, 13, 8, 5, 0, 7],
        [16, 14, 10, 12, 9, 7, 0],
    ]

    total, route, states = held_karp(cost)
    print("Held-Karp route:", " -> ".join(labels[i] for i in route))
    print("Minimum tour cost:", total)
    print("DP endpoint states:", states, "(expected 6 * 2^5 = 192)")

    # Independent exhaustive check on hub + four locations (A-D).
    small = [row[:5] for row in cost[:5]]
    dp_small, route_small, _ = held_karp(small)
    brute_cost, brute_route = exhaustive_tsp(small)
    print("\nINDEPENDENT VALIDATION (hub + A-D)")
    print("Held-Karp cost:", dp_small, "| route:", route_small)
    print("Exhaustive cost:", brute_cost, "| route:", brute_route)
    print("All 4! = 24 visit orders checked:", dp_small == brute_cost)

    print("\nSTATE-SPACE GROWTH")
    for m in range(4, 9):
        print(f"  {m} delivery locations: {m * (2 ** (m - 1))} endpoint states")
    print("Complexity: O(m^2 * 2^m) time and O(m * 2^m) memory.")
    print("For 200 locations, exact Held-Karp is impractical; investigate nearest")
    print("neighbour + 2-opt/3-opt, simulated annealing or other TSP heuristics.")


def main():
    parser = argparse.ArgumentParser(description="DAA Assignment 4B implementations")
    parser.add_argument("--task", type=int, choices=range(1, 7),
                        help="run only task number 1 to 6")
    args = parser.parse_args()

    tasks = {
        1: run_task1,
        2: run_task2,
        3: run_task3,
        4: run_task4,
        5: run_task5,
        6: run_task6,
    }
    print("=" * 78)
    print("DESIGN AND ANALYSIS OF ALGORITHMS - ASSIGNMENT 4B")
    print("Python reference implementation | Tasks 1-6")
    print("=" * 78)
    if args.task:
        tasks[args.task]()
    else:
        for task in tasks.values():
            task()
    print("\n" + "=" * 78)
    print("ASSIGNMENT 4B EXECUTION COMPLETED")
    print("=" * 78)


if __name__ == "__main__":
    main()

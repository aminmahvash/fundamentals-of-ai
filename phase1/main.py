from collections import deque
import heapq
from environment import Map



# BFS (Breadth-First Search)
def bfs(env):
    start = env.get_start_state()
    goal = env.get_goal_state()
    print(f"\n=== BFS ===")
    print(f"Start: {start}, Goal: {goal}")

    # queue: (state, path, cost)
    queue = deque([(start, [start], 0)])
    visited = set([start])
    expanded_count = 0

    yield ("expand", start)
    expanded_count += 1

    while queue:
        state, path, cost_so_far = queue.popleft()

        if state == goal:
            print(f"Expanded nodes: {expanded_count}")
            print(f"Path length (nodes): {len(path)}")
            print(f"Total path cost: {cost_so_far}")
            yield ("goal", path)
            return path

        for next_state, edge_cost in env.get_successors(state):
            if next_state not in visited:
                visited.add(next_state)
                new_path = path + [next_state]
                new_cost = cost_so_far + edge_cost
                queue.append((next_state, new_path, new_cost))
                yield ("frontier", next_state)
                yield ("expand", next_state)
                expanded_count += 1

    print(f"Expanded nodes: {expanded_count} (no path found)")
    yield ("fail", None)
    return None


# IDS (Iterative Deepening Search)
def ids(env):
    start = env.get_start_state()
    goal = env.get_goal_state()
    print(f"\n=== IDS (Iterative Deepening Search) ===")
    print(f"Start: {start}, Goal: {goal}")

    if env.is_goal_state(start):
        print(f"Start is already the goal!")
        yield ("goal", [start])
        return [start]

    total_expanded = 0

    # شروع از عمق 0 تا حداکثر معقول
    for depth_limit in range(0, 101):
        yield ("reset_visuals", None)

        # پشته: (state, path, cost, depth)
        stack = [(start, [start], 0, 0)]

        # بهینه‌سازی: نگهداری کمترین عمق دیده‌شده برای هر state
        visited_at_depth = {start: 0}

        result_path = None
        result_cost = None
        expanded_this = 0

        # اولین expand برای start (فقط یکبار در هر iteration)
        yield ("expand", start)
        expanded_this += 1

        while stack:
            state, path, cost, depth = stack.pop()

            if env.is_goal_state(state):
                result_path = path
                result_cost = cost
                break

            # اگر از محدودیت عمق گذشتیم، رد کن
            if depth >= depth_limit:
                continue

            # فقط اگر در عمق بهتری هستیم ادامه بده
            if visited_at_depth.get(state, float('inf')) < depth:
                continue

            # گرفتن successorها
            successors = env.get_successors(state)

            # بهینه‌سازی: اگر فاصله Manhattan داریم، sort کن برای کشف سریع‌تر
            def manhattan_dist(s):
                return abs(s[0] - goal[0]) + abs(s[1] - goal[1])

            successors = sorted(successors, key=lambda x: manhattan_dist(x[0]), reverse=True)

            for next_state, edge_cost in successors:
                new_depth = depth + 1

                # اگر از محدودیت عبور کردیم (check زودهنگام)
                if new_depth > depth_limit:
                    continue

                # بهینه‌سازی کلیدی: اگر این state را قبلاً در عمق مساوی یا کمتر دیده بودیم
                if next_state in visited_at_depth and visited_at_depth[next_state] <= new_depth:
                    continue

                # جلوگیری از چرخه ساده در مسیر فعلی - چک سبک‌تر
                if next_state in path[-20:]:  # فقط 20 تای آخر را چک کن
                    continue

                new_path = path + [next_state]
                new_cost = cost + edge_cost

                # ذخیره عمق بازدید
                visited_at_depth[next_state] = new_depth

                stack.append((next_state, new_path, new_cost, new_depth))

                # visualization
                yield ("frontier", next_state)
                yield ("expand", next_state)
                expanded_this += 1

        total_expanded += expanded_this

        # اگر مسیر پیدا شد
        if result_path is not None:
            print(f"\n--- SUCCESS ---")
            print(f"Goal found at depth limit: {depth_limit}")
            print(f"Total expanded nodes (all depths): {total_expanded}")
            print(f"Path length (nodes): {len(result_path)}")
            print(f"Total path cost: {result_cost}")
            yield ("goal", result_path)
            return result_path

        # بهینه‌سازی: اگر در این عمق هیچ نودی اکسپند نشد، یعنی مرده‌ایم
        if expanded_this == 0 and depth_limit > 0:
            print(f"No more nodes to expand at depth {depth_limit}, terminating early.")
            break

    print(f"\n--- FAILURE: No path found ---")
    print(f"Total expanded nodes: {total_expanded}")
    yield ("fail", None)
    return None


# BDS (Bidirectional Search)
def bds(env):
    start = env.get_start_state()
    goal = env.get_goal_state()
    print(f"\n=== BDS ===")
    print(f"Start: {start}, Goal: {goal}")

    if start == goal:
        print("Start and goal are the same.")
        yield ("goal", [start])
        return [start]

    # Forward: (state, path, cost)
    queue_f = deque([(start, [start], 0)])
    visited_f = {start: ([start], 0)}  # path, cost
    # Backward: (state, path, cost)
    queue_b = deque([(goal, [goal], 0)])
    visited_b = {goal: ([goal], 0)}

    expanded_count = 0
    yield ("expand", start)
    expanded_count += 1
    yield ("expand", goal)
    expanded_count += 1

    while queue_f and queue_b:
        # expand from start side
        state_f, path_f, cost_f = queue_f.popleft()
        for next_s, edge_cost in env.get_successors(state_f):
            if next_s not in visited_f:
                new_path_f = path_f + [next_s]
                new_cost_f = cost_f + edge_cost
                visited_f[next_s] = (new_path_f, new_cost_f)
                queue_f.append((next_s, new_path_f, new_cost_f))
                yield ("frontier", next_s)
                yield ("expand", next_s)
                expanded_count += 1

                if next_s in visited_b:
                    path_b, cost_b = visited_b[next_s]
                    full_path = new_path_f + path_b[-2::-1]
                    full_cost = new_cost_f + cost_b
                    print(f"Expanded nodes: {expanded_count}")
                    print(f"Path length (nodes): {len(full_path)}")
                    print(f"Total path cost: {full_cost}")
                    yield ("goal", full_path)
                    return full_path

        # expand from goal side (using predecessors)
        state_b, path_b, cost_b = queue_b.popleft()
        for prev_s, edge_cost in env.get_predecessors(state_b):
            if prev_s not in visited_b:
                new_path_b = path_b + [prev_s]
                new_cost_b = cost_b + edge_cost
                visited_b[prev_s] = (new_path_b, new_cost_b)
                queue_b.append((prev_s, new_path_b, new_cost_b))
                yield ("frontier", prev_s)
                yield ("expand", prev_s)
                expanded_count += 1

                if prev_s in visited_f:
                    path_f, cost_f = visited_f[prev_s]
                    full_path = path_f + new_path_b[-2::-1]
                    full_cost = cost_f + new_cost_b
                    print(f"Expanded nodes: {expanded_count}")
                    print(f"Path length (nodes): {len(full_path)}")
                    print(f"Total path cost: {full_cost}")
                    yield ("goal", full_path)
                    return full_path

    print(f"Expanded nodes: {expanded_count} (no path found)")
    yield ("fail", None)
    return None

# A*
def astar(env):
    start = env.get_start_state()
    goal = env.get_goal_state()
    print(f"\n=== A* ===")
    print(f"Start: {start}, Goal: {goal}")

    def heuristic(state):
        try:
            return abs(state[0] - goal[0]) + abs(state[1] - goal[1])
        except:
            return 0

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start)}
    expanded_count = 0
    yield ("expand", start)
    expanded_count += 1

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            # path and cost
            path = []
            c = current
            while c in came_from:
                path.append(c)
                c = came_from[c]
            path.append(start)
            path.reverse()
            total_cost = g_score[current]
            print(f"Expanded nodes: {expanded_count}")
            print(f"Path length (nodes): {len(path)}")
            print(f"Total path cost: {total_cost}")
            yield ("goal", path)
            return path

        for neighbor, edge_cost in env.get_successors(current):
            tentative_g = g_score[current] + edge_cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                yield ("frontier", neighbor)
                yield ("expand", neighbor)
                expanded_count += 1

    print(f"Expanded nodes: {expanded_count} (no path found)")
    yield ("fail", None)
    return None

# A* Bonus (Creative Heuristic)
def astar_bonus(env):
    start = env.get_start_state()
    goal = env.get_goal_state()
    print(f"\n=== A* BONUS (Creative Heuristic) ===")
    print(f"Start: {start}, Goal: {goal}")

    def heuristic_bonus(state):
        manhattan = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
        return 4.0 * manhattan

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_bonus(start)}
    expanded_count = 0
    yield ("expand", start)
    expanded_count += 1

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            c = current
            while c in came_from:
                path.append(c)
                c = came_from[c]
            path.append(start)
            path.reverse()
            total_cost = g_score[current]
            print(f"Expanded nodes: {expanded_count}")
            print(f"Path length (nodes): {len(path)}")
            print(f"Total path cost: {total_cost}")
            yield ("goal", path)
            return path

        for neighbor, edge_cost in env.get_successors(current):
            tentative_g = g_score[current] + edge_cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic_bonus(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                yield ("frontier", neighbor)
                yield ("expand", neighbor)
                expanded_count += 1

    print(f"Expanded nodes: {expanded_count} (no path found)")
    yield ("fail", None)
    return None

if __name__ == "__main__":
    map = Map(
        search_algorithm=ids,
        seed=42,
        delay=2
    )
    map.start()
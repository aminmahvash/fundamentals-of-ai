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


def dls(env, max_depth=50):
    start = env.get_start_state()
    goal = env.get_goal_state()  # فقط برای چاپ
    print(f"\n=== DLS (max depth = {max_depth}) ===")
    print(f"Start: {start}, Goal: {goal}")

    stack = [(start, [start], 0, 0, {start})]
    expanded_count = 0

    yield ("expand", start)
    expanded_count += 1

    while stack:
        state, path, cost, depth, path_set = stack.pop()

        if env.is_goal_state(state):
            print(f"Expanded nodes: {expanded_count}")
            print(f"Path length (nodes): {len(path)}")
            print(f"Total path cost: {cost}")
            yield ("goal", path)
            return path

        if depth >= max_depth:
            continue

        for next_state, edge_cost in env.get_successors(state):
            if next_state in path_set:
                continue
            new_path_set = path_set.copy()
            new_path_set.add(next_state)
            new_path = path + [next_state]
            new_cost = cost + edge_cost
            stack.append((next_state, new_path, new_cost, depth + 1, new_path_set))
            yield ("frontier", next_state)
            yield ("expand", next_state)
            expanded_count += 1

    print(f"Expanded nodes: {expanded_count} (no path found within depth {max_depth})")
    yield ("fail", None)
    return None


def ids(env):
    start = env.get_start_state()
    goal = env.get_goal_state()
    print(f"\n=== IDS ===")
    print(f"Start: {start}, Goal: {goal}")

    total_expanded = 0
    depth_limit = 0

    while depth_limit <= 100:
        yield ("reset_visuals", None)

        stack = [(start, [start], 0, 0, {start})]
        exp_this = 0
        result_path = None
        result_cost = None

        yield ("expand", start)
        exp_this += 1

        while stack:
            state, path, cost, depth, path_set = stack.pop()

            if env.is_goal_state(state):
                result_path = path
                result_cost = cost
                break

            if depth >= depth_limit:
                continue

            for next_state, edge_cost in env.get_successors(state):
                if next_state in path_set:
                    continue
                new_path_set = path_set.copy()
                new_path_set.add(next_state)
                new_path = path + [next_state]
                new_cost = cost + edge_cost
                stack.append((next_state, new_path, new_cost, depth + 1, new_path_set))
                yield ("frontier", next_state)
                yield ("expand", next_state)
                exp_this += 1

        total_expanded += exp_this

        if result_path is not None:
            print(f"Goal found at depth {depth_limit}")
            print(f"Total expanded nodes (all depths): {total_expanded}")
            print(f"Path length (nodes): {len(result_path)}")
            print(f"Total path cost: {result_cost}")
            yield ("goal", result_path)
            return result_path

        depth_limit += 1

    print(f"No path found up to depth {depth_limit}")
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
            # reconstruct path and cost
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
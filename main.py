from collections import deque
import heapq
from environment import Map


def bfs(env):
    start = env.get_start_state()
    goal = env.get_goal_state()

    queue = deque([(start, [start])])
    visited = set([start])

    yield ("expand", start)

    while queue:
        state, path = queue.popleft()

        if state == goal:
            yield ("goal", path)
            return path

        for next_state, cost in env.get_successors(state):
            if next_state not in visited:
                visited.add(next_state)
                new_path = path + [next_state]
                queue.append((next_state, new_path))
                yield ("frontier", next_state)
                yield ("expand", next_state)

    yield ("fail", None)
    return None


def dls(env, max_depth=10, current_state=None, path=None, visited=None, depth=0):
    if current_state is None:
        current_state = env.get_start_state()
        path = [current_state]
        visited = set([current_state])
        yield ("expand", current_state)

    goal = env.get_goal_state()

    if current_state == goal:
        yield ("goal", path)
        return path

    if depth == max_depth:
        return None

    for next_state, cost in env.get_successors(current_state):
        if next_state not in visited:
            visited.add(next_state)
            new_path = path + [next_state]
            yield ("frontier", next_state)
            yield ("expand", next_state)

            result = yield from dls(env, max_depth, next_state, new_path, visited, depth + 1)
            if result is not None:
                return result

    return None

def ids(env):
    depth = 0
    while True:
        yield ("reset_visuals", None)
        result = yield from dls(env, max_depth=depth)
        if result is not None:
            yield ("goal", result)
            return result
        depth += 1
        if depth > 100:   # safe guard
            yield ("fail", None)
            return None

def bds(env):
    start = env.get_start_state()
    goal = env.get_goal_state()

    if start == goal:
        yield ("goal", [start])
        return [start]

    # Forward queue from start
    queue_f = deque([(start, [start])])
    visited_f = {start: [start]}
    # Backward queue from goal
    queue_b = deque([(goal, [goal])])
    visited_b = {goal: [goal]}

    yield ("expand", start)
    yield ("expand", goal)

    while queue_f and queue_b:
        # expand from start side
        state_f, path_f = queue_f.popleft()
        for next_s, cost in env.get_successors(state_f):
            if next_s not in visited_f:
                visited_f[next_s] = path_f + [next_s]
                queue_f.append((next_s, visited_f[next_s]))
                yield ("frontier", next_s)
                yield ("expand", next_s)

                if next_s in visited_b:
                    full_path = visited_f[next_s] + visited_b[next_s][-2::-1]
                    yield ("goal", full_path)
                    return full_path

        # expand from goal side (using predecessors)
        state_b, path_b = queue_b.popleft()
        for prev_s, cost in env.get_predecessors(state_b):
            if prev_s not in visited_b:
                visited_b[prev_s] = path_b + [prev_s]
                queue_b.append((prev_s, visited_b[prev_s]))
                yield ("frontier", prev_s)
                yield ("expand", prev_s)

                if prev_s in visited_f:
                    full_path = visited_f[prev_s] + visited_b[prev_s][-2::-1]
                    yield ("goal", full_path)
                    return full_path

    yield ("fail", None)
    return None


def astar(env):
    start = env.get_start_state()
    goal = env.get_goal_state()

    # Heuristic: Manhattan distance (if states are tuples of coordinates)
    def heuristic(state):
        try:
            return abs(state[0] - goal[0]) + abs(state[1] - goal[1])
        except:
            return 0   # fallback if state is not coordinate tuple

    # Bonus heuristic (non-admissible, for extra credit)
    def heuristic_bonus(state):
        # Overestimate slightly to reduce expanded nodes
        try:
            return 1.5 * (abs(state[0] - goal[0]) + abs(state[1] - goal[1]))
        except:
            return 0

    # You can switch to heuristic_bonus for bonus part
    h = heuristic   # change to heuristic_bonus if needed

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: h(start)}

    yield ("expand", start)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            # reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            yield ("goal", path)
            return path

        for neighbor, cost in env.get_successors(current):
            tentative_g = g_score[current] + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                yield ("frontier", neighbor)
                yield ("expand", neighbor)

    yield ("fail", None)
    return None

if __name__ == "__main__":
    map = Map(
        search_algorithm=bfs,
        seed=42,
        delay=25
    )
    map.start()
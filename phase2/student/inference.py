from collections import deque
from planforge.core.geometry import inside_boundary, overlaps, aspect_ratio
from planforge.core.constraints import constraint_is_satisfied


def forward_check(problem, variable, value, assignment, domains):
    """
    domain متغیرهای assign نشده را بعد از assign کردن variable=value کوچک می‌کند.
    None برمی‌گرداند اگر domain یک متغیر خالی شود.
    """
    new_domains = {v: list(vals) for v, vals in domains.items()}

    for name, rect in assignment.items():
        new_domains[name] = [rect]
    new_domains[variable] = [value]

    changed = True
    while changed:
        changed = False
        for other in problem.variables:
            if other in assignment or other == variable:
                continue

            spec = problem.room_specs[other]
            kept = []
            for candidate in new_domains[other]:
                if not inside_boundary(candidate, problem.width, problem.height):
                    continue
                if not (spec.min_area <= candidate.area <= spec.max_area):
                    continue
                if aspect_ratio(candidate) > spec.max_aspect_ratio + 1e-9:
                    continue

                overlap = False
                for assigned_name, assigned_rect in assignment.items():
                    if overlaps(candidate, assigned_rect):
                        overlap = True
                        break
                if overlap:
                    continue
                if overlaps(candidate, value):
                    continue

                temp = dict(assignment)
                temp[variable] = value
                temp[other] = candidate
                constraint_ok = True
                for c in problem.constraints:
                    if other not in c.variables:
                        continue
                    if not constraint_is_satisfied(problem, c, temp):
                        constraint_ok = False
                        break
                if constraint_ok:
                    kept.append(candidate)

            if len(kept) != len(new_domains[other]):
                changed = True
            new_domains[other] = kept
            if not kept:
                return None

    return new_domains


def ac3(problem, domains):
    """AC-3 preprocessing: domain‌ها را قبل از backtracking کوچک می‌کند."""
    new_domains = {v: list(vals) for v, vals in domains.items()}
    variables = problem.variables
    arc_set = set()

    for c in problem.constraints:
        if len(c.variables) == 2:
            a, b = c.variables[0], c.variables[1]
            arc_set.add((a, b))
            arc_set.add((b, a))

    for i, a in enumerate(variables):
        for b in variables[i + 1:]:
            arc_set.add((a, b))
            arc_set.add((b, a))

    queue = deque(arc_set)

    while queue:
        xi, xj = queue.popleft()

        to_remove = []
        for vi in new_domains[xi]:
            has_support = False
            for vj in new_domains[xj]:
                if overlaps(vi, vj):
                    continue
                temp = {xi: vi, xj: vj}
                ok = True
                for c in problem.constraints:
                    if xi in c.variables and xj in c.variables:
                        if not constraint_is_satisfied(problem, c, temp):
                            ok = False
                            break
                if ok:
                    has_support = True
                    break
            if not has_support:
                to_remove.append(vi)

        if to_remove:
            for v in to_remove:
                new_domains[xi].remove(v)
            if not new_domains[xi]:
                return None
            for xk in variables:
                if xk != xi and xk != xj and (xk, xi) in arc_set:
                    queue.append((xk, xi))

    return new_domains
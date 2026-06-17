from planforge.core.geometry import inside_boundary, overlaps, aspect_ratio
from planforge.core.constraints import constraint_is_satisfied


def _quick_consistent(problem, assignment, variable, value):
    """بررسی سبک سازگاری برای استفاده در heuristic‌ها."""
    spec = problem.room_specs[variable]

    if not inside_boundary(value, problem.width, problem.height):
        return False
    if not (spec.min_area <= value.area <= spec.max_area):
        return False
    if aspect_ratio(value) > spec.max_aspect_ratio + 1e-9:
        return False
    for other_var, other_rect in assignment.items():
        if other_var == variable:
            continue
        if overlaps(value, other_rect):
            return False

    temp = dict(assignment)
    temp[variable] = value
    for c in problem.constraints:
        if variable not in c.variables:
            continue
        if not constraint_is_satisfied(problem, c, temp):
            return False

    return True


def _remaining_values(problem, variable, assignment, domains):
    """تعداد مقادیر معتبر باقی‌مانده در domain یک متغیر."""
    return sum(
        1 for v in domains[variable]
        if _quick_consistent(problem, assignment, variable, v)
    )


def _degree(problem, variable, assignment):
    """تعداد قیودی که variable با متغیرهای assign نشده دیگر دارد."""
    unassigned = set(problem.variables) - set(assignment.keys())
    count = 0
    for c in problem.constraints:
        if variable in c.variables:
            for other in c.variables:
                if other != variable and other in unassigned:
                    count += 1
                    break
    return count


def select_unassigned_variable(problem, assignment, domains):
    """MRV با tie-breaker degree heuristic."""
    unassigned = [v for v in problem.variables if v not in assignment]

    best_var = None
    best_remaining = float("inf")
    best_degree = -1

    for var in unassigned:
        remaining = _remaining_values(problem, var, assignment, domains)
        degree = _degree(problem, var, assignment)

        if (best_var is None
                or remaining < best_remaining
                or (remaining == best_remaining and degree > best_degree)):
            best_var = var
            best_remaining = remaining
            best_degree = degree

    return best_var


def order_domain_values(problem, variable, assignment, domains):
    """LCV واقعی: مقادیری که کمترین محدودیت روی بقیه ایجاد می‌کنند اول."""
    unassigned_others = [v for v in problem.variables
                         if v not in assignment and v != variable]

    if not unassigned_others:
        return list(domains[variable])

    def lcv_key(value):
        temp = dict(assignment)
        temp[variable] = value
        eliminated = sum(
            1
            for other in unassigned_others
            for other_val in domains[other]
            if not _quick_consistent(problem, temp, other, other_val)
        )
        return (eliminated, -value.area)

    candidates = list(domains[variable])
    candidates.sort(key=lcv_key)
    return candidates
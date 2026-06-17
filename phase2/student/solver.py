from student.consistency import is_consistent
from student.heuristics import select_unassigned_variable, order_domain_values, _quick_consistent
from student.inference import ac3, forward_check


def is_complete(problem, assignment):
    return all(v in assignment for v in problem.variables)


def backtrack(problem, assignment, domains, ctx):
    ctx.on_node()

    if ctx.should_stop:
        return

    if is_complete(problem, assignment):
        ctx.on_solution(assignment)
        return

    var = select_unassigned_variable(problem, assignment, domains)
    ctx.on_select_variable(var, assignment)

    unassigned_others = [v for v in problem.variables
                         if v not in assignment and v != var]

    lcv_values = order_domain_values(problem, var, assignment, domains)

    def _lcv_eliminated(value):
        temp = dict(assignment)
        temp[var] = value
        return sum(
            1
            for other in unassigned_others
            for other_val in domains[other]
            if not _quick_consistent(problem, temp, other, other_val)
        )

    ordered_values = sorted(
        lcv_values,
        key=lambda rect: (_lcv_eliminated(rect) // 100, -rect.area, rect.x, rect.y),
    )

    for value in ordered_values:
        if ctx.should_stop:
            return

        ctx.on_assignment_tried()
        ctx.on_consistency_check()

        if is_consistent(problem, assignment, var, value):
            assignment[var] = value
            ctx.on_assign(var, value, assignment)

            before_fc = ctx.domain_size(domains)
            new_domains = forward_check(problem, var, value, assignment, domains)
            if new_domains is not None:
                after_fc = ctx.domain_size(new_domains)
                ctx.on_prune(before_fc, after_fc)
                ctx.on_prune(count=before_fc - after_fc)
                backtrack(problem, assignment, new_domains, ctx)

            del assignment[var]
            ctx.on_unassign(var, assignment)
            ctx.on_backtrack()


def solve(problem, ctx):
    domains = ctx.copy_domains()
    before_ac3 = ctx.domain_size(domains)

    reduced = ac3(problem, domains)
    if reduced is None:
        return None

    after_ac3 = ctx.domain_size(reduced)
    ctx.on_prune(before_ac3, after_ac3)
    ctx.on_prune(count=before_ac3 - after_ac3)
    domains = reduced

    backtrack(problem, {}, domains, ctx)
    return ctx.best_assignment
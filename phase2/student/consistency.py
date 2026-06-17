from planforge.core.geometry import inside_boundary, overlaps
from planforge.core.constraints import constraint_is_satisfied


# ─────────────────────────────────────────────
# تابع: is_consistent
# بررسی می‌کند که آیا assign کردن value به variable
# با assignment فعلی سازگار است یا نه
# ─────────────────────────────────────────────
def is_consistent(problem, assignment, variable, value) -> bool:
    """
    True برمی‌گرداند اگر مقدار value برای variable
    با قیود سخت مسئله و assignment فعلی سازگار باشد.

    بررسی‌های انجام شده:
    1. مستطیل value باید داخل مرز خانه باشد
    2. مساحت اتاق باید در بازه مجاز باشد
    3. value نباید با هیچ اتاق از قبل assign شده overlap داشته باشد
    4. قیود صریح (explicit constraints) نباید نقض شوند
    """

    # ─────────────────────────────────────────
    # بررسی ۱: مستطیل باید داخل مرز خانه باشد
    # ─────────────────────────────────────────
    if not inside_boundary(value, problem.width, problem.height):
        return False

    # ─────────────────────────────────────────
    # بررسی ۲: مساحت اتاق باید در بازه مجاز باشد
    # ─────────────────────────────────────────
    room_spec = problem.room_specs[variable]
    if not (room_spec.min_area <= value.area <= room_spec.max_area):
        return False

    # ─────────────────────────────────────────
    # بررسی ۳: overlap با اتاق‌های قبلاً assign شده
    # ─────────────────────────────────────────
    for assigned_var, assigned_value in assignment.items():
        if assigned_var == variable:
            continue
        if overlaps(value, assigned_value):
            return False

    # ─────────────────────────────────────────
    # بررسی ۴: قیود صریح مسئله
    # constraint_is_satisfied اگر هنوز همه متغیرهای یک قید
    # assign نشده باشند، True برمی‌گرداند (قید هنوز قابل بررسی نیست)
    # بنابراین برای assignment‌های جزئی مناسب است
    # ─────────────────────────────────────────
    # یک assignment موقت می‌سازیم که variable جدید هم داخلش باشد
    temp_assignment = dict(assignment)
    temp_assignment[variable] = value

    for constraint in problem.constraints:
        # فقط قیودی که این variable در آن‌ها شرکت دارد را بررسی می‌کنیم
        if variable not in constraint.variables:
            continue

        # اگر قید نقض شده بود False برمی‌گردانیم
        if not constraint_is_satisfied(problem, constraint, temp_assignment):
            return False

    return True
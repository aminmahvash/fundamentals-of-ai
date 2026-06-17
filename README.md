# AI Course Projects

## Phase 1: Search Algorithms for Self-Driving Taxi

KamBiz buys a self-driving car in Manhattan and needs search algorithms (BFS, DLS, IDS, BDS, A*) for pathfinding to turn it into a taxi.

**Environment Designer:** [@m-semi](https://github.com/m-semi)  (Mahdi Semsarzadeh)  
**Instructor:** Dr. Elham Hatefi  
**TAs:** Mahdi Semsarzadeh, Sadra Khaleghi, Mohammad Saleh Mahdinejad


## Phase 2: Floor Plan Layout Optimization using CSP

In this phase, we developed an intelligent floor plan layout generator for modern apartments using Constraint Satisfaction Problem (CSP) techniques. The system automatically places and scales various rooms while strictly adhering to architectural guidelines and soft design preferences.

### Core Architecture & Algorithms
* **Backtracking Solver:** A robust depth-first search backtracking engine with live pruning.
* **Inference & Arc Consistency:** Full **AC-3 (Arc Consistency)** preprocessing and dynamic **Forward Checking (MAC)** propagation loop during search.
* **Variable & Value Heuristics:** Implemented **Dynamic MRV** (Minimum Remaining Values) with a Degree Heuristic tie-breaker, and a comprehensive **LCV** (Least Constraining Value) sorting mechanism.
* **Soft Constraints Optimization:** Advanced scoring system evaluating apartment coverage ratio, aspect ratios, daylight access, room shapes, zoning, and relative room distances.

**Environment Designer:** [@msmahdinejad](https://github.com/msmahdinejad)  (Mohammad Saleh Mahdinejad)  
**Instructor:** Dr. Marjan Kaedi  
**TAs:** Mahdi Semsarzadeh, Sadra Khaleghi, Mohammad Saleh Mahdinejad

## Phase 3: Comming soon
---

# پروژه‌های درس هوش مصنوعی

## فاز اول: الگوریتم‌های جستجو برای تاکسی خودران

کامبیز در منهتن یک ماشین خودران می‌خرد و برای مسیریابی به الگوریتم‌های جستجو (*BFS, DLS, IDS, BDS, A) نیاز دارد.

**طراح محیط:**  [@m-semi](https://github.com/m-semi)  (مهدی سمسارزاده)  
**استاد:** دکتر الهام هاتفی  
**دستیاران:** مهدی سمسارزاده، صدرا خالقی، محمدصالح مهدی‌نژاد


## فاز دوم: بهینه‌سازی چیدمان نقشه ساختمان با CSP

در این فاز، یک سیستم هوشمند برای چیدمان خودکار و بهینه اتاق‌های آپارتمان بر اساس مسائل ارضای قید (CSP) پیاده‌سازی شد. این سیستم ابعاد و موقعیت اتاق‌ها را با توجه به قیود سخت معماری و ترجیحات نرم طراحی بهینه‌سازی می‌کند.

### الگوریتم‌ها و ساختار اصلی
* **موتور جستجوی عقب‌گرد (Backtracking):** موتور جستجوی عمق‌اول برای یافتن نقشه‌های معتبر به همراه مکانیزم هرس زنده.
* **استنتاج و سازگاری کمان:** بهره‌گیری از الگوریتم پیش‌پردازش **AC-3** و انتشار محدودیت‌ها به صورت **Forward Checking پویا** در طول جستجو.
* **هوریستیک‌های انتخابی:** پیاده‌سازی **MRV پویا** به همراه هوریستیک درجه (Degree) برای انتخاب متغیر، و مکانیزم **LCV واقعی** برای اولویت‌بندی مقادیر دامنه.
* **امتیازدهی قیود نرم:** تابع ارزیابی پیشرفته برای سنجش نسبت پوشش فضا، تناسبات هندسی اتاق‌ها، میزان نورگیر بودن، زونینگ فضاها و دسترسی‌های داخلی.

**طراح محیط:** [@msmahdinejad](https://github.com/msmahdinejad)  (محمدصالح مهدی‌نژاد)    
**استاد:** دکتر الهام هاتفی  
**دستیاران:** مهدی سمسارزاده، صدرا خالقی، محمدصالح مهدی‌نژاد

## فاز سوم: به زودی

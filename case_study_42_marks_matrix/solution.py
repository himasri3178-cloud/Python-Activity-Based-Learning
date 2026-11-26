# Case Study 42: Student Marks Matrix Analysis
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, nested loops, strings, lists, nested lists, tuples, tuple unpacking

print("=" * 76)
print("          CASE STUDY 42: STUDENT MARKS MATRIX ANALYSIS")
print("=" * 76)

PASS_MARK = 40
LOW_AVG_THRESHOLD = 60.0

subjects = ["Mathematics", "Physics", "Chemistry", "Python", "English"]
students = [
    "Aarav",
    "Bhavna",
    "Charan",
    "Diya",
    "Eshan",
    "Farah",
]

# Nested list (2D matrix): rows = students, columns = subjects (out of 100)
marks_matrix = [
    [92, 88, 76, 95, 84],   # Aarav
    [54, 48, 52, 68, 72],   # Bhavna
    [91, 89, 75, 96, 84],   # Charan (ties with Aarav at 435 total!)
    [45, 36, 41, 58, 63],   # Diya (one fail in Physics)
    [78, 64, 59, 85, 79],   # Eshan
    [60, 51, 49, 74, 70],   # Farah
]

num_students = len(students)
num_subjects = len(subjects)

# 1. Validate matrix dimensions and score bounds (0..100)
is_valid_matrix = True
if len(marks_matrix) != num_students:
    is_valid_matrix = False
else:
    for r in range(num_students):
        if len(marks_matrix[r]) != num_subjects:
            is_valid_matrix = False
            break
        for c in range(num_subjects):
            val = marks_matrix[r][c]
            if val < 0 or val > 100:
                is_valid_matrix = False
                break

if not is_valid_matrix:
    print("[ERROR] Marks matrix dimensions or values (0-100) are invalid.")
else:
    # 2. Row-wise (student-wise) statistics
    print("ROW-WISE (STUDENT) PERFORMANCE")
    print("-" * 76)
    print(f"{'Student':<10} {'Total':>6} {'Avg':>7} {'Min':>5} {'Max':>5}  {'Status'}")
    print("-" * 76)

    student_totals = []
    highest_total = -1
    top_performers = []

    for r in range(num_students):
        row = marks_matrix[r]
        s_total = 0
        s_min = row[0]
        s_max = row[0]
        failed_subjects = []

        for c in range(num_subjects):
            mark = row[c]
            s_total += mark
            if mark < s_min:
                s_min = mark
            if mark > s_max:
                s_max = mark
            if mark < PASS_MARK:
                failed_subjects.append(subjects[c])

        s_avg = s_total / num_subjects
        student_totals.append(s_total)

        if len(failed_subjects) == 0:
            status = "PASS"
        else:
            status = "FAIL (" + ", ".join(failed_subjects) + ")"

        print(f"{students[r]:<10} {s_total:>6} {s_avg:>7.2f} {s_min:>5} {s_max:>5}  {status}")

        if s_total > highest_total:
            highest_total = s_total
            top_performers = [(students[r], s_total, s_avg)]
        elif s_total == highest_total:
            top_performers.append((students[r], s_total, s_avg))

    # 3. Column-wise (subject-wise) statistics
    print("\nCOLUMN-WISE (SUBJECT) PERFORMANCE")
    print("-" * 76)
    print(f"{'Subject':<14} {'Avg':>7} {'Min':>5} {'Max':>5} {'Pass':>6}  {'Remarks'}")
    print("-" * 76)

    low_avg_subjects = []
    for c in range(num_subjects):
        col_total = 0
        col_min = marks_matrix[0][c]
        col_max = marks_matrix[0][c]
        pass_count = 0

        for r in range(num_students):
            mark = marks_matrix[r][c]
            col_total += mark
            if mark < col_min:
                col_min = mark
            if mark > col_max:
                col_max = mark
            if mark >= PASS_MARK:
                pass_count += 1

        col_avg = col_total / num_students
        remark = "Healthy"
        if col_avg < LOW_AVG_THRESHOLD:
            remark = f"LOW AVERAGE (< {LOW_AVG_THRESHOLD:.0f})"
            low_avg_subjects.append((subjects[c], col_avg))

        print(
            f"{subjects[c]:<14} {col_avg:>7.2f} {col_min:>5} {col_max:>5} "
            f"{pass_count:>3}/{num_students:<2}  {remark}"
        )

    # 4. Highlights summary
    print("\nSUMMARY HIGHLIGHTS")
    print("-" * 76)
    print(f"Top Performer(s) (Total = {highest_total}/{num_subjects * 100}):")
    for name, tot, avg in top_performers:
        print(f"   -> {name}: {tot} marks (Average: {avg:.2f}%)")

    print(f"Subjects Below {LOW_AVG_THRESHOLD:.0f}% Class Average:")
    if len(low_avg_subjects) == 0:
        print("   -> None")
    else:
        for subj_name, subj_avg in low_avg_subjects:
            print(f"   -> {subj_name}: {subj_avg:.2f}%")

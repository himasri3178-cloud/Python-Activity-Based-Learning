# Case Study 48: Tuple-Based Employee Shift Conflict Detection
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, nested loops, strings, lists, tuples, tuple operations, tuple unpacking

print("=" * 78)
print("     CASE STUDY 48: TUPLE-BASED EMPLOYEE SHIFT CONFLICT DETECTION")
print("=" * 78)

# Shift tuples: (emp_id, emp_name, day, start_time_hhmm, end_time_hhmm, department)
shift_records = [
    ("E101", "Ananya", "Mon", "09:00", "13:00", "Support"),
    ("E101", "Ananya", "Mon", "12:00", "16:00", "Billing"),     # Overlaps 12:00-13:00
    ("E101", "Ananya", "Tue", "09:00", "13:00", "Support"),
    ("E101", "Ananya", "Tue", "13:00", "17:00", "Dispatch"),    # Touching boundary -> OK
    ("E102", "Bharat", "Mon", "08:30", "12:30", "Security"),
    ("E102", "Bharat", "Mon", "14:00", "18:00", "Security"),    # Separate -> OK
    ("E103", "Chitra", "Wed", "10:00", "15:00", "FrontDesk"),
    ("E103", "Chitra", "Wed", "10:00", "15:00", "Events"),      # Exact duplicate -> Conflict
    ("E103", "Chitra", "Wed", "14:30", "19:00", "Helpdesk"),    # Overlaps both previous shifts
    ("E104", "Deepak", "Thu", "18:00", "16:00", "NightOps"),    # Invalid: end <= start
]

valid_shifts = []
invalid_shifts = []

# Parse and validate shift tuples
for shift in shift_records:
    emp_id, emp_name, day, start_str, end_str, dept = shift

    # Extract HH and MM via string slicing
    if len(start_str) != 5 or len(end_str) != 5 or start_str[2] != ":" or end_str[2] != ":":
        invalid_shifts.append((shift, "Malformed HH:MM format"))
        continue

    s_hr = int(start_str[:2])
    s_min = int(start_str[3:])
    e_hr = int(end_str[:2])
    e_min = int(end_str[3:])

    start_mins = s_hr * 60 + s_min
    end_mins = e_hr * 60 + e_min

    if s_hr < 0 or s_hr > 23 or s_min < 0 or s_min > 59 or e_hr < 0 or e_hr > 24 or e_min < 0 or e_min > 59:
        invalid_shifts.append((shift, "Out-of-range clock time"))
    elif end_mins <= start_mins:
        invalid_shifts.append((shift, "End time must be after start time"))
    else:
        # Store enriched tuple using tuple concatenation
        valid_shifts.append(shift + (start_mins, end_mins))

print("SHIFT RECORDS VALIDATED:", len(valid_shifts), "| INVALID:", len(invalid_shifts))
if len(invalid_shifts) > 0:
    print("\nINVALID SHIFT ENTRIES:")
    for bad_shift, reason in invalid_shifts:
        eid, ename, dy, st, en, dpt = bad_shift
        print(f"   - {eid} ({ename}) {dy} {st}-{en} [{dpt}]: {reason}")

# Pairwise overlap detection using nested loops
conflicts = []
conflicted_employees = []

n = len(valid_shifts)
for i in range(n):
    id1, name1, day1, s1_str, e1_str, dept1, s1, e1 = valid_shifts[i]
    for j in range(i + 1, n):
        id2, name2, day2, s2_str, e2_str, dept2, s2, e2 = valid_shifts[j]

        if id1 == id2 and day1 == day2:
            # Overlap rule: s1 < e2 and s2 < e1 (boundary touch s1 == e2 is allowed)
            if s1 < e2 and s2 < e1:
                overlap_start = s1 if s1 > s2 else s2
                overlap_end = e1 if e1 < e2 else e2
                overlap_mins = overlap_end - overlap_start
                conflicts.append((
                    id1, name1, day1,
                    s1_str + "-" + e1_str + " (" + dept1 + ")",
                    s2_str + "-" + e2_str + " (" + dept2 + ")",
                    overlap_mins,
                ))
                emp_label = id1 + " - " + name1
                if emp_label not in conflicted_employees:
                    conflicted_employees.append(emp_label)

print("\nDETECTED SHIFT CONFLICTS:")
print("-" * 78)
if len(conflicts) == 0:
    print("No overlapping shift conflicts detected.")
else:
    for eid, ename, dy, slot1, slot2, ov_mins in conflicts:
        print(
            f"CONFLICT | {eid} ({ename}) on {dy}: "
            f"[{slot1}] overlaps [{slot2}] by {ov_mins} mins"
        )

print("-" * 78)
print(f"Total Conflicts Found      : {len(conflicts)}")
print(f"Employees with Conflicts   : {len(conflicted_employees)}")
for emp in conflicted_employees:
    print(f"   -> {emp}")

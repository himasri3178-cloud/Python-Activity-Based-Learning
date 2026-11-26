# Case Study 66: Student Academic Risk Classification
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, strings, lists, tuples, tuple unpacking

print("=" * 78)
print("        CASE STUDY 66: STUDENT ACADEMIC RISK CLASSIFICATION")
print("=" * 78)

# Academic policy thresholds
MIN_THEORY_MARKS = 40.0    # Out of 100
MIN_ATTENDANCE = 75.0      # Percentage
MIN_LAB_SCORE = 20.0       # Out of 50

# Parallel input lists representing student records
student_ids = ["S101", "S102", "S103", "S104", "S105", "S106", "S107", "S108"]
student_names = ["Aarav", "Bhavna", "Charan", "Diya", "Eshan", "Farah", "Gaurav", "Hina"]
theory_marks = [78.0, 35.0, 62.0, 32.0, 28.0, 40.0, 85.0, -5.0]
attendance_pct = [88.0, 82.0, 68.0, 65.0, 58.0, 75.0, 70.0, 90.0]
lab_scores = [42.0, 36.0, 28.0, 30.0, 14.0, 20.0, 18.0, 40.0]

no_risk_count = 0
low_risk_count = 0
moderate_risk_count = 0
high_risk_count = 0
invalid_count = 0

multi_risk_students = []

print(
    f"{'ID':<6} {'Name':<9} {'Marks':>6} {'Att%':>6} {'Lab':>5} "
    f"{'Category':<15}  {'Active Risk Factors'}"
)
print("-" * 78)

for i in range(len(student_ids)):
    sid = student_ids[i]
    sname = student_names[i]
    marks = theory_marks[i]
    att = attendance_pct[i]
    lab = lab_scores[i]

    # Validate score and percentage ranges
    if marks < 0 or marks > 100 or att < 0 or att > 100 or lab < 0 or lab > 50:
        invalid_count += 1
        print(
            f"{sid:<6} {sname:<9} {marks:>6.1f} {att:>6.1f} {lab:>5.1f} "
            f"{'INVALID':<15}  [Data out of valid bounds]"
        )
        continue

    risk_factors = []
    if marks < MIN_THEORY_MARKS:
        risk_factors.append(f"Low Marks ({marks:.1f}<40)")
    if att < MIN_ATTENDANCE:
        risk_factors.append(f"Low Attendance ({att:.1f}%<75%)")
    if lab < MIN_LAB_SCORE:
        risk_factors.append(f"Low Lab ({lab:.1f}<20)")

    factor_count = len(risk_factors)

    if factor_count == 0:
        category = "NO RISK"
        no_risk_count += 1
        factors_text = "None (Good Standing)"
    elif factor_count == 1:
        category = "LOW RISK"
        low_risk_count += 1
        factors_text = risk_factors[0]
    elif factor_count == 2:
        category = "MODERATE RISK"
        moderate_risk_count += 1
        factors_text = " + ".join(risk_factors)
        multi_risk_students.append((sid, sname, category, factors_text))
    else:
        category = "HIGH RISK"
        high_risk_count += 1
        factors_text = " + ".join(risk_factors)
        multi_risk_students.append((sid, sname, category, factors_text))

    print(
        f"{sid:<6} {sname:<9} {marks:>6.1f} {att:>6.1f} {lab:>5.1f} "
        f"{category:<15}  {factors_text}"
    )

print("-" * 78)
print("COHORT RISK SUMMARY")
print(f"Total Records Evaluated : {len(student_ids)} (Invalid: {invalid_count})")
print(f"No Risk (0 factors)     : {no_risk_count}")
print(f"Low Risk (1 factor)     : {low_risk_count}")
print(f"Moderate Risk (2 fact.) : {moderate_risk_count}")
print(f"High Risk (3 factors)   : {high_risk_count}")
print(f"\nStudents with Multiple Simultaneous Risk Factors ({len(multi_risk_students)}):")
for sid, sname, cat, desc in multi_risk_students:
    print(f"   -> {sid} ({sname}) [{cat}]: {desc}")

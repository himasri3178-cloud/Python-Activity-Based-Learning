# Case Study 27: Advanced Numeric Pattern Generator
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, nested loops, pattern generation, strings, lists, tuples, tuple unpacking

print("=" * 68)
print("       CASE STUDY 27: ADVANCED NUMERIC PATTERN GENERATOR")
print("=" * 68)

# Test cases: (mode, dimension_n)
# Modes: "HOLLOW_DIAMOND", "SYMMETRIC_DIAMOND"
# Valid dimension range: integer from 1 to 9
test_requests = [
    ("SYMMETRIC_DIAMOND", 5),
    ("HOLLOW_DIAMOND", 5),
    ("HOLLOW_DIAMOND", 4),
    ("SYMMETRIC_DIAMOND", 1),
    ("HOLLOW_DIAMOND", 0),
    ("SYMMETRIC_DIAMOND", -3),
    ("HOLLOW_DIAMOND", 12),
]

for mode, n in test_requests:
    print(f"\nRequest -> Mode: {mode}, Dimension n = {n}")
    print("-" * 50)

    # Dimension validation
    if type(n) is not int or n < 1 or n > 9:
        print(f"[INVALID DIMENSION] n={n} rejected. Allowed range is integer 1 to 9.")
        continue

    if mode == "SYMMETRIC_DIAMOND":
        # Upper half including middle row (1 to n)
        for row in range(1, n + 1):
            line = ""
            # Leading spaces for alignment (2 spaces per missing column)
            for sp in range(n - row):
                line += "  "
            # Ascending numbers: 1 to row
            for num in range(1, row + 1):
                line += str(num) + " "
            # Descending numbers: row-1 down to 1
            for num in range(row - 1, 0, -1):
                line += str(num) + " "
            print(line.rstrip())

        # Lower half (n-1 down to 1)
        for row in range(n - 1, 0, -1):
            line = ""
            for sp in range(n - row):
                line += "  "
            for num in range(1, row + 1):
                line += str(num) + " "
            for num in range(row - 1, 0, -1):
                line += str(num) + " "
            print(line.rstrip())

    elif mode == "HOLLOW_DIAMOND":
        total_rows = (2 * n) - 1
        for i in range(1, total_rows + 1):
            if i <= n:
                row_val = i
            else:
                row_val = total_rows - i + 1

            line = ""
            # Leading alignment spaces
            for sp in range(n - row_val):
                line += "  "

            if row_val == 1:
                line += "1"
            else:
                # Left boundary digit
                line += str(row_val)
                # Inner hollow gap: (2 * (row_val - 1) - 1) double spaces + 1
                inner_gaps = (2 * row_val) - 3
                for g in range(inner_gaps):
                    line += "  "
                line += " " + str(row_val)

            print(line)
    else:
        print(f"[INVALID MODE] Unknown pattern mode: {mode}")

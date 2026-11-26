# Case Study 29: Password Policy Validation Engine
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, strings, lists, tuples, tuple unpacking

print("=" * 74)
print("         CASE STUDY 29: PASSWORD POLICY VALIDATION ENGINE")
print("=" * 74)

MIN_LENGTH = 8
MAX_CONSECUTIVE_REPEAT = 2   # 3+ identical consecutive chars disallowed
SPECIAL_CHARS = "!@#$%^&*()-_+=.,?/:;"
PROHIBITED_SUBSTRINGS = ("password", "admin", "1234", "qwerty", "welcome")

# Test cases: (case_label, candidate_password)
test_passwords = [
    ("TC01 - Strong", "Sky@2026#Py"),
    ("TC02 - Too Short", "Ab1@x"),
    ("TC03 - Missing Upper & Special", "secure99word"),
    ("TC04 - Missing Digit", "Cloud@Alpha"),
    ("TC05 - Repeated Chars", "GoodPasss@12"),
    ("TC06 - Prohibited Substring", "MyAdmin#2026"),
    ("TC07 - Contains Whitespace", "Valid @2026"),
    ("TC08 - Strong Boundary 8ch", "P@ss9Wxy"),
]

passed_count = 0
failed_count = 0

for label, pwd in test_passwords:
    failures = []

    # 1. Minimum length check
    if len(pwd) < MIN_LENGTH:
        failures.append(f"Length {len(pwd)} < minimum {MIN_LENGTH}")

    # 2. Character-category and whitespace checks
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    has_space = False

    for ch in pwd:
        if "A" <= ch <= "Z":
            has_upper = True
        elif "a" <= ch <= "z":
            has_lower = True
        elif "0" <= ch <= "9":
            has_digit = True
        elif ch in SPECIAL_CHARS:
            has_special = True
        elif ch == " " or ch == "\t":
            has_space = True

    if not has_upper:
        failures.append("Missing uppercase letter (A-Z)")
    if not has_lower:
        failures.append("Missing lowercase letter (a-z)")
    if not has_digit:
        failures.append("Missing numeric digit (0-9)")
    if not has_special:
        failures.append("Missing special character")
    if has_space:
        failures.append("Contains disallowed whitespace")

    # 3. Consecutive repetition check (> 2 identical characters in a row)
    if len(pwd) >= 3:
        run_count = 1
        repeat_found = ""
        for i in range(1, len(pwd)):
            if pwd[i] == pwd[i - 1]:
                run_count += 1
                if run_count > MAX_CONSECUTIVE_REPEAT:
                    repeat_found = pwd[i]
                    break
            else:
                run_count = 1
        if repeat_found != "":
            failures.append(f"3+ consecutive repeated character '{repeat_found}'")

    # 4. Prohibited substring check (case-insensitive)
    lower_pwd = pwd.lower()
    matched_banned = []
    for word in PROHIBITED_SUBSTRINGS:
        if word in lower_pwd:
            matched_banned.append(word)
    if len(matched_banned) > 0:
        failures.append("Contains prohibited substring: " + ", ".join(matched_banned))

    # Print evaluation result
    if len(failures) == 0:
        passed_count += 1
        print(f"[{label}] '{pwd}' -> PASS (All policy rules satisfied)")
    else:
        failed_count += 1
        print(f"[{label}] '{pwd}' -> FAIL ({len(failures)} issue(s)):")
        for reason in failures:
            print(f"    - {reason}")

print("-" * 74)
print(f"Total Evaluated: {len(test_passwords)} | Passed: {passed_count} | Failed: {failed_count}")

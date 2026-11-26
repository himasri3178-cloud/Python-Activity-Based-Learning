# Case Study 35: Text Compression Using Character Runs (Run-Length Encoding)
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, strings, lists, tuples, tuple unpacking

print("=" * 78)
print("       CASE STUDY 35: TEXT COMPRESSION USING CHARACTER RUNS")
print("=" * 78)

# Test cases: (case_label, input_text)
test_strings = [
    ("TC01 - High Repetition", "AAAAABBBCCDAA"),
    ("TC02 - Long Sensor Run", "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWB"),
    ("TC03 - No Repetition (Expansion)", "ABCDEF"),
    ("TC04 - Pairs Only (Equal Length)", "AABBCC"),
    ("TC05 - Single Character", "Z"),
    ("TC06 - Empty String", ""),
]

beneficial_count = 0
not_beneficial_count = 0

print(
    f"{'Case':<30} {'OrigLen':>7} {'EncLen':>7} {'Saved':>7}  {'Verdict & Output'}"
)
print("-" * 78)

for label, text in test_strings:
    orig_len = len(text)

    if orig_len == 0:
        not_beneficial_count += 1
        print(f"{label:<30} {0:>7} {0:>7} {'0.0%':>7}  [EMPTY INPUT] Nothing to compress")
        continue

    # Run-length encoding using a loop over consecutive identical characters
    encoded = ""
    runs_list = []
    i = 0
    while i < orig_len:
        current_char = text[i]
        run_len = 1
        while (i + run_len) < orig_len and text[i + run_len] == current_char:
            run_len += 1
        runs_list.append((current_char, run_len))
        encoded += current_char + str(run_len)
        i += run_len

    enc_len = len(encoded)
    diff = orig_len - enc_len
    savings_pct = (diff / orig_len) * 100.0

    if enc_len < orig_len:
        beneficial_count += 1
        status = f"BENEFICIAL -> Encoded: '{encoded}'"
    else:
        not_beneficial_count += 1
        status = f"NOT BENEFICIAL -> Keep original '{text}' (RLE: '{encoded}')"

    print(f"{label:<30} {orig_len:>7} {enc_len:>7} {savings_pct:>6.1f}%  {status}")

print("-" * 78)
print(f"Total Cases Evaluated : {len(test_strings)}")
print(f"Compression Beneficial: {beneficial_count}")
print(f"Not Beneficial / Empty: {not_beneficial_count}")

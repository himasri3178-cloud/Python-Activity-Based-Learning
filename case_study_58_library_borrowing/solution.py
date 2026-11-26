# Case Study 58: Library Borrowing and Fine Reconciliation
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, strings, lists, nested lists, tuples, tuple unpacking

print("=" * 78)
print("      CASE STUDY 58: LIBRARY BORROWING AND FINE RECONCILIATION")
print("=" * 78)

# Inventory nested list: [book_id, title, total_copies, available_copies]
books_inventory = [
    ["BK101", "Python Programming", 3, 3],
    ["BK102", "Data Structures", 2, 2],
    ["BK103", "Discrete Maths", 2, 2],
    ["BK104", "Computer Networks", 1, 1],
]

# Borrowing tuples:
# (record_id, member_id, book_id, allowed_days, days_kept, is_returned)
borrowing_records = [
    ("BR01", "MEM01", "BK101", 14, 10, True),    # Returned on time
    ("BR02", "MEM02", "BK101", 14, 18, True),    # Overdue 4 days (Rs. 5/day = 20)
    ("BR03", "MEM03", "BK101", 14, 25, False),   # Still out, overdue 11 days
    ("BR04", "MEM04", "BK102", 14, 21, True),    # Overdue 7 days (5*5 + 2*10 = 45)
    ("BR05", "MEM05", "BK102", 14, 12, False),   # Still out, within allowed days
    ("BR06", "MEM06", "BK103", 14, 16, False),   # Still out, overdue 2 days
    ("BR07", "MEM07", "BK104", 14, 30, False),   # Still out, overdue 16 days
    ("BR08", "MEM08", "BK104", 14, 5, False),    # Anomaly: exceeds total copies (1)!
    ("BR09", "MEM09", "BK999", 14, 7, True),     # Unknown book ID
]

overdue_records = []
anomalies = []
collected_fines = 0.0
pending_fines = 0.0

print(
    f"{'RecID':<6} {'Mem':<6} {'Book':<6} {'Allow':>5} {'Kept':>5} "
    f"{'Delay':>5} {'Fine':>7}  {'Return & Fine Status'}"
)
print("-" * 78)

for rec in borrowing_records:
    rec_id, mem_id, book_id, allowed_days, days_kept, is_returned = rec

    # Locate book in inventory
    book_index = -1
    for idx in range(len(books_inventory)):
        if books_inventory[idx][0] == book_id:
            book_index = idx
            break

    if book_index == -1:
        anomalies.append(f"{rec_id}: Unknown book ID '{book_id}'")
        print(f"{rec_id:<6} {mem_id:<6} {book_id:<6} {allowed_days:>5} {days_kept:>5}   ---      ---  [INVALID BOOK ID]")
        continue

    if days_kept < 0 or allowed_days <= 0:
        anomalies.append(f"{rec_id}: Invalid day count")
        print(f"{rec_id:<6} {mem_id:<6} {book_id:<6} {allowed_days:>5} {days_kept:>5}   ---      ---  [INVALID DAYS]")
        continue

    # Progressive fine calculation:
    # Delay 1 - 5 days   : Rs. 5 / day
    # Delay 6 - 10 days  : Rs. 10 / day
    # Delay > 10 days    : Rs. 20 / day
    delay = days_kept - allowed_days
    if delay < 0:
        delay = 0

    fine = 0.0
    rem_delay = delay
    if rem_delay > 10:
        fine += (rem_delay - 10) * 20.0
        rem_delay = 10
    if rem_delay > 5:
        fine += (rem_delay - 5) * 10.0
        rem_delay = 5
    if rem_delay > 0:
        fine += rem_delay * 5.0

    # Reconcile available copies for unreturned books
    if not is_returned:
        if books_inventory[book_index][3] > 0:
            books_inventory[book_index][3] -= 1
        else:
            anomalies.append(
                f"{rec_id}: Stock discrepancy on {book_id} (issued > total copies)"
            )

    if delay > 0:
        overdue_records.append((rec_id, mem_id, book_id, delay, fine, is_returned))

    if is_returned:
        collected_fines += fine
        status_text = "Returned On Time" if delay == 0 else "Returned (Fine Paid)"
    else:
        pending_fines += fine
        status_text = "Checked Out (On Time)" if delay == 0 else "OVERDUE (Unreturned)"

    print(
        f"{rec_id:<6} {mem_id:<6} {book_id:<6} {allowed_days:>5} {days_kept:>5} "
        f"{delay:>5} {fine:>7.2f}  {status_text}"
    )

print("\nRECONCILED BOOK INVENTORY")
print("-" * 78)
print(f"{'BookID':<8} {'Title':<24} {'Total':>6} {'Issued':>7} {'Available':>10}")
print("-" * 78)
for item in books_inventory:
    bk_id, title, total_cp, avail_cp = item
    issued_cp = total_cp - avail_cp
    print(f"{bk_id:<8} {title:<24} {total_cp:>6} {issued_cp:>7} {avail_cp:>10}")

print("\nRECONCILIATION SUMMARY")
print("-" * 78)
print(f"Total Records Processed : {len(borrowing_records)}")
print(f"Overdue Records Count   : {len(overdue_records)}")
print(f"Fines Collected (Paid)  : Rs. {collected_fines:.2f}")
print(f"Fines Pending (Active)  : Rs. {pending_fines:.2f}")
print(f"Total Fines Assessed    : Rs. {collected_fines + pending_fines:.2f}")
if len(anomalies) > 0:
    print("Inventory / Record Anomalies:")
    for note in anomalies:
        print(f"   -> {note}")

# Case Study 13: ATM Transaction Sequence Simulation
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, strings, lists, tuples, tuple unpacking

print("=" * 74)
print("          CASE STUDY 13: ATM TRANSACTION SEQUENCE SIMULATION")
print("=" * 74)

# Account policy configuration
opening_balance = 15000.0
MIN_BALANCE = 500.0
MAX_PER_WITHDRAWAL = 10000.0
MAX_DAILY_WITHDRAWAL = 20000.0
MAX_SINGLE_DEPOSIT = 50000.0

balance = opening_balance
daily_withdrawn = 0.0
total_deposited = 0.0

# Sequence of test transactions: (txn_id, txn_type, amount)
transactions = [
    ("TXN01", "DEPOSIT", 5000.0),      # Valid deposit -> 20000
    ("TXN02", "WITHDRAW", 8000.0),     # Valid withdrawal -> 12000
    ("TXN03", "WITHDRAW", 12000.0),    # Exceeds per-txn limit (10000)
    ("TXN04", "WITHDRAW", 2550.0),     # Not multiple of 100
    ("TXN05", "DEPOSIT", -500.0),      # Invalid negative amount
    ("TXN06", "WITHDRAW", 9000.0),     # Valid -> daily = 17000, bal = 3000
    ("TXN07", "WITHDRAW", 4000.0),     # Exceeds daily limit (17000+4000 > 20000)
    ("TXN08", "WITHDRAW", 2700.0),     # Would breach minimum balance (3000-2700 < 500)
    ("TXN09", "WITHDRAW", 2500.0),     # Valid -> daily = 19500, bal = 500 (exact min)
    ("TXN10", "TRANSFER", 1000.0),     # Unsupported transaction type
    ("TXN11", "DEPOSIT", 60000.0),     # Exceeds single deposit limit
]

accepted_log = []
rejected_log = []

print(f"Opening Balance       : Rs. {opening_balance:.2f}")
print(f"Minimum Balance Rule  : Rs. {MIN_BALANCE:.2f}")
print(f"Per-Txn / Daily Limit : Rs. {MAX_PER_WITHDRAWAL:.2f} / Rs. {MAX_DAILY_WITHDRAWAL:.2f}")
print("-" * 74)
print(f"{'ID':<6} {'Type':<10} {'Amount':>10} {'Status':<10} {'Balance':>10}  {'Reason / Note'}")
print("-" * 74)

idx = 0
while idx < len(transactions):
    txn_id, txn_type, amount = transactions[idx]
    idx += 1

    clean_type = txn_type.strip().upper()

    if amount <= 0:
        reason = "Amount must be positive"
        rejected_log.append((txn_id, clean_type, amount, reason))
        print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'REJECTED':<10} {balance:>10.2f}  {reason}")
        continue

    if clean_type == "DEPOSIT":
        if amount > MAX_SINGLE_DEPOSIT:
            reason = f"Exceeds max deposit (Rs.{MAX_SINGLE_DEPOSIT:.0f})"
            rejected_log.append((txn_id, clean_type, amount, reason))
            print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'REJECTED':<10} {balance:>10.2f}  {reason}")
        else:
            balance += amount
            total_deposited += amount
            accepted_log.append((txn_id, clean_type, amount, balance))
            print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'ACCEPTED':<10} {balance:>10.2f}  Credited")

    elif clean_type == "WITHDRAW":
        if amount % 100 != 0:
            reason = "Must be a multiple of Rs. 100"
            rejected_log.append((txn_id, clean_type, amount, reason))
            print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'REJECTED':<10} {balance:>10.2f}  {reason}")
        elif amount > MAX_PER_WITHDRAWAL:
            reason = f"Exceeds per-txn limit (Rs.{MAX_PER_WITHDRAWAL:.0f})"
            rejected_log.append((txn_id, clean_type, amount, reason))
            print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'REJECTED':<10} {balance:>10.2f}  {reason}")
        elif daily_withdrawn + amount > MAX_DAILY_WITHDRAWAL:
            reason = f"Exceeds daily limit (Used Rs.{daily_withdrawn:.0f})"
            rejected_log.append((txn_id, clean_type, amount, reason))
            print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'REJECTED':<10} {balance:>10.2f}  {reason}")
        elif balance - amount < MIN_BALANCE:
            reason = f"Breaches min balance (Rs.{MIN_BALANCE:.0f})"
            rejected_log.append((txn_id, clean_type, amount, reason))
            print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'REJECTED':<10} {balance:>10.2f}  {reason}")
        else:
            balance -= amount
            daily_withdrawn += amount
            accepted_log.append((txn_id, clean_type, amount, balance))
            print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'ACCEPTED':<10} {balance:>10.2f}  Dispensed")

    else:
        reason = "Unsupported transaction type"
        rejected_log.append((txn_id, clean_type, amount, reason))
        print(f"{txn_id:<6} {clean_type:<10} {amount:>10.2f} {'REJECTED':<10} {balance:>10.2f}  {reason}")

print("-" * 74)
print("TRANSACTION SUMMARY")
print(f"Total Transactions Attempted : {len(transactions)}")
print(f"Accepted Transactions        : {len(accepted_log)}")
print(f"Rejected Transactions        : {len(rejected_log)}")
print(f"Opening Balance              : Rs. {opening_balance:.2f}")
print(f"Total Deposited              : Rs. {total_deposited:.2f}")
print(f"Total Withdrawn              : Rs. {daily_withdrawn:.2f}")
print(f"Closing Balance              : Rs. {balance:.2f}")

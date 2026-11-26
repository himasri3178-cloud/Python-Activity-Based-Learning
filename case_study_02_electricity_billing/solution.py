# Case Study 02: Progressive Electricity Billing
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, strings, lists, tuples, tuple unpacking

print("=" * 72)
print("        CASE STUDY 02: PROGRESSIVE ELECTRICITY BILLING SYSTEM")
print("=" * 72)

# Constants for tariff and billing rules
FIXED_CHARGE = 150.0
SURCHARGE_UNIT_LIMIT = 300
HIGH_USAGE_SURCHARGE_RATE = 0.10   # 10% on energy charge when units > 300
SOLAR_REBATE_RATE = 0.08           # 8% rebate on energy charge
LATE_FEE_RATE = 0.05               # 5% penalty on (energy + fixed)
UNUSUAL_PCT_INCREASE = 25.0        # >25% jump from previous month flagged
UNUSUAL_AMT_INCREASE = 500.0       # >Rs. 500 jump from previous month flagged

# Test dataset: list of tuples
# (household_id, month_name, units_consumed, has_solar_rebate, is_late_payment)
test_households = [
    (
        "HH-101 (Normal & Unusual Spike Pattern)",
        [
            ("Jan-2026", 85, False, False),
            ("Feb-2026", 150, True, False),
            ("Mar-2026", 240, False, False),
            ("Apr-2026", 410, False, True),
            ("May-2026", 390, True, False),
        ],
    ),
    (
        "HH-102 (Zero Usage & Boundary/Invalid Validation)",
        [
            ("Jan-2026", 0, False, False),
            ("Feb-2026", 100, True, False),
            ("Mar-2026", 300, False, False),
            ("Apr-2026", -25, False, False),
        ],
    ),
]

for household_label, monthly_records in test_households:
    print("\nHousehold:", household_label)
    print("-" * 72)
    print(
        f"{'Month':<10} {'Units':>6} {'Energy':>9} {'Fixed':>7} "
        f"{'Surchg':>8} {'Rebate':>8} {'NetBill':>10}  {'Alert'}"
    )
    print("-" * 72)

    valid_bills = []
    valid_months = []
    unusual_months = []
    prev_bill = None
    prev_month = ""
    total_net_bill = 0.0
    total_units = 0
    highest_bill = -1.0
    highest_month = ""

    for record in monthly_records:
        month_name, units, has_solar, is_late = record

        # Input validation
        if units < 0:
            print(
                f"{month_name:<10} {units:>6} {'N/A':>9} {'N/A':>7} "
                f"{'N/A':>8} {'N/A':>8} {'INVALID':>10}  [REJECTED: Negative units]"
            )
            continue

        # Progressive slab calculation
        # Slab 1: 0 - 100 units   @ Rs. 2.50
        # Slab 2: 101 - 200 units @ Rs. 4.00
        # Slab 3: 201 - 350 units @ Rs. 6.00
        # Slab 4: > 350 units     @ Rs. 8.00
        energy_charge = 0.0
        remaining = units

        if remaining > 350:
            energy_charge += (remaining - 350) * 8.00
            remaining = 350
        if remaining > 200:
            energy_charge += (remaining - 200) * 6.00
            remaining = 200
        if remaining > 100:
            energy_charge += (remaining - 100) * 4.00
            remaining = 100
        if remaining > 0:
            energy_charge += remaining * 2.50

        # Surcharges and rebates
        surcharge = 0.0
        if units > SURCHARGE_UNIT_LIMIT:
            surcharge += energy_charge * HIGH_USAGE_SURCHARGE_RATE
        if is_late:
            surcharge += (energy_charge + FIXED_CHARGE) * LATE_FEE_RATE

        rebate = 0.0
        if has_solar and units > 0:
            rebate = energy_charge * SOLAR_REBATE_RATE

        net_bill = round(energy_charge + FIXED_CHARGE + surcharge - rebate, 2)

        # Compare against previous valid month
        alert_msg = "Normal"
        if prev_bill is not None and prev_bill > 0:
            diff = net_bill - prev_bill
            pct_change = (diff / prev_bill) * 100.0
            if pct_change > UNUSUAL_PCT_INCREASE or diff > UNUSUAL_AMT_INCREASE:
                alert_msg = f"UNUSUAL (+{pct_change:.1f}%, +Rs.{diff:.2f} vs {prev_month})"
                unusual_months.append((month_name, prev_month, pct_change, diff))
        elif prev_bill == 0 and net_bill > UNUSUAL_AMT_INCREASE:
            alert_msg = f"UNUSUAL (+Rs.{net_bill:.2f} from zero)"
            unusual_months.append((month_name, prev_month, 100.0, net_bill))

        print(
            f"{month_name:<10} {units:>6} {energy_charge:>9.2f} {FIXED_CHARGE:>7.2f} "
            f"{surcharge:>8.2f} {rebate:>8.2f} {net_bill:>10.2f}  {alert_msg}"
        )

        valid_bills.append(net_bill)
        valid_months.append(month_name)
        total_net_bill += net_bill
        total_units += units
        if net_bill > highest_bill:
            highest_bill = net_bill
            highest_month = month_name

        prev_bill = net_bill
        prev_month = month_name

    # Summary for household
    print("-" * 72)
    valid_count = len(valid_bills)
    if valid_count > 0:
        avg_bill = total_net_bill / valid_count
        print(f"Valid Months Processed : {valid_count}")
        print(f"Total Units Consumed   : {total_units} kWh")
        print(f"Total Net Billing      : Rs. {total_net_bill:.2f}")
        print(f"Average Monthly Bill   : Rs. {avg_bill:.2f}")
        print(f"Peak Bill Month        : {highest_month} (Rs. {highest_bill:.2f})")
        print(f"Unusual Increases      : {len(unusual_months)}")
        for u_month, p_month, pct, diff in unusual_months:
            print(
                f"   -> {u_month} jumped by Rs. {diff:.2f} ({pct:.1f}%) compared to {p_month}"
            )
    else:
        print("No valid billing records found.")

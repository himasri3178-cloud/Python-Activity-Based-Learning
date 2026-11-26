# Case Study 06: Railway Fare and Reservation Calculator
# Syllabus topics used: variables, data types, operators, conditional statements,
# loops, strings, lists, tuples, tuple unpacking

print("=" * 78)
print("         CASE STUDY 06: RAILWAY FARE AND RESERVATION CALCULATOR")
print("=" * 78)

# Passenger booking records (test cases covering slabs, classes, age, cancellations, invalid inputs)
# Tuple format:
# (pnr, passenger_name, age, travel_class, distance_km, status, hours_before_departure)
bookings = [
    ("PNR01", "Aarav Sharma", 28, "3A", 450, "CONFIRMED", 0),
    ("PNR02", "Meera Nair", 65, "2A", 820, "CONFIRMED", 0),
    ("PNR03", "Rohan Verma", 8, "SL", 250, "CONFIRMED", 0),
    ("PNR04", "Baby Ananya", 3, "1A", 600, "CONFIRMED", 0),
    ("PNR05", "Kiran Rao", 34, "2A", 520, "CANCELLED", 60),
    ("PNR06", "Sneha Iyer", 62, "3A", 350, "CANCELLED", 20),
    ("PNR07", "Vikram Das", 41, "SL", 180, "CANCELLED", 6),
    ("PNR08", "Invalid Test", -4, "SL", 100, "CONFIRMED", 0),
    ("PNR09", "Bad Class", 25, "VIP", 200, "CONFIRMED", 0),
]

total_collected = 0.0
total_refunded = 0.0
confirmed_count = 0
cancelled_count = 0
rejected_count = 0

print(
    f"{'PNR':<6} {'Name':<14} {'Age':>3} {'Cls':<4} {'Dist':>5} "
    f"{'Gross':>8} {'Conc':>8} {'ResFee':>7} {'Net/Pen':>9}  {'Status / Remarks'}"
)
print("-" * 78)

for booking in bookings:
    pnr, name, age, travel_class, distance, status, hours_before = booking

    # Validate inputs
    if age < 0 or age > 120:
        print(f"{pnr:<6} {name:<14} {age:>3} {travel_class:<4} {distance:>5}   INVALID AGE")
        rejected_count += 1
        continue
    if distance <= 0:
        print(f"{pnr:<6} {name:<14} {age:>3} {travel_class:<4} {distance:>5}   INVALID DISTANCE")
        rejected_count += 1
        continue
    if travel_class not in ("SL", "3A", "2A", "1A"):
        print(f"{pnr:<6} {name:<14} {age:>3} {travel_class:<4} {distance:>5}   INVALID CLASS")
        rejected_count += 1
        continue

    # Distance slab base fare (Sleeper base rate per km)
    # 1 - 100 km   : Rs. 1.20 / km
    # 101 - 300 km : Rs. 1.00 / km
    # 301 - 600 km : Rs. 0.85 / km
    # > 600 km     : Rs. 0.70 / km
    base_fare = 0.0
    rem = distance
    if rem > 600:
        base_fare += (rem - 600) * 0.70
        rem = 600
    if rem > 300:
        base_fare += (rem - 300) * 0.85
        rem = 300
    if rem > 100:
        base_fare += (rem - 100) * 1.00
        rem = 100
    if rem > 0:
        base_fare += rem * 1.20

    # Travel class multiplier and fixed reservation fee
    if travel_class == "SL":
        multiplier = 1.0
        res_fee = 20.0
    elif travel_class == "3A":
        multiplier = 2.2
        res_fee = 40.0
    elif travel_class == "2A":
        multiplier = 3.2
        res_fee = 50.0
    else:  # "1A"
        multiplier = 5.0
        res_fee = 60.0

    class_fare = base_fare * multiplier

    # Age-based concession
    # Age < 5         : 100% free (no ticket/reservation fee)
    # Age 5 to 11     : 50% concession on class fare
    # Age >= 60       : 40% concession on class fare
    # Age 12 to 59    : 0% concession
    if age < 5:
        concession = class_fare
        res_fee = 0.0
        conc_note = "Infant Free"
    elif age <= 11:
        concession = class_fare * 0.50
        conc_note = "Child 50%"
    elif age >= 60:
        concession = class_fare * 0.40
        conc_note = "Senior 40%"
    else:
        concession = 0.0
        conc_note = "Regular"

    ticket_total = round((class_fare - concession) + res_fee, 2)

    if status == "CONFIRMED":
        confirmed_count += 1
        total_collected += ticket_total
        print(
            f"{pnr:<6} {name:<14} {age:>3} {travel_class:<4} {distance:>5} "
            f"{class_fare:>8.2f} {concession:>8.2f} {res_fee:>7.2f} {ticket_total:>9.2f}  "
            f"CONFIRMED ({conc_note})"
        )
    elif status == "CANCELLED":
        cancelled_count += 1
        # Cancellation penalty rules:
        # >= 48 hours : flat Rs. 60 clerkage (or full ticket if less than 60)
        # 12 - 47 hrs : 25% of ticket total
        # 1 - 11 hrs  : 50% of ticket total
        # <= 0 hrs    : 100% (no refund)
        if age < 5:
            penalty = 0.0
        elif hours_before >= 48:
            penalty = 60.0 if ticket_total >= 60.0 else ticket_total
        elif hours_before >= 12:
            penalty = round(ticket_total * 0.25, 2)
        elif hours_before > 0:
            penalty = round(ticket_total * 0.50, 2)
        else:
            penalty = ticket_total

        refund = round(ticket_total - penalty, 2)
        total_collected += penalty
        total_refunded += refund
        print(
            f"{pnr:<6} {name:<14} {age:>3} {travel_class:<4} {distance:>5} "
            f"{class_fare:>8.2f} {concession:>8.2f} {res_fee:>7.2f} {penalty:>9.2f}  "
            f"CANCELLED ({hours_before}h, Refund Rs.{refund:.2f})"
        )
    else:
        rejected_count += 1
        print(f"{pnr:<6} {name:<14} {age:>3} {travel_class:<4} {distance:>5}   INVALID STATUS")

print("-" * 78)
print(f"Confirmed Bookings : {confirmed_count}")
print(f"Cancelled Bookings : {cancelled_count}")
print(f"Rejected Records   : {rejected_count}")
print(f"Total Net Revenue  : Rs. {total_collected:.2f}")
print(f"Total Refunded     : Rs. {total_refunded:.2f}")

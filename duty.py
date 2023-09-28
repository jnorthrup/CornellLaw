import sys

def calculate_stamp_duty(transaction_amount, conveyance=False):
    duty = 0
    if conveyance:
        if transaction_amount <= 1000:
            return 0.25
        elif transaction_amount <= 2500:
            return 2.00
        elif transaction_amount <= 5000:
            return 5.00
        elif transaction_amount <= 10000:
            return 10.00
        elif transaction_amount <= 20000:
            return 20.00
        else:
            excess_amount = transaction_amount - 20000
            increments = excess_amount / 10000
            increments = int(-(-increments // 1))
            additional_duty = increments * 20.00
            return 20.00 + additional_duty
    else:
        excess_amount = transaction_amount - 7500
        if excess_amount > 0:
            increments = excess_amount / 2500
            increments = int(-(-increments // 1))
            additional_duty = increments * 0.30
            duty += additional_duty
    return duty

def calculate_duty_stamps(duty):
    available_stamps = [1, 2, 3, 5, 10, 100, 200, 500, 1000]
    duty_cents = int(duty * 100)
    stamp_count = {}
    for stamp in reversed(available_stamps):
        count, duty_cents = divmod(duty_cents, stamp)
        if count > 0:
            stamp_value = stamp / 100 if stamp >= 100 else stamp
            stamp_count[stamp_value] = count
    return stamp_count

if __name__ == "__main__":
    transaction_amount = 62000  # default
    conveyance = False

    if len(sys.argv) > 1:
        transaction_amount = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2].lower() == 'conveyance':
        conveyance = True

    duty = calculate_stamp_duty(transaction_amount, conveyance)
    print(f"Stamp duty for ${transaction_amount} is ${duty:.2f}")
    stamps = calculate_duty_stamps(duty)
    
    print("Exact change in stamps:")
    for stamp, count in stamps.items():
        print(f"{count} x ${stamp if stamp >= 1 else f'{stamp:.2f}'} stamp(s)")
        c
# Duty calculation for conveyance
def conveyance_duty(amount):
    if amount <= 1000:
        return 0.25
    elif amount <= 5000:
        return 0.5
    elif amount <= 10000:
        return 1.0
    elif amount <= 25000:
        return 2.0
    elif amount <= 50000:
        return 5.0
    elif amount <= 100000:
        return 10.0
    else:
        return 20.0 + 10.0 * ((amount - 100000) // 10000)

# Duty calculation for insurance
def insurance_duty(amount, type="life"):
    if type == "life":
        if amount <= 1000:
            return 0.25
        elif amount <= 5000:
            return 0.5
        else:
            return 1.0
    else:  # marine, inland, fire etc.
        return 0.25

# Duty calculation for lease
def lease_duty(years):
    if years <= 3:
        return 0.5
    else:
        return 1.0

# Duty calculation for mortgage
def mortgage_duty(amount):
    if amount <= 500:
        return 0.5
    elif amount <= 1000:
        return 1.0
    elif amount <= 2500:
        return 2.0
    elif amount <= 5000:
        return 5.0
    elif amount <= 10000:
        return 10.0
    else:
        return 15.0 + 10.0 * ((amount - 10000) // 10000)

# Duty calculation for medicine or preparation
def medicine_duty(retail_price):
    if retail_price <= 0.25:
        return 0.01
    elif retail_price <= 0.5:
        return 0.02
    else:
        return 0.05  # Assuming 5 cents for prices above 50 cents

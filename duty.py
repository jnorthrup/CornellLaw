import sys


## 1863 stamp duty on instruments
# conveyance duty
def conveyance_duty(property_value: float) -> float:
    """
    Calculate the stamp duty for conveyances based on the value.

    Args:
    - value (float): The consideration or value of the property being conveyed.

    Returns:
    - float: The stamp duty based on the conveyance scale.
    """
    if property_value <= 100:
        raise ValueError("Property value must be greater than 100 dollars.")
    elif property_value <= 500:
        fee = 0.50
    elif property_value <= 1000:
        fee = 1.00
    elif property_value <= 2500:
        fee = 2.00
    elif property_value <= 5000:
        fee = 5.00
    elif property_value <= 10000:
        fee = 10.00
    elif property_value <= 20000:
        fee = 20.00
    else:
        fee = 20.00 + 20.00 * ((property_value - 20000) // 10000)
        if (property_value - 20000) % 10000 > 0:
            fee += 20.00  # Adding fee for the fractional part exceeding 10,000 increments

    return fee

# # Example
# property_value = float(input("Enter the value of the property: "))
# duty = conveyance_duty(property_value)
# print(f"The stamp duty for a property valued at ${property_value} is ${duty:.2f}.")

def bill_of_exchange_inland(value: float) -> float:
    """
    Calculate the stamp duty for Inland Bills of Exchange based on the value.

    Args:
    - value (float): The amount of the bill.

    Returns:
    - float: The stamp duty based on the bill value.
    """
    if value <= 20:
        return 0.02
    if value <= 100:
        return 0.05
    if value <= 200:
        return 0.10
    if value <= 300:
        return 0.15
    if value <= 500:
        return 0.20
    if value <= 750:
        return 0.30
    if value <= 1000:
        return 0.40
    return 0.60


def bill_of_exchange_foreign(value: float, set_count: int = 1) -> float:
    """
    Calculate the stamp duty for Foreign Bills of Exchange based on the value.

    Args:
    - value (float): The amount of the bill.
    - set_count (int): Number of sets for the bill.

    Returns:
    - float: The stamp duty based on the bill value.
    """
    if set_count >= 3 and value < 100:
        return 0.03 * set_count
    if value <= 150:
        return 0.05 * set_count
    if value <= 200:
        return 0.10 * set_count
    if value <= 300:
        return 0.15 * set_count
    if value <= 500:
        return 0.20 * set_count
    if value <= 750:
        return 0.30 * set_count
    if value <= 1000:
        return 0.40 * set_count
    if value <= 3500:
        return 0.50 * set_count
    if value <= 5000:
        return 0.75 * set_count
    return 1.00 * set_count


#######
## main block, accept value, and optional paramter 2, duty type (0,1,2) for conveyance, inland, foreign,
## and print the result total duty and a suggested purchase of stamps denominated in 1,5,10,50,100,500,1000,5000,10000 cent denominations, to arrive at stamp duty
#######

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python duty.py <value> [type] 0=conveyance, 1=inland, 2=foreign")
        sys.exit(1)

    value = float(sys.argv[1])
    duty_type = 0
    if len(sys.argv) == 3:
        duty_type = int(sys.argv[2])

    if duty_type == 0:
        duty = conveyance_duty(value)
    elif duty_type == 1:
        duty = bill_of_exchange_inland(value)
    elif duty_type == 2:
        duty = bill_of_exchange_foreign(value)
    else:
        print("Invalid duty type")
        sys.exit(1)

    # for each denom below, perform a coin sorter result to present the minimum stamps of exact change
    # displayed each as dollars amount and number of stamps

    denom = sorted([1, 5, 10, 50,   100, 500, 1000, 2875], reverse=True)


    def coin_sorter(v, denom):
        result = {}
        for i in denom:
            if v >= i:
                result[i] = v // i
                v = v % i
        return result

    # print the result of the coin sorter in a more readable format, as USD from cent units
    def print_coin_sorter(v, denom):
        result = coin_sorter(v, denom)
        for i in result:
            print(f"{i / 100:6.2f} x {result[i] } = {i / 100 * result[i]:6.2f}")
        print(f"Total: {sum([i / 100 * result[i] for i in result]):6.2f}")
        return result

    print(f"The stamp duty for a bill valued at ${value:.2f} is ${duty:.2f}.")
    print_coin_sorter(duty * 100, denom)


"""Reusable input and display helpers."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def text_input(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Value cannot be empty.")

def integer_input(label, minimum=0):
    while True:
        try:
            value = int(input(label).strip())
            if value >= minimum:
                return value
        except ValueError:
            pass
        print(f"Enter a whole number of at least {minimum}.")

def money_input(label, minimum=0):
    while True:
        try:
            value = Decimal(input(label).strip())
            if value.is_finite() and value >= Decimal(str(minimum)):
                return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        except (InvalidOperation, ValueError):
            pass
        print(f"Enter a valid amount of at least {minimum}.")

def choose(title, options):
    print("\n" + title)
    for index, option in enumerate(options, 1):
        print(f"{index}. {option}")
    while True:
        selection = integer_input("Choose: ", 1)
        if selection <= len(options):
            return selection
        print("Invalid menu choice.")

def find_by_id(records, record_id):
    return next((record for record in records if int(record["id"]) == record_id), None)

def show_records(records):
    if not records:
        print("No records found.")
    else:
        for record in records:
            print(" | ".join(f"{key}: {value}" for key, value in record.items()))

def optional_text(label, old):
    value = input(f"{label} [{old}] (Enter to keep): ").strip()
    return value if value else old


def phone_input(label="Phone number: ", current=None):
    """Validate and verify a phone number: exactly 10 ASCII digits."""
    while True:
        value = input(label).strip()
        if current is not None and not value:
            return current
        if len(value) == 10 and value.isascii() and value.isdigit():
            return value  # Keep as text to preserve leading zeroes.
        print("Invalid phone number! Enter exactly 10 digits (0-9).")

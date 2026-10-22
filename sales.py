"""Sales, invoices, payments, and automatic stock deduction."""
from datetime import date
from decimal import Decimal
from storage import load_json, save_json, next_id
from utils import choose, integer_input, money_input, find_by_id, show_records

def rounded(value):
    return float(Decimal(str(value)).quantize(Decimal("0.01")))

def create_sale():
    customers = load_json("customers")
    customer = find_by_id(customers, integer_input("Customer ID: ", 1))
    if not customer:
        print("Customer not found. Add the customer first.")
        return
    items = load_json("inventory")
    show_records(items)
    item = find_by_id(items, integer_input("Item ID: ", 1))
    if not item:
        print("Item not found.")
        return
    quantity = integer_input("Quantity: ", 1)
    if quantity > item["stock"]:
        print("Insufficient stock. Sale cancelled.")
        return
    total = rounded(Decimal(str(item["price"])) * quantity)
    print(f"Total bill: {total:.2f}")
    while True:
        paid = money_input("Initial payment (0 for unpaid): ")
        if paid <= total:
            break
        print("Payment cannot exceed total bill.")
    records = load_json("sales")
    record = {"id": next_id(records), "date": date.today().isoformat(),
              "customer_id": customer["id"], "customer_name": customer["name"],
              "item_id": item["id"], "item_name": item["name"],
              "quantity": quantity, "unit_price": item["price"],
              "total": total, "paid": paid, "due": rounded(Decimal(str(total)) - Decimal(str(paid)))}
    # Save both changed files after all validation succeeds.
    item["stock"] -= quantity
    save_json("inventory", items)
    records.append(record)
    save_json("sales", records)
    print("Invoice created:")
    show_records([record])

def view_sales():
    show_records(load_json("sales"))

def receive_payment():
    records = load_json("sales")
    record = find_by_id(records, integer_input("Invoice ID: ", 1))
    if not record:
        print("Invoice not found.")
        return
    if record["due"] <= 0:
        print("Invoice is already fully paid.")
        return
    print(f"Outstanding: {record['due']:.2f}")
    while True:
        amount = money_input("Payment amount: ", 0.01)
        if amount <= record["due"]:
            break
        print("Payment cannot exceed outstanding balance.")
    record["paid"] = rounded(Decimal(str(record["paid"])) + Decimal(str(amount)))
    record["due"] = rounded(Decimal(str(record["total"])) - Decimal(str(record["paid"])))
    save_json("sales", records)
    print(f"Payment received. Remaining due: {record['due']:.2f}")

def menu(role="admin"):
    actions = [create_sale, view_sales, receive_payment]
    while True:
        choice = choose("SALES & INVOICES", ["Create sale / invoice", "View all sales and invoices", "Receive pending payment", "Back"])
        if choice == 4:
            return
        actions[choice - 1]()

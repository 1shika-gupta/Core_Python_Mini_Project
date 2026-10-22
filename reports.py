"""Expenses and simple business summary."""
from datetime import date
from decimal import Decimal
from storage import load_json, load_csv, append_csv, next_id
from utils import choose, text_input, money_input, show_records

def add_expense():
    records = load_csv("expenses")
    record = {"id": next_id(records), "date": date.today().isoformat(),
              "category": text_input("Category: "),
              "description": text_input("Description: "),
              "amount": f"{money_input('Amount: '):.2f}"}
    append_csv("expenses", record)
    print("Expense recorded:", record["id"])

def view_expenses():
    show_records(load_csv("expenses"))

def calculate_totals():
    sales = load_json("sales")
    expenses = load_csv("expenses")
    total_sales = sum((Decimal(str(r["total"])) for r in sales), Decimal("0"))
    payments = sum((Decimal(str(r["paid"])) for r in sales), Decimal("0"))
    dues = sum((Decimal(str(r["due"])) for r in sales), Decimal("0"))
    total_expenses = sum((Decimal(str(r["amount"])) for r in expenses), Decimal("0"))
    return total_sales, payments, dues, total_expenses

def summary():
    sales, payments, dues, expenses = calculate_totals()
    print("\nBUSINESS SUMMARY (all-time)")
    print(f"Total sales:             {sales:.2f}")
    print(f"Total payments received: {payments:.2f}")
    print(f"Outstanding dues:        {dues:.2f}")
    print(f"Total expenses:          {expenses:.2f}")

def menu(role="admin"):
    actions = [add_expense, view_expenses, summary]
    labels = ["Record expense", "View expenses", "Business summary"]
    if role != "admin":
        actions = [view_expenses, summary]
        labels = ["View expenses", "Business summary"]
    while True:
        choice = choose("EXPENSES & REPORTS", labels + ["Back"])
        if choice == len(labels) + 1:
            return
        actions[choice - 1]()

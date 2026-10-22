"""Inventory and stock management."""
from storage import load_json, save_json, next_id
from utils import choose, text_input, integer_input, money_input, find_by_id, show_records, optional_text

def add_item():
    records = load_json("inventory")
    record = {"id": next_id(records), "name": text_input("Item name: "),
              "price": money_input("Unit price: "), "stock": integer_input("Opening stock: "),
              "low_stock_limit": integer_input("Low stock threshold: ")}
    records.append(record)
    save_json("inventory", records)
    print("Item added:", record["id"])

def view_items():
    show_records(load_json("inventory"))

def search_item():
    record = find_by_id(load_json("inventory"), integer_input("Item ID: ", 1))
    show_records([record] if record else [])

def update_item():
    records = load_json("inventory")
    record = find_by_id(records, integer_input("Item ID: ", 1))
    if not record:
        print("Item not found.")
        return
    record["name"] = optional_text("Name", record["name"])
    print("Current price:", record["price"])
    if choose("Change price?", ["Yes", "No"]) == 1:
        record["price"] = money_input("New price: ")
    if choose("Change low-stock threshold?", ["Yes", "No"]) == 1:
        record["low_stock_limit"] = integer_input("New threshold: ")
    save_json("inventory", records)
    print("Item updated. Use stock adjustment to change quantity.")

def adjust_stock():
    records = load_json("inventory")
    record = find_by_id(records, integer_input("Item ID: ", 1))
    if not record:
        print("Item not found.")
        return
    direction = choose("STOCK ADJUSTMENT", ["Add stock", "Remove stock", "Back"])
    if direction == 3:
        return
    amount = integer_input("Quantity: ", 1)
    if direction == 2 and amount > record["stock"]:
        print("Insufficient stock.")
        return
    record["stock"] += amount if direction == 1 else -amount
    save_json("inventory", records)
    print("New stock:", record["stock"])

def low_stock():
    records = load_json("inventory")
    show_records([r for r in records if r["stock"] <= r["low_stock_limit"]])

def menu(role="admin"):
    actions = [add_item, view_items, search_item, update_item, adjust_stock, low_stock]
    labels = ["Add item", "View all items", "Search by ID", "Update item", "Add/remove stock", "Low-stock alerts"]
    if role != "admin":
        actions = [view_items, search_item, low_stock]
        labels = ["View all items", "Search by ID", "Low-stock alerts"]
    while True:
        choice = choose("INVENTORY / STOCK", labels + ["Back"])
        if choice == len(labels) + 1:
            return
        actions[choice - 1]()

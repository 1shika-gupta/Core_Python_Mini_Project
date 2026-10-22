"""Customer CRUD operations."""
from storage import load_json, save_json, next_id
from utils import choose, text_input, integer_input, find_by_id, show_records, optional_text, phone_input

def add_customer():
    records = load_json("customers")
    record = {"id": next_id(records), "name": text_input("Name: "),
              "phone": phone_input("Phone (10 digits): "), "address": text_input("Address: ")}
    records.append(record)
    save_json("customers", records)
    print("Customer added:", record["id"])

def view_customers():
    show_records(load_json("customers"))

def search_customer():
    record = find_by_id(load_json("customers"), integer_input("Customer ID: ", 1))
    show_records([record] if record else [])

def update_customer():
    records = load_json("customers")
    record = find_by_id(records, integer_input("Customer ID: ", 1))
    if not record:
        print("Customer not found.")
        return
    for field in ("name", "phone", "address"):
        record[field] = (phone_input("Phone (10 digits) [Enter to keep]: ", record[field])
                         if field == "phone" else optional_text(field.title(), record[field]))
    save_json("customers", records)
    print("Customer updated.")

def delete_customer():
    records = load_json("customers")
    customer_id = integer_input("Customer ID: ", 1)
    if not find_by_id(records, customer_id):
        print("Customer not found.")
        return
    if any(int(sale["customer_id"]) == customer_id for sale in load_json("sales")):
        print("Cannot delete a customer with sales history.")
        return
    save_json("customers", [record for record in records if record["id"] != customer_id])
    print("Customer deleted.")


def search_customer_by_name():
    query = text_input("Customer name (full or partial): ").casefold()
    records = load_json("customers")
    show_records([r for r in records if query in r["name"].casefold()])

def search_customer_by_phone():
    phone = phone_input("Customer phone (10 digits): ")
    show_records([r for r in load_json("customers") if r["phone"] == phone])

def menu(role="admin"):
    actions = [add_customer, view_customers, search_customer, search_customer_by_name,
               search_customer_by_phone, update_customer, delete_customer]
    labels = ["Add customer", "View all customers", "Search by ID", "Search by name",
              "Search by contact number", "Update customer", "Delete customer"]
    if role != "admin":
        actions = actions[1:5]
        labels = labels[1:5]
    while True:
        choice = choose("CUSTOMER MANAGEMENT", labels + ["Back"])
        if choice == len(labels) + 1:
            return
        actions[choice - 1]()

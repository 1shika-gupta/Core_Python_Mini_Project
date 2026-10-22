"""Employee records and daily attendance."""
from datetime import date, datetime
from storage import load_json, save_json, next_id, load_csv, append_csv
from utils import choose, text_input, integer_input, find_by_id, show_records, phone_input

def add_employee():
    records = load_json("employees")
    record = {"id": next_id(records), "name": text_input("Name: "),
              "role": text_input("Role: "), "phone": phone_input("Phone (10 digits): ")}
    records.append(record)
    save_json("employees", records)
    print("Employee added:", record["id"])

def view_employees():
    show_records(load_json("employees"))

def search_employee():
    record = find_by_id(load_json("employees"), integer_input("Employee ID: ", 1))
    show_records([record] if record else [])

def date_input():
    while True:
        value = input("Date YYYY-MM-DD (Enter for today): ").strip() or date.today().isoformat()
        try:
            if datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d") == value:
                return value
        except ValueError:
            pass
        print("Invalid date. Use YYYY-MM-DD.")

def mark_attendance():
    employee_id = integer_input("Employee ID: ", 1)
    if not find_by_id(load_json("employees"), employee_id):
        print("Employee not found.")
        return
    day = date_input()
    if any(int(r["employee_id"]) == employee_id and r["date"] == day for r in load_csv("attendance")):
        print("Attendance already marked for this employee on this date.")
        return
    status = "Present" if choose("Attendance", ["Present", "Absent"]) == 1 else "Absent"
    append_csv("attendance", {"employee_id": employee_id, "date": day, "status": status})
    print("Attendance saved.")

def view_attendance():
    day = date_input()
    show_records([r for r in load_csv("attendance") if r["date"] == day])

def menu(role="admin"):
    actions = [add_employee, view_employees, search_employee, mark_attendance, view_attendance]
    labels = ["Add employee", "View employees", "Search by ID", "Mark attendance", "View attendance by date"]
    if role != "admin":
        actions = actions[1:]
        labels = labels[1:]
    while True:
        choice = choose("EMPLOYEES & ATTENDANCE", labels + ["Back"])
        if choice == len(labels) + 1:
            return
        actions[choice - 1]()

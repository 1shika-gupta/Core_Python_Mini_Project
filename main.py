"""Entry point for the Small Business ERP CLI."""
import customers
import sales
import inventory
import employees
import reports
import auth
from storage import initialize
from utils import choose


def main():
    initialize()
    auth.setup_admin()
    user = auth.login()
    if user is None:
        return
    actions = [customers.menu, sales.menu, inventory.menu, employees.menu, reports.menu]
    labels = ["Customer Management", "Sales & Invoices", "Inventory / Stock",
              "Employees & Attendance", "Expenses & Reports"]
    if user["role"] == "admin":
        actions.append(lambda role: auth.manage_users())
        labels.append("Admin - Manage User Accounts")
    while True:
        choice = choose("# SMALL BUSINESS ERP\n==============================", labels + ["Exit"])
        if choice == len(labels) + 1:
            print("Goodbye!")
            return
        actions[choice - 1](user["role"])


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
    except (OSError, ValueError) as error:
        print("Data file error:", error)

# Small Business ERP — Python CLI Mini Project

A beginner-friendly college project with **five modules**, using only Python's standard library. Data persists in JSON and CSV files. No database or pip install is required.

## Requirements
- Python 3.9 or newer
- Visual Studio Code (optional, recommended)

## Open and run in VS Code
1. Extract `Small_Business_ERP_CLI.zip`.
2. Open **Visual Studio Code**.
3. Choose **File → Open Folder** and select `Small_Business_ERP_CLI`.
4. Open **Terminal → New Terminal**.
5. Check that the terminal is inside `Small_Business_ERP_CLI` (run `cd Small_Business_ERP_CLI` if needed).
6. Run `python main.py` (on some systems use `python3 main.py` or Windows `py main.py`).
7. Enter the menu number, then follow the prompts. Select **Back** to return to the main menu.

File paths use the location of `storage.py`, so the program also works if launched from another working directory.

## Files explained for viva
| File | Purpose |
|---|---|
| `main.py` | Entry point and main menu |
| `customers.py` | Add, list, search, update and delete customers |
| `sales.py` | Create invoices, reduce stock, collect full/partial payments |
| `inventory.py` | Manage items, stock quantities and low-stock alerts |
| `employees.py` | Store employees and prevent duplicate daily attendance |
| `reports.py` | Record expenses and calculate business totals |
| `storage.py` | Initialize and read/write JSON and CSV files |
| `utils.py` | Shared validation, menus, record search and display |
| `data/` | Persistent JSON/CSV records |

## Storage and IDs
Customer, employee, item and invoice records are JSON lists. Attendance and expenses are CSV tables. IDs are generated as `max(existing IDs) + 1` within each collection. Deleting the highest-ID customer can therefore reuse that ID later if no customer sales exist. Existing customers with sales cannot be deleted to preserve invoice references. All reports show all-time totals; payments are stored cumulatively per invoice (not as individual payment transactions).

## Sample demonstration (enter through the menus)
1. Customer Management → Add customer: name `Asha`, phone `9876543210`, address `Mumbai` → customer ID `1`.
2. Inventory → Add item: name `Notebook`, price `50`, stock `10`, low-stock threshold `3` → item ID `1`.
3. Sales → Create sale: customer `1`, item `1`, quantity `3`, initial payment `100` → invoice total `150`, paid `100`, due `50`; remaining stock `7`.
4. Sales → Receive pending payment: invoice `1`, payment `20` → paid `120`, due `30`.
5. Employees → Add employee: name `Ravi`, role `Cashier`, phone `9999999999` → employee ID `1`; mark Present for today's date. Repeating the same date is blocked.
6. Expenses → Record expense: category `Rent`, description `Shop rent`, amount `40`.
7. Expenses → Business summary:

```text
BUSINESS SUMMARY (all-time)
Total sales:             150.00
Total payments received: 120.00
Outstanding dues:        30.00
Total expenses:          40.00
```

Try selling 8 more notebooks after step 3: the system rejects the sale because only 7 remain.

## Reset demonstration data
To start a new demonstration, close the app, change each JSON file in `data/` to `[]`, and leave only the CSV header lines in `attendance.csv` and `expenses.csv`. Do not delete source files.

## Design notes
- Prices and payments are validated as nonnegative, with two decimal places.
- Stock is never allowed below zero.
- Sale stock updates and invoice writes are separate file operations; this educational CLI is intended for single-user local use, not concurrent or crash-safe accounting.
- No payroll, authentication, database, GUI or third-party dependencies.

## Updated: Administrator / Staff Roles and Customer Contact Validation

On the **first run**, the application prompts you to create an administrator username and password (at least six characters). There is **no default password**. Sign in with this account on subsequent runs. Account records are stored in `data/users.json`; passwords are stored as salted PBKDF2 hashes, not plain text. This is a simple local demonstration login, not a production security system.

**Administrator** can use all five modules, including adding/updating/deleting customers, managing inventory, adding employees, recording expenses, and the additional **Admin - Manage User Accounts** menu. From there the administrator can add staff users and view usernames and roles.

**Staff** can view and search customers (including by name or phone), create sales and receive payments, view inventory, mark/view attendance, and view expenses and reports. Staff cannot edit customer records, inventory, employee records, expenses, or user accounts.

Customer Management now includes **Search by name** (case-insensitive, partial matches allowed) and **Search by contact number** (exact 10 digits). Customer and employee phone numbers must contain **exactly 10 digits (0-9)**. Invalid numbers show a message and are requested again. Customer phone edits also use this validation. All customer records are stored persistently in `data/customers.json`.

### Example validation

```text
Phone (10 digits): 12345
Invalid phone number! Enter exactly 10 digits (0-9).
Phone (10 digits): 9876543210
Customer added: 1
```

### Running

Extract the ZIP, open `Small_Business_ERP_CLI` with **VS Code → File → Open Folder**, open **Terminal → New Terminal**, and run `python main.py` (or `python3 main.py`). Complete first-time admin setup, log in, and choose a menu option.

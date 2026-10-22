"""File storage helpers; paths are relative to this project."""
import csv
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
JSON_FILES = ("customers", "employees", "inventory", "sales", "users")
CSV_FIELDS = {"attendance": ["employee_id", "date", "status"],
              "expenses": ["id", "date", "category", "description", "amount"]}

def initialize():
    DATA.mkdir(exist_ok=True)
    for name in JSON_FILES:
        path = DATA / (name + ".json")
        if not path.exists():
            path.write_text("[]\n", encoding="utf-8")
    for name, fields in CSV_FIELDS.items():
        path = DATA / (name + ".csv")
        if not path.exists():
            with path.open("w", newline="", encoding="utf-8") as file:
                csv.writer(file).writerow(fields)

def load_json(name):
    with (DATA / (name + ".json")).open(encoding="utf-8") as file:
        return json.load(file)

def save_json(name, records):
    with (DATA / (name + ".json")).open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)

def load_csv(name):
    with (DATA / (name + ".csv")).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def append_csv(name, record):
    with (DATA / (name + ".csv")).open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS[name])
        writer.writerow(record)

def next_id(records):
    return max((int(record["id"]) for record in records), default=0) + 1

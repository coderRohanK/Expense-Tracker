import sqlite3
from datetime import datetime

DB = "expenses.db"


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            category TEXT,
            amount REAL
        );
    """)

    con.commit()
    con.close()



def log_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    date = datetime.now().strftime("%Y-%m-%d")

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                (amount, category, date))
    con.commit()
    con.close()

    check_budget(category)
    print("Expense Added.\n")


def set_budget():
    month = input("Enter month (YYYY-MM): ")
    category = input("Category: ")
    amount = float(input("Budget amount: "))

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO budgets (month, category, amount) VALUES (?, ?, ?)",
                (month, category, amount))
    con.commit()
    con.close()

    print("Budget Saved.\n")


def check_budget(category):
    month = datetime.now().strftime("%Y-%m")

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("SELECT amount FROM budgets WHERE month=? AND category=?",
                (month, category))
    row = cur.fetchone()

    if row:
        budget = row[0]

        cur.execute("""
            SELECT SUM(amount) FROM expenses
            WHERE category=? AND strftime('%Y-%m', date)=?
        """, (category, month))

        spent = cur.fetchone()[0] or 0

        if spent > budget:
            print("⚠ ALERT: You exceeded the budget for", category)

    con.close()



def total_spending():
    month = input("Enter month (YYYY-MM): ")

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE strftime('%Y-%m', date)=?
    """, (month,))

    total = cur.fetchone()[0] or 0
    print(f"Total spent in {month}: ₹{total}\n")

    con.close()


def compare_budget():
    month = input("Enter month (YYYY-MM): ")

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE strftime('%Y-%m', date)=?
        GROUP BY category
    """, (month,))

    rows = cur.fetchall()

    print("\nCategory | Spent | Budget")
    print("--------------------------")

    for cat, spent in rows:
        cur.execute("""
            SELECT amount FROM budgets
            WHERE month=? AND category=?
        """, (month, cat))
        row = cur.fetchone()
        budget = row[0] if row else 0

        print(f"{cat} | {spent} | {budget}")

    print()
    con.close()



def main():
    init_db()
    while True:
        print("1. Log Expense")
        print("2. Set Budget")
        print("3. Total Spending (Monthly)")
        print("4. Compare Spending vs Budget")
        print("5. Exit")

        choice = input("Choice: ")

        if choice == "1":
            log_expense()
        elif choice == "2":
            set_budget()
        elif choice == "3":
            total_spending()
        elif choice == "4":
            compare_budget()
        elif choice == "5":
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()

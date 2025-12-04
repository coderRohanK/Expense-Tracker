Expense Tracker – Python Application

This is a simple Python console-based application that helps users track daily expenses and set monthly budgets for different categories.
The app stores data using SQLite and provides basic financial reports.


Features
1. Log Daily Expenses
Enter amount
Enter category (Food, Transport, Entertainment, etc.)
Automatically stores date

2. Categorized Expenses
Every expense is grouped under a category

3. Set Monthly Budgets
Set a budget for each category
Stored as Month + Category + Budget Amount

4. Budget Alerts
System alerts when spending exceeds the category budget for the current month

5. Basic Reports
Total Spending Per Month
Category-wise Spending vs Budget Comparison



Project Structure

main.py

expenses.db   (auto-created)

README.md


How to Run the Application

1. Install Python (3.x)
Make sure Python is installed on your system.
2. Run the Application
python main.py

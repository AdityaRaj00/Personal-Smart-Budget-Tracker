# -----------------------------------------------------------------------------
# Personal Budget Tracker CLI
# -----------------------------------------------------------------------------
# A command-line tool for managing personal finances by tracking expenses
# against user-defined categories and budgets.
#
# Features:
# - Category and budget creation
# - Transaction logging
# - Data persistence via JSON files
# - Weekly and monthly visual spending reports with Matplotlib
# -----------------------------------------------------------------------------

import json
from datetime import date, timedelta
import matplotlib.pyplot as plt

class Transaction:
    """Represents a single financial transaction with its details."""
    def __init__(self, date, amount, category, description=''):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

class Category:
    """Represents a spending category with an associated budget and transactions."""
    def __init__(self, name, budget=0):
        self.name = name
        self.budget = budget
        self.transactions = []

    def add_transaction(self, transaction):
        """Adds a new transaction to this category."""
        self.transactions.append(transaction)
        print(f"Success: Added transaction of {transaction.amount} to '{self.name}'.")

    def total_spent(self):
        """Calculates the total amount spent in this category."""
        return sum(transaction.amount for transaction in self.transactions)

    def remaining_budget(self):
        """Calculates the remaining budget for this category."""
        return self.budget - self.total_spent()

    def transactions_in_period(self, start_date, end_date):
        """Returns a list of transactions within a specified date range."""
        return [t for t in self.transactions if start_date <= t.date <= end_date]

class BudgetTracker:
    """The main class for managing all categories and budget operations."""
    def __init__(self):
        self.categories = {}

    def add_category(self, name, budget=0):
        """Adds a new spending category to the tracker."""
        if name in self.categories:
            print(f"Error: Category '{name}' already exists.")
        else:
            self.categories[name] = Category(name, budget)
            print(f"Success: Added category '{name}' with a budget of ${budget:.2f}.")

    def add_transaction(self, category_name, amount, description=''):
        """Adds a new transaction to the specified category."""
        if category_name in self.categories:
            today = date.today()
            transaction = Transaction(today, amount, category_name, description)
            self.categories[category_name].add_transaction(transaction)
        else:
            print(f"Error: Category '{category_name}' not found.")

    def generate_report(self, category_name):
        """Prints a detailed spending report for a single category."""
        if category_name in self.categories:
            category = self.categories[category_name]
            print(f"\n--- Report for '{category.name}' ---")
            print(f"  Budget:          ${category.budget:.2f}")
            print(f"  Total Spent:     ${category.total_spent():.2f}")
            print(f"  Remaining:       ${category.remaining_budget():.2f}")
            print("\n  Transactions:")
            if category.transactions:
                for t in category.transactions:
                    print(f"    - {t.date}: ${t.amount:.2f} ({t.description})")
            else:
                print("    No transactions in this category.")
            print("-" * 25)
        else:
            print(f"Error: Category '{category_name}' not found.")

    def generate_period_report(self, category_name, period_type='weekly'):
        """Generates and plots a weekly or monthly spending report."""
        if category_name not in self.categories:
            print(f"Error: Category '{category_name}' not found.")
            return

        today = date.today()
        if period_type == 'weekly':
            start_date = today - timedelta(days=today.weekday())
            dates = [start_date + timedelta(days=i) for i in range(7)]
            labels = [d.strftime('%a, %b %d') for d in dates]
            title = f"Weekly Spending for '{category_name}'"
        else: # Monthly
            start_of_year = today.replace(day=1, month=1)
            months = [(start_of_year.replace(month=i)).strftime('%B') for i in range(1, today.month + 1)]
            labels = months
            title = f"Monthly Spending for '{category_name}' ({today.year})"

        spending_data = self._calculate_period_spending(category_name, period_type)
        self._plot_spending(labels, spending_data, title)

    def _calculate_period_spending(self, category_name, period_type):
        """Helper function to calculate spending data for plots."""
        today = date.today()
        category = self.categories[category_name]
        data = []
        if period_type == 'weekly':
            start_of_week = today - timedelta(days=today.weekday())
            for i in range(7):
                day = start_of_week + timedelta(days=i)
                day_total = sum(t.amount for t in category.transactions_in_period(day, day))
                data.append(day_total)
        else: # Monthly
            for month_num in range(1, today.month + 1):
                start_of_month = today.replace(day=1, month=month_num)
                end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                month_total = sum(t.amount for t in category.transactions_in_period(start_of_month, end_of_month))
                data.append(month_total)
        return data

    def _plot_spending(self, labels, data, title):
        """Helper function to create and display a bar chart."""
        plt.figure(figsize=(10, 6))
        plt.bar(labels, data, color='skyblue')
        plt.title(title, fontsize=16)
        plt.ylabel("Amount Spent ($)", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def save_data(self, filename):
        """Saves all budget data to a JSON file."""
        data = {
            name: {
                "budget": cat.budget,
                "transactions": [
                    {"date": t.date.isoformat(), "amount": t.amount, "description": t.description}
                    for t in cat.transactions
                ]
            } for name, cat in self.categories.items()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Success: Budget data saved to '{filename}'.")

    def load_data(self, filename):
        """Loads budget data from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.categories.clear()
                for name, cat_data in data.items():
                    category = Category(name, cat_data["budget"])
                    for t_data in cat_data["transactions"]:
                        transaction = Transaction(
                            date.fromisoformat(t_data["date"]),
                            t_data["amount"],
                            name,
                            t_data["description"]
                        )
                        category.transactions.append(transaction)
                    self.categories[name] = category
            print(f"Success: Budget data loaded from '{filename}'.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found. Starting with a fresh budget.")
        except json.JSONDecodeError:
            print(f"Error: Could not read '{filename}'. The file may be corrupted.")

def main():
    """Main function to run the budget tracker application loop."""
    tracker = BudgetTracker()
    while True:
        print("\n===== Personal Budget Tracker =====")
        print("1. Add Category")
        print("2. Add Transaction")
        print("3. Generate Category Report")
        print("4. Generate Weekly Spending Plot")
        print("5. Generate Monthly Spending Plot")
        print("6. Save Data to File")
        print("7. Load Data from File")
        print("8. Exit")
        choice = input("Choose an option: ")

        try:
            if choice == '1':
                name = input("Enter category name: ")
                budget = float(input("Enter budget amount: "))
                tracker.add_category(name, budget)
            elif choice == '2':
                name = input("Enter category name for transaction: ")
                amount = float(input("Enter transaction amount: "))
                desc = input("Enter description (optional): ")
                tracker.add_transaction(name, amount, desc)
            elif choice == '3':
                name = input("Enter category name for report: ")
                tracker.generate_report(name)
            elif choice == '4':
                name = input("Enter category name for weekly plot: ")
                tracker.generate_period_report(name, 'weekly')
            elif choice == '5':
                name = input("Enter category name for monthly plot: ")
                tracker.generate_period_report(name, 'monthly')
            elif choice == '6':
                filename = input("Enter filename to save (e.g., budget.json): ")
                tracker.save_data(filename)
            elif choice == '7':
                filename = input("Enter filename to load (e.g., budget.json): ")
                tracker.load_data(filename)
            elif choice == '8':
                print("Exiting Budget Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 8.")
        except ValueError:
            print("Invalid input. Please enter a valid number for amounts and budgets.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

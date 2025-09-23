import json
from datetime import date, timedelta
import matplotlib.pyplot as plt

class Transaction:
    def _init_(self, date, amount, category, description=''):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description  # Optional description of the transaction

class Category:
    def _init_(self, name, budget=0):
        self.name = name
        self.budget = budget  # Budget limit for this category
        self.transactions = []  # List of Transaction objects

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        print(f"Added transaction: {transaction.amount} for {self.name} on {transaction.date}.")

    def total_spent(self):
        return sum(transaction.amount for transaction in self.transactions)

    def remaining_budget(self):
        return self.budget - self.total_spent()

    def transactions_in_period(self, start_date, end_date):
        return [t for t in self.transactions if start_date <= t.date <= end_date]

class BudgetTracker:
    def _init_(self):
        self.categories = {}

    def add_category(self, name, budget=0):
        category = Category(name, budget)
        self.categories[name] = category
        print(f"Added category '{name}' with a budget of ${budget}.")

    def add_transaction(self, category_name, amount, description=''):
        if category_name in self.categories:
            today = date.today()
            transaction = Transaction(today, amount, category_name, description)
            self.categories[category_name].add_transaction(transaction)
        else:
            print("Category not found.")

    def generate_report(self, category_name):
        if category_name in self.categories:
            category = self.categories[category_name]
            print(f"\nReport for {category.name}:")
            print(f"Budget: ${category.budget}")
            print(f"Total Spent: ${category.total_spent()}")
            print(f"Remaining Budget: ${category.remaining_budget()}")
            print("\nTransactions:")
            for transaction in category.transactions:
                print(f" - {transaction.date}: ${transaction.amount} ({transaction.description})")
        else:
            print("Category not found.")

    def generate_weekly_report(self, category_name):
        if category_name in self.categories:
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            transactions = self.categories[category_name].transactions_in_period(start_of_week, end_of_week)
            total_spent = sum(t.amount for t in transactions)
            print(f"\nWeekly Report for {category_name} ({start_of_week} to {end_of_week}):")
            print(f"Total Spent: ${total_spent}")
            self.plot_weekly_comparison(category_name)
        else:
            print("Category not found.")

    def generate_monthly_report(self, category_name):
        if category_name in self.categories:
            today = date.today()
            start_of_month = today.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            transactions = self.categories[category_name].transactions_in_period(start_of_month, end_of_month)
            total_spent = sum(t.amount for t in transactions)
            print(f"\nMonthly Report for {category_name} ({start_of_month} to {end_of_month}):")
            print(f"Total Spent: ${total_spent}")
            self.plot_monthly_comparison(category_name)
        else:
            print("Category not found.")

    def plot_weekly_comparison(self, category_name):
        week_start = date.today() - timedelta(days=date.today().weekday())
        week_data = []
        for i in range(0, 7):
            date_to_check = week_start + timedelta(days=i)
            transactions = self.categories[category_name].transactions_in_period(date_to_check, date_to_check)
            week_data.append(sum(t.amount for t in transactions))

        plt.figure(figsize=(10, 5))
        plt.bar([str(week_start + timedelta(days=i)) for i in range(7)], week_data)
        plt.title(f"Weekly Spending Comparison for {category_name}")
        plt.xlabel("Date")
        plt.ylabel("Amount Spent ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_monthly_comparison(self, category_name):
        today = date.today()
        months = [today.replace(day=1, month=i) for i in range(1, today.month + 1)]
        monthly_data = []

        for month in months:
            next_month = (month + timedelta(days=32)).replace(day=1)
            transactions = self.categories[category_name].transactions_in_period(month, next_month - timedelta(days=1))
            monthly_data.append(sum(t.amount for t in transactions))

        plt.figure(figsize=(10, 5))
        plt.bar([m.strftime("%B") for m in months], monthly_data)
        plt.title(f"Monthly Spending Comparison for {category_name}")
        plt.xlabel("Month")
        plt.ylabel("Amount Spent ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def save_to_file(self, filename):
        data = {
            category_name: {
                "budget": category.budget,
                "transactions": [{"date": trans.date.isoformat(), "amount": trans.amount, "description": trans.description} for trans in category.transactions]
            } for category_name, category in self.categories.items()
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print("Budget data saved to file.")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for category_name, category_data in data.items():
                    category = Category(category_name, category_data["budget"])
                    category.transactions = [Transaction(date.fromisoformat(trans["date"]), trans["amount"], category_name, trans["description"]) for trans in category_data["transactions"]]
                    self.categories[category_name] = category
            print("Budget data loaded from file.")
        except FileNotFoundError:
            print("File not found.")


def main():
    budget_tracker = BudgetTracker()
    while True:
        print("\n1. Add Category\n2. Add Transaction\n3. Generate Report\n4. Generate Weekly Report\n5. Generate Monthly Report\n6. Save to File\n7. Load from File\n8. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter category name: ")
            budget = float(input("Enter budget: "))
            budget_tracker.add_category(name, budget)
        elif choice == '2':
            category_name = input("Enter category name: ")
            amount = float(input("Enter transaction amount: "))
            description = input("Enter description (optional): ")
            budget_tracker.add_transaction(category_name, amount, description)
        elif choice == '3':
            category_name = input("Enter category name: ")
            budget_tracker.generate_report(category_name)
        elif choice == '4':
            category_name = input("Enter category name: ")
            budget_tracker.generate_weekly_report(category_name)
        elif choice == '5':
            category_name = input("Enter category name: ")
            budget_tracker.generate_monthly_report(category_name)
        elif choice == '6':
            filename = input("Enter filename to save data: ")
            budget_tracker.save_to_file(filename)
        elif choice == '7':
            filename = input("Enter filename to load data: ")
            budget_tracker.load_from_file(filename)
        elif choice == '8':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "_main_":
    main()
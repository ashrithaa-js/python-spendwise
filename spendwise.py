import datetime
import matplotlib.pyplot as plt

class ExpenseManager:
    def __init__(self):
        self.expenses = []
        self.categories = set()
        self.currency_symbol = '₹'
        self.daily_limit = None
        self.monthly_limit = None
        self.yearly_limit = None
        self.serial_counter = 1
        self.filename = None

    def add_expense(self, category, amount, date=None, comment=None):
        if not date:
            date = datetime.date.today().strftime('%d-%m-%Y')

        serial_number = len(self.expenses) + 1

        self.expenses.append({"serial_number": serial_number, "date": date, "category": category, "amount": amount, "comment": comment})
        self.categories.add(category)

        if self.daily_limit is not None:
            today_expenses = sum(expense['amount'] for expense in self.expenses if expense['date'] == date)
            if today_expenses + amount > self.daily_limit:
                print("Warning: You have exceeded your daily spending limit!")

        if self.monthly_limit is not None:
            current_month = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%B')
            monthly_expense = sum(expense['amount'] for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').strftime('%B') == current_month)
            if monthly_expense > self.monthly_limit:
                print("Warning: You have exceeded your monthly spending limit!")

        if self.yearly_limit is not None:
            current_year = datetime.datetime.strptime(date, '%d-%m-%Y').year
            yearly_expense = sum(expense['amount'] for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == current_year)
            if yearly_expense > self.yearly_limit:
                print("Warning: You have exceeded your yearly spending limit!")

        self.save_expenses(self.filename)

    def delete_expense(self, serial_number):
        for idx, expense in enumerate(self.expenses):
            if expense['serial_number'] == serial_number:
                del self.expenses[idx]
                print("Expense deleted successfully.")
                for idx, expense in enumerate(self.expenses, start=1):
                    expense['serial_number'] = idx
                self.save_expenses(self.filename)
                return
        print("Expense not found.")

    def save_expenses(self, filename):
        with open(filename, 'w') as f:
            for expense in self.expenses:
                f.write(f"{expense['serial_number']}|{expense['date']}|{expense['category']}|{expense['amount']}|{expense.get('comment', '')}\n")

    def view_expenses(self, date=None):
        if not date:
            date = datetime.date.today().strftime('%d-%m-%Y')
        expenses_on_date = [expense for expense in self.expenses if expense['date'] == date]
        if expenses_on_date:
            print(f"Expenses on {date}:")
            for expense in expenses_on_date:
                print(f"Serial Number: {expense['serial_number']} | Category: {expense['category']} | Amount: {self.currency_symbol}{expense['amount']:.2f} | Comment: {expense.get('comment', '')}")
        else:
            print("No expenses recorded for this date.")

    def view_monthly_expenses(self, year=None,month=None):
        if not month:
            month = datetime.date.today().strftime('%B')
        if not year:
            year = datetime.date.today().year           
        expenses_on_month = [expense for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').strftime('%B') == month and datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year]
        if expenses_on_month:
            print(f"Expenses for {month}:")
            for expense in expenses_on_month:
                print(f"Serial Number: {expense['serial_number']} | Category: {expense['category']} | Amount: {self.currency_symbol}{expense['amount']:.2f} | Comment: {expense.get('comment', '')}")
        else:
            print("No expenses recorded for this month.")

    def view_yearly_expenses(self, year=None):
        if not year:
            year = datetime.date.today().year
        expenses_on_year = [expense for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year]
        if expenses_on_year:
            print(f"Expenses for {year}:")
            for expense in expenses_on_year:
                print(f"Serial Number: {expense['serial_number']} | Category: {expense['category']} | Amount: {self.currency_symbol}{expense['amount']:.2f} | Comment: {expense.get('comment', '')}")
        else:
            print("No expenses recorded for this year.")

    def total_expenses(self, date=None):
        if not date:
            date = datetime.date.today().strftime('%d-%m-%Y')
        total = sum(expense['amount'] for expense in self.expenses if expense['date'] == date)
        print(f"Total Expenses on {date}: {self.currency_symbol}{total:.2f}")

    def visualize_expenses_by_date(self, date=None):
        if not date:
            date = datetime.date.today().strftime('%d-%m-%Y')
        expenses_on_date = [expense for expense in self.expenses if expense['date'] == date]
        if expenses_on_date:
            category_expenses = {}
            for expense in expenses_on_date:
                category = expense['category']
                if category not in category_expenses:
                    category_expenses[category] = 0
                category_expenses[category] += expense['amount']

            labels = list(category_expenses.keys())
            values = list(category_expenses.values())

            plt.figure(figsize=(10, 6))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title(f"Expense Summary on {date}")
            plt.show()
        else:
            print("No expenses recorded for this date.")

    def visualize_expenses_by_month(self, year=None, month=None):
        if not month:
            month = datetime.date.today().strftime('%B')
        if not year:
            year = datetime.date.today().year
        expenses_on_month = [expense for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').strftime('%B') == month and datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year]
        if expenses_on_month:
            category_expenses = {}
            for expense in expenses_on_month:
                category = expense['category']
                if category not in category_expenses:
                    category_expenses[category] = 0
                category_expenses[category] += expense['amount']
    
            labels = list(category_expenses.keys())
            values = list(category_expenses.values())
    
            plt.figure(figsize=(10, 6))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title(f"Expense Summary for {month}")
            plt.show()
        else:
            print("No expenses recorded for this month.")

 
    def visualize_expenses_by_year(self, year=None):
        if not year:
            year = datetime.date.today().year
        expenses_on_year = [expense for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year]
        if expenses_on_year:
            category_expenses = {}
            for expense in expenses_on_year:
                category = expense['category']
                if category not in category_expenses:
                    category_expenses[category] = 0
                category_expenses[category] += expense['amount']

            labels = list(category_expenses.keys())
            values = list(category_expenses.values())

            plt.figure(figsize=(10, 6))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title(f"Expense Summary for {year}")
            plt.show()
        else:
            print("No expenses recorded for this year.")

    def visualize_monthexpenses_by_year(self, year=None):
        if not year:
            year = datetime.date.today().year
        expenses_on_year = [expense for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == int(year)]
        if expenses_on_year:
            month_expenses = {}
            for expense in expenses_on_year:
                month = datetime.datetime.strptime(expense['date'], '%d-%m-%Y').strftime('%B')
                if month not in month_expenses:
                    month_expenses[month] = 0
                month_expenses[month] += expense['amount']

            months = list(month_expenses.keys())
            expenses = list(month_expenses.values())

            plt.figure(figsize=(12, 6))
            plt.bar(months, expenses, color='skyblue')
            plt.xlabel('Month')
            plt.ylabel('Total Expenses')
            plt.title(f"Expense Summary for {year}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            print("No expenses recorded for this year.")

    def set_monthly_limit(self, limit):
        self.monthly_limit = limit

    def set_yearly_limit(self, limit):
        self.yearly_limit = limit

    def set_daily_limit(self, limit):
        self.daily_limit = limit

    def total_monthly_expense(self, year=None ,month=None):
        if not month:
            month = datetime.date.today().strftime('%B')
        if not year:
            year = datetime.date.today().year
        expenses_on_month = [expense['amount'] for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').strftime('%B') == month and datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year]
        total = sum(expenses_on_month)
        print(f"Total Expenses for {month}: {self.currency_symbol}{total:.2f}")
        if self.monthly_limit is not None:
            if total > self.monthly_limit:
                print("You have exceeded your monthly spending limit!")

    def total_yearly_expense(self, year=None):
        if not year:
            year = datetime.date.today().year
        expenses_on_year = [expense['amount'] for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year]
        total = sum(expenses_on_year)
        print(f"Total Expenses for {year}: {self.currency_symbol}{total:.2f}")
        if self.yearly_limit is not None:
            if total > self.yearly_limit:
                print("You have exceeded your yearly spending limit!")

    def edit_expense(self, serial_number, new_category=None, new_amount=None, new_date=None, new_comment=None):
        for expense in self.expenses:
            if expense['serial_number'] == serial_number:
                if new_category:
                    expense['category'] = new_category
                if new_amount is not None:
                    expense['amount'] = float(new_amount)
                if new_date:
                    expense['date'] = new_date
                if new_comment:
                    expense['comment'] = new_comment
                print("Expense edited successfully.")
                self.save_expenses(self.filename)
                return
        print("Expense not found.")

    def load_expenses(self, filename):
        self.expenses = []
        self.serial_counter = 1
        self.filename = filename
        with open(filename, 'r') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 5:
                    serial_number, date, category, amount, comment = fields
                    amount = float(amount)
                    self.expenses.append({"serial_number": int(serial_number), "date": date, "category": category, "amount": amount, "comment": comment})
                    self.serial_counter = max(self.serial_counter, int(serial_number) + 1)
                else:
                    print(f"Issue loading line: {line}")

    def view_daily_expense_by_category(self, date=""):
        if not date:
            date = datetime.date.today().strftime('%d-%m-%Y')
        filtered_expenses = [expense for expense in self.expenses if expense['date'] == date]
    
        if filtered_expenses:
            category_expenses = {}
            for expense in filtered_expenses:
                category = expense['category']
                if category not in category_expenses:
                    category_expenses[category] = []
                category_expenses[category].append(expense)
    
            print(f"Daily Expenses for {date}:")
            for category, expenses in category_expenses.items():
                print(f"\nCategory: {category}")
                for idx, exp in enumerate(expenses, start=1):
                    print(f"{idx}. Amount: {self.currency_symbol}{exp['amount']:.2f} | Comment: {exp.get('comment', '')}")
        else:
            print("No expenses recorded for this date.")


    def total_daily_expense_by_category(self, date=None):
        if not date:
            date = datetime.date.today().strftime('%d-%m-%Y')
        categories = set(expense['category'] for expense in self.expenses if expense['date'] == date)
        for category in categories:
            total_expense = sum(expense['amount'] for expense in self.expenses if expense['date'] == date and expense['category'] == category)
            print(f"Total expense in {category} on {date}: {self.currency_symbol}{total_expense:.2f}")

    
    def view_monthly_expense_by_category(self, year=None, month=None):
        if not year:
            year = datetime.date.today().year
        if not month:
            month = datetime.date.today().month
        filtered_expenses = [expense for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year and datetime.datetime.strptime(expense['date'], '%d-%m-%Y').month == month]
    
        if filtered_expenses:
            category_expenses = {}
            for expense in filtered_expenses:
                category = expense['category']
                if category not in category_expenses:
                    category_expenses[category] = []
                category_expenses[category].append(expense)
    
            print(f"Monthly Expenses for {datetime.date(year, month, 1).strftime('%B')} {year}:")
            for category, expenses in category_expenses.items():
                print(f"\nCategory: {category}")
                for idx, exp in enumerate(expenses, start=1):
                    print(f"{idx}. Date: {exp['date']} | Amount: {self.currency_symbol}{exp['amount']:.2f} | Comment: {exp.get('comment', '')}")
        else:
            print("No expenses recorded for this month.")
    
    def total_monthly_expense_by_category(self, year=None, month=None):
        if not year:
            year = datetime.date.today().year

        if not month:
            month = datetime.date.today().strftime('%B')

        categories = set(expense['category'] for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').strftime('%B') == month and datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == int(year))
        for category in categories:
            total_expense = sum(expense['amount'] for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').strftime('%B') == month and datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == int(year) and expense['category'] == category)
            print(f"Total expense in {category} for {month} {year}: {self.currency_symbol}{total_expense:.2f}")
    
    def view_yearly_expense_by_category(self, year=None):
        if not year:
            year = datetime.date.today().year
            # Filter expenses for the given year
            filtered_expenses = [expense for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year]

        if filtered_expenses:
            category_expenses = {}
            for expense in filtered_expenses:
                category = expense['category']
                if category not in category_expenses:
                    category_expenses[category] = []
                category_expenses[category].append(expense)

            print(f"Expenses for {year}:")
            for category, expenses in category_expenses.items():
                print(f"\nCategory: {category}")
                for idx, exp in enumerate(expenses, start=1):
                    print(f"{idx}. Date: {exp['date']} | Amount: {self.currency_symbol}{exp['amount']:.2f} | Comment: {exp.get('comment', '')}")
        else:
            print("No expenses recorded for this year.")

    
    def total_yearly_expense_by_category(self, year=None):
        if not year:
            year = datetime.date.today().year
        categories = set(expense['category'] for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year)
        for category in categories:
            total_expense = sum(expense['amount'] for expense in self.expenses if datetime.datetime.strptime(expense['date'], '%d-%m-%Y').year == year and expense['category'] == category)
            print(f"Total expense in {category} for {year}: {self.currency_symbol}{total_expense:.2f}")


def main():
    manager = ExpenseManager()
    manager.filename = "expense.txt"

    while True:
        print("\n1. Add Expense")
        print("2. Edit Expense")
        print("3. Delete Expense")
        print("4. Set Daily Limit")
        print("5. Set Monthly Limit")
        print("6. Set Yearly Limit")
        print("7. View Daily Expenses")
        print("8. View Monthly Expenses")
        print("9. View Yearly Expenses")
        print("10. Total Daily Expense")
        print("11. Total Monthly Expense")
        print("12. Total Yearly Expense")
        print("13. View Daily Expense by Category")
        print("14. View Monthly Expense by Category")
        print("15. View Yearly Expense by Category")
        print("16. Total Daily Expense by Category")
        print("17. Total Monthly Expense by Category")
        print("18. Total Yearly Expense by Category")
        print("19. Visualize Daily Expenses")
        print("20. Visualize Monthly Expenses")
        print("21. Visualize Monthly Expenses per Year")
        print("22. Visualize Yearly Expenses")
        print("23. Save Expenses")
        print("24. Load Expenses")
        print("25. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            date = input("Enter date (press Enter for today's date): ")
            comment = input("Enter comment (optional): ")
            manager.add_expense(category, amount, date, comment)

        elif choice == '2':
            serial_number = int(input("Enter serial number of the expense to edit: "))
            new_category = input("Enter new category (press Enter to keep unchanged): ")
            new_amount = input("Enter new amount (press Enter to keep unchanged): ")
            new_date = input("Enter new date (press Enter to keep unchanged): ")
            new_comment = input("Enter new comment (press Enter to keep unchanged): ")
            manager.edit_expense(serial_number, new_category, new_amount, new_date, new_comment)

        elif choice == '3':
            serial_number = int(input("Enter serial number of the expense to delete: "))
            manager.delete_expense(serial_number)

        elif choice == '4':
            limit = float(input("Enter daily limit: "))
            manager.set_daily_limit(limit)

        elif choice == '5':
            limit = float(input("Enter monthly limit: "))
            manager.set_monthly_limit(limit)

        elif choice == '6':
            limit = float(input("Enter yearly limit: "))
            manager.set_yearly_limit(limit)

        elif choice == '7':
            date = input("Enter date (press Enter for today's date): ")
            manager.view_expenses(date)

        elif choice == '8':
            month = input("Enter month (press Enter for current month): ")
            year = input("Enter year (press Enter for current year): ")
            manager.view_monthly_expenses(year,month)

        elif choice == '9':
            year = input("Enter year (press Enter for current year): ")
            manager.view_yearly_expenses(year)

        elif choice == '10':
            date = input("Enter date (press Enter for today's date): ")
            manager.total_expenses(date)

        elif choice == '11':
            month = input("Enter month (press Enter for current month): ")
            year = input("Enter year (press Enter for current year): ")
            manager.total_monthly_expense(year,month)

        elif choice == '12':
            year = input("Enter year (press Enter for current year): ")
            manager.total_yearly_expense(year)

        elif choice == '13':
            date = input("Enter date (press Enter for today's date): ")
            manager.view_daily_expense_by_category(date)

        elif choice == '14':
            month = input("Enter month (press Enter for current month): ")
            year = input("Enter year (press Enter for current year): ")            
            manager.view_monthly_expense_by_category(year, month)
        
        elif choice == '15':
            year = input("Enter year (press Enter for current year): ")
            manager.view_yearly_expense_by_category(year)

        elif choice == '16':
            date = input("Enter date (press Enter for today's date): ")
            manager.total_daily_expense_by_category(date)

        elif choice == '17':
            month = input("Enter month (press Enter for current month): ")
            year = input("Enter year (press Enter for current year): ")
            manager.total_monthly_expense_by_category(year,month)

        elif choice == '18':
            year = input("Enter year (press Enter for current year): ")
            manager.total_yearly_expense_by_category(year)

        elif choice == '19':
            date = input("Enter date (press Enter for today's date): ")
            manager.visualize_expenses_by_date(date)

        elif choice == '20':
            month = input("Enter month (press Enter for current month): ")
            year = input("Enter year (press Enter for current year): ")            
            manager.visualize_expenses_by_month(year,month)

        elif choice == '21':
            year = input("Enter year (press Enter for current year): ")
            manager.visualize_monthexpenses_by_year(year)

        elif choice == '22':
            year = input("Enter year (press Enter for current year): ")
            manager.visualize_expenses_by_year(year)

        elif choice == '23':
            filename = input("Enter filename to save expenses: ")
            manager.save_expenses(filename)

        elif choice == '24':
            filename = input("Enter filename to load expenses: ")
            manager.load_expenses(filename)

        elif choice == '25':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

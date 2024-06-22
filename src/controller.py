import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
from data import ExpenseModel
from datetime import datetime, date
import sqlite3

class ExpenseTrackerController:
    def __init__(self):
        self.model = ExpenseModel()

    def add_expense(self, amount, category, date, description):
        try:
            # Validate inputs
            if not (amount and category and date):
                raise ValueError("All fields except description are required.")

            amount = float(amount)  # Convert amount to float

            # Validate and convert date to string if necessary
            if isinstance(date, datetime) or isinstance(date, date):
                date = date.strftime("%Y-%m-%d")
            elif isinstance(date, str):
                datetime.strptime(date, '%Y-%m-%d')  # Validate date format
            else:
                raise ValueError("Date format is not valid.")

            self.model.add_expense(amount, category, date, description)
        except ValueError as ve:
            print(f"Error adding expense: {ve}")
        except Exception as e:
            print(f"Error adding expense: {e}")


    def get_expenses(self):
        try:
            return self.model.get_expenses()
        except Exception as e:
            print(f"Error getting expenses: {e}")
            return []

    def get_categories(self):
        try:
            return self.model.get_categories()
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    def add_category(self, category):
        try:
            self.model.add_category(category)
        except Exception as e:
            print(f"Error adding category: {e}")

    def remove_category(self, category):
        try:
            self.model.remove_category(category)
        except Exception as e:
            print(f"Error removing category: {e}")
            
    def load_expenses(self):
        try:
            return self.model.get_expenses()
        except Exception as e:
            print(f"Error loading expenses: {e}")
            return []

    def filter_expenses(self, category, start_date, end_date, min_amount, max_amount):
        try:
            expenses = self.model.get_expenses()

            # Filter by category
            if category and category != 'All':
                expenses = [expense for expense in expenses if expense[2] == category]

            # Filter by date range
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                expenses = [expense for expense in expenses if datetime.strptime(expense[3], '%Y-%m-%d') >= start_date]

            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                expenses = [expense for expense in expenses if datetime.strptime(expense[3], '%Y-%m-%d') <= end_date]

            # Filter by amount range
            if min_amount:
                expenses = [expense for expense in expenses if expense[1] >= float(min_amount)]

            if max_amount:
                expenses = [expense for expense in expenses if expense[1] <= float(max_amount)]

            return expenses
        except Exception as e:
            print(f"Error filtering expenses: {e}")
            return []

    def plot_expense_distribution(self):
        try:
            return self.model.plot_expense_distribution()
        except Exception as e:
            print(f"Error plotting expense distribution: {e}")

    def plot_monthly_expenses(self):
        try:
            return self.model.plot_monthly_expenses()
        except Exception as e:
            print(f"Error plotting monthly expenses: {e}")

    def export_to_csv(self, file_path):
        try:
            return self.model.export_to_csv(file_path)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

    def export_to_pdf(self, file_path):
        try:
            return self.model.export_to_pdf(file_path)
        except Exception as e:
            print(f"Error exporting to PDF: {e}")

    def export_to_sqlite(self, file_path):
        try:
            return self.model.export_to_sqlite(file_path)
        except Exception as e:
            print(f"Error exporting to SQLite: {e}")

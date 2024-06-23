import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
from data import ExpenseModel
from datetime import datetime, date
import sqlite3

class ExpenseTrackerController:
    def __init__(self):
        self.model = ExpenseModel()
        
    def validate_date(self, date_str):
        """
        Validate and normalize the date format to '%Y-%m-%d'.
        
        Args:
        - date_str (str): Date string in format '%Y-%m-%d'.
        
        Returns:
        - str: Validated date string in format '%Y-%m-%d'.
        
        Raises:
        - ValueError: If date format is not valid.
        """
        if not date_str:
            return datetime.today().date().strftime("%m/%d/%Y")  # Default to today's date if empty

        try:
            return datetime.strptime(date_str, '%m/%d/%Y').date().strftime("%m/%d/%Y")
        except ValueError:
            raise ValueError("Date format is not valid. It should be in YYYY/MM/DD format.")

    def add_expense(self, amount, category, date_str, description):
        """
        Add an expense to the model after validating inputs and date format.
        
        Args:
        - amount (str or float): Amount of the expense.
        - category (str): Category of the expense.
        - date_str (str): Date of the expense in format '%Y-%m-%d'.
        - description (str): Description of the expense.
        
        Raises:
        - ValueError: If any required field is missing or if amount is not numeric.
        - Exception: For any unexpected errors during the addition of expense.
        """
        try:
            # Validate inputs
            if not (amount and category and date_str):
                raise ValueError("All fields except description are required.")

            # Convert amount to float (if it's not already)
            amount = float(amount)

            # Validate and normalize date format
            date = self.validate_date(date_str)

            # Add expense to model
            self.model.add_expense(amount, category, date, description)

        except ValueError as ve:
            print(f"Error adding expense: {ve}")
            raise  # Re-raise the ValueError to propagate it to the caller (e.g., the GUI)

        except Exception as e:
            print(f"Error adding expense: {e}")
            raise Exception("Unexpected error occurred while adding expense.")


        
    def get_expenses(self):
        try:
            return self.model.get_expenses()
        except Exception as e:
            print(f"Error getting expenses: {e}")
            return []
        
    def get_expenses_charts(self):
        try:
            return self.model.get_expenses_charts()
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

import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from tkinter import filedialog

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'expenses.db')

class ExpenseModel:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DB_FILE)
            self.cursor = self.conn.cursor()
            self.create_tables_if_not_exist()
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")

    def create_tables_if_not_exist(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                    id INTEGER PRIMARY KEY,
                                    amount REAL,
                                    category TEXT,
                                    date TEXT,
                                    description TEXT)''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT UNIQUE)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def add_expense(self, amount, category, date, description):
        try:
            self.cursor.execute('INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)',
                                (amount, category, date, description))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")

    def get_expenses(self):
        try:
            self.cursor.execute('SELECT amount, category, date, description FROM expenses')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching expenses: {e}")
            return []
        
    def get_expenses_charts(self):
        try:
            self.cursor.execute('SELECT * FROM expenses')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching expenses: {e}")
            return []

    def add_category(self, category):
        try:
            self.cursor.execute('INSERT INTO categories (name) VALUES (?)', (category,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Category '{category}' already exists.")
        except sqlite3.Error as e:
            print(f"Error adding category: {e}")

    def remove_category(self, category):
        try:
            self.cursor.execute('DELETE FROM categories WHERE name=?', (category,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error removing category: {e}")

    def get_categories(self):
        try:
            self.cursor.execute('SELECT name FROM categories')
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error fetching categories: {e}")
            return []

    def export_to_csv(self, file_path):
        try:
            self.cursor.execute('SELECT * FROM expenses')
            rows = self.cursor.fetchall()

            df = pd.DataFrame(rows, columns=['id', 'amount', 'category', 'date', 'description'])
            df.to_csv(file_path, index=False)
            print(f"Data exported to {file_path} successfully.")
        except sqlite3.Error as e:
            print(f"Error exporting to CSV: {e}")

    def export_to_pdf(self, file_path):
        try:
            self.cursor.execute('SELECT * FROM expenses')
            rows = self.cursor.fetchall()

            df = pd.DataFrame(rows, columns=['id', 'amount', 'category', 'date', 'description'])

            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111)
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

            pdf = matplotlib.backends.backend_pdf.PdfPages(file_path)
            pdf.savefig(fig)
            pdf.close()
            print(f"Data exported to {file_path} successfully.")
        except sqlite3.Error as e:
            print(f"Error exporting to PDF: {e}")

    def export_to_sqlite(self, file_path):
        try:
            conn_export = sqlite3.connect(file_path)
            cursor_export = conn_export.cursor()
            
            self.cursor.execute('SELECT amount, category, date, description FROM expenses')
            rows = self.cursor.fetchall()

            cursor_export.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                    id INTEGER PRIMARY KEY,
                                    amount REAL,
                                    category TEXT,
                                    date TEXT,
                                    description TEXT)''')

            cursor_export.executemany('INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)', rows)
            conn_export.commit()
            conn_export.close()
            print(f"Data exported to {file_path} successfully.")
        except sqlite3.Error as e:
            print(f"Error exporting to SQLite: {e}")

    def close_connection(self):
        try:
            self.conn.close()
            print("Database connection closed.")
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")

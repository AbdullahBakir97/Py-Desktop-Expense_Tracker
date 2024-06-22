import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from tkinter import filedialog

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'expenses.db')

class ExpenseModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables_if_not_exist()

    def create_tables_if_not_exist(self):
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

    def add_expense(self, amount, category, date, description):
        self.cursor.execute('INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)',
                            (amount, category, date, description))
        self.conn.commit()

    def get_expenses(self):
        self.cursor.execute('SELECT * FROM expenses')
        return self.cursor.fetchall()

    def add_category(self, category):
        try:
            self.cursor.execute('INSERT INTO categories (name) VALUES (?)', (category,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Handle category already exists error
            pass

    def remove_category(self, category):
        self.cursor.execute('DELETE FROM categories WHERE name=?', (category,))
        self.conn.commit()

    def get_categories(self):
        self.cursor.execute('SELECT name FROM categories')
        return [row[0] for row in self.cursor.fetchall()]

    def export_to_csv(self, file_path):
        self.cursor.execute('SELECT * FROM expenses')
        rows = self.cursor.fetchall()

        df = pd.DataFrame(rows, columns=['id', 'amount', 'category', 'date', 'description'])
        df.to_csv(file_path, index=False)

    def export_to_pdf(self, file_path):
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

    def export_to_sqlite(self, file_path):
        conn_export = sqlite3.connect(file_path)
        cursor_export = conn_export.cursor()
        
        self.cursor.execute('SELECT * FROM expenses')
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

    def close_connection(self):
        self.conn.close()

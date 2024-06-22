# src/utils.py

import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import matplotlib.backends.backend_pdf

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'expenses.db')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create expenses table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        amount REAL,
                        category TEXT,
                        date TEXT,
                        description TEXT)''')
    
    # Create categories table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE)''')

    conn.commit()
    conn.close()

def add_expense_to_db(amount, category, date, description):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)',
                   (amount, category, date, description))
    conn.commit()
    conn.close()

def get_expenses_from_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()
    return rows

def export_to_csv(file_path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=['id', 'amount', 'category', 'date', 'description'])
    df.to_csv(file_path, index=False)

def export_to_pdf(file_path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=['id', 'amount', 'category', 'date', 'description'])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    pdf = matplotlib.backends.backend_pdf.PdfPages(file_path)
    pdf.savefig(fig)
    pdf.close()

def export_to_sqlite(file_path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('ATTACH DATABASE ? AS import_db', (file_path,))
    cursor.execute('INSERT INTO import_db.expenses SELECT * FROM expenses')
    conn.commit()
    conn.close()

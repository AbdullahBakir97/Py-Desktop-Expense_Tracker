import sqlite3
from tkinter import ttk, messagebox
from data import DB_FILE

class Preferences(ttk.Frame):
    def __init__(self, parent, controller, update_categories):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.update_categories = update_categories

        self.conn = None
        self.cursor = None
        self.connect_to_database()
        self.create_categories_table()
        self.load_categories_from_db()

        self.setup_ui()

    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect(DB_FILE)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_categories_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT UNIQUE)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating categories table: {e}")

    def load_categories_from_db(self):
        try:
            self.cursor.execute('SELECT name FROM categories')
            self.categories = [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error loading categories from database: {e}")

    def add_category(self, category):
        try:
            self.cursor.execute('INSERT INTO categories (name) VALUES (?)', (category,))
            self.conn.commit()
            self.load_categories_from_db()
            self.update_categories()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Category already exists!")
        except sqlite3.Error as e:
            print(f"Error adding category: {e}")
            messagebox.showerror("Error", f"Error adding category: {e}")

    def remove_category(self, category):
        try:
            self.cursor.execute('DELETE FROM categories WHERE name=?', (category,))
            self.conn.commit()
            self.load_categories_from_db()
            self.update_categories()
        except sqlite3.Error as e:
            print(f"Error removing category: {e}")
            messagebox.showerror("Error", f"Error removing category: {e}")

    def setup_ui(self):
        ttk.Label(self, text="Preferences Panel").pack(padx=10, pady=10)
        ttk.Button(self, text="Add Category", command=self.add_category_button_click).pack(padx=10, pady=10)

        ttk.Label(self, text="Categories:").pack(padx=10, pady=5)
        for category in self.categories:
            ttk.Label(self, text=category).pack(padx=10, pady=2)

    def add_category_button_click(self):
        category = "New Category"
        self.add_category(category)
        self.setup_ui()

    def close_connection(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from preferences import Preferences
from controller import ExpenseTrackerController
from datetime import datetime
from tkcalendar import Calendar, DateEntry
import pandas as pd
import matplotlib.pyplot as plt

class ExpenseTrackerView:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("Expense Tracker")
        self.controller = controller

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.setup_tabs()
        self.setup_export_buttons()
        self.setup_settings_tab()

        self.preferences = Preferences(self.root, self.controller, self.update_categories)
        self.load_categories()

    def setup_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.grid(row=0, column=0, sticky=(tk.W, tk.E))

        tab_names = ["Add Expense", "View Expenses", "Filter Expenses", "Reports"]
        tab_frames = [ttk.Frame(self.tabs) for _ in range(len(tab_names))]
        for frame, name in zip(tab_frames, tab_names):
            self.tabs.add(frame, text=name)

        self.setup_add_expense_form(tab_frames[0])
        self.setup_expense_table(tab_frames[1])
        self.setup_filter_form(tab_frames[2])
        self.setup_report_form(tab_frames[3])

    def setup_add_expense_form(self, frame):
        ttk.Label(frame, text="Amount:").grid(row=0, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(frame, width=25)
        self.amount_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Category:").grid(row=1, column=0, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.update_category_menu(frame)

        ttk.Label(frame, text="Date:").grid(row=2, column=0, sticky=tk.W)
        self.date_entry = DateEntry(frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.date_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        ttk.Label(frame, text="Description:").grid(row=3, column=0, sticky=tk.W)
        self.description_entry = ttk.Entry(frame, width=25)
        self.description_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        self.add_button = ttk.Button(frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=4, columnspan=2, pady=10)

    def setup_expense_table(self, frame):
        columns = ('Amount', 'Category', 'Date', 'Description')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=100)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E))
        frame.columnconfigure(0, weight=1)

        self.load_button = ttk.Button(frame, text="Load Expenses", command=self.load_expenses)
        self.load_button.grid(row=1, column=0, pady=10)

    def setup_filter_form(self, frame):
        ttk.Label(frame, text="Category:").grid(row=0, column=0, sticky=tk.W)
        self.filter_category_var = tk.StringVar(value="All")
        self.filter_category_menu = ttk.OptionMenu(frame, self.filter_category_var, "All", *self.controller.get_categories())
        self.filter_category_menu.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Date Range:").grid(row=0, column=2, sticky=tk.W)
        self.start_date_entry = ttk.Entry(frame, width=10)
        self.start_date_entry.grid(row=0, column=3, sticky=(tk.W, tk.E))
        self.end_date_entry = ttk.Entry(frame, width=10)
        self.end_date_entry.grid(row=0, column=4, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Amount Range:").grid(row=1, column=0, sticky=tk.W)
        self.min_amount_entry = ttk.Entry(frame, width=10)
        self.min_amount_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.max_amount_entry = ttk.Entry(frame, width=10)
        self.max_amount_entry.grid(row=1, column=2, sticky=(tk.W, tk.E))

        self.filter_button = ttk.Button(frame, text="Filter", command=self.filter_expenses)
        self.filter_button.grid(row=1, column=4, padx=10)

        # Treeview for displaying filtered expenses
        columns = ('Amount', 'Category', 'Date', 'Description')
        self.filtered_tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.filtered_tree.heading(col, text=col)
            self.filtered_tree.column(col, minwidth=0, width=100)

        self.filtered_tree.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E))

    def setup_report_form(self, frame):
        self.report_frame = ttk.Frame(frame, padding="10")
        self.report_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))

        self.pie_chart_button = ttk.Button(self.report_frame, text="Expense Distribution", command=self.plot_expense_distribution)
        self.pie_chart_button.grid(row=0, column=0, padx=10)

        self.bar_chart_button = ttk.Button(self.report_frame, text="Monthly Expenses", command=self.plot_monthly_expenses)
        self.bar_chart_button.grid(row=0, column=1, padx=10)

    def setup_settings_tab(self):
        settings_frame = ttk.Frame(self.tabs)
        self.tabs.add(settings_frame, text="Settings")

        ttk.Label(settings_frame, text="Add New Category:").grid(row=0, column=0, sticky=tk.W)
        self.new_category_entry = ttk.Entry(settings_frame, width=25)
        self.new_category_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.add_category_button = ttk.Button(settings_frame, text="Add", command=self.add_new_category)
        self.add_category_button.grid(row=0, column=2, padx=10)

        self.category_listbox = tk.Listbox(settings_frame, selectmode=tk.SINGLE)
        self.category_listbox.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.remove_category_button = ttk.Button(settings_frame, text="Remove", command=self.remove_category)
        self.remove_category_button.grid(row=1, column=2, padx=10)

    def update_category_menu(self, frame=None):
        if frame is None:
            frame = self.tabs.nametowidget(self.tabs.tabs()[0])
        
        categories = self.controller.get_categories()
        
        if hasattr(self, 'category_var'):
            self.category_var.set(categories[0] if categories else "")
            
            if hasattr(self, 'category_menu'):
                self.category_menu['menu'].delete(0, 'end')
                for category in categories:
                    self.category_menu['menu'].add_command(label=category, command=tk._setit(self.category_var, category))
            else:
                self.category_menu = ttk.OptionMenu(frame, self.category_var, categories[0] if categories else "", *categories)
                self.category_menu.grid(row=1, column=1, sticky=(tk.W, tk.E))


    def update_categories(self):
        self.update_category_menu(self.tabs.winfo_children()[0])  # Assuming first tab is Add Expense
        self.load_categories()  # Update categories in all other relevant places

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_var.set('')
        self.date_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def clear_filtered_tree(self):
        for item in self.filtered_tree.get_children():
            self.filtered_tree.delete(item)

    def setup_export_buttons(self):
        ttk.Label(self.root, text="Export Data:").grid(row=1, column=0, pady=10)
        self.export_csv_button = ttk.Button(self.root, text="Export to CSV", command=self.export_to_csv)
        self.export_csv_button.grid(row=1, column=0, padx=10, sticky=tk.W)

        self.export_pdf_button = ttk.Button(self.root, text="Export to PDF", command=self.export_to_pdf)
        self.export_pdf_button.grid(row=1, column=0, padx=10, sticky=tk.E)

        self.export_sqlite_button = ttk.Button(self.root, text="Export to SQLite", command=self.export_to_sqlite)
        self.export_sqlite_button.grid(row=1, column=0, padx=10)

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.controller.export_to_csv(file_path)
                messagebox.showinfo("Success", f"Data exported to {file_path} successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting to CSV: {e}")

    def export_to_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                self.controller.export_to_pdf(file_path)
                messagebox.showinfo("Success", f"Data exported to {file_path} successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting to PDF: {e}")

    def export_to_sqlite(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite files", "*.db")])
        if file_path:
            try:
                self.controller.export_to_sqlite(file_path)
                messagebox.showinfo("Success", f"Data exported to {file_path} successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting to SQLite: {e}")

    def add_new_category(self):
        category = self.new_category_entry.get().strip()
        if category:
            self.controller.add_category(category)
            self.preferences.add_category(category)  # Notify Preferences to add category
            self.update_categories()  # Update categories in both tabs

    def remove_category(self):
        category_index = self.category_listbox.curselection()
        if category_index:
            category = self.category_listbox.get(category_index[0])
            self.controller.remove_category(category)
            self.preferences.remove_category(category)  # Notify Preferences to remove category
            self.update_categories()  # Update categories in both tabs

    def load_categories(self):
        categories = self.controller.get_categories()
        self.category_listbox.delete(0, tk.END)
        for category in categories:
            self.category_listbox.insert(tk.END, category)

    def add_expense(self):
        amount = self.amount_entry.get().strip()
        category = self.category_var.get()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        description = self.description_entry.get().strip()

        try:
            # Validate inputs
            if not (amount and category and date):
                raise ValueError("All fields except description are required.")

            amount = float(amount)  # Convert amount to float

            # Add expense using controller
            self.controller.add_expense(amount, category, date, description)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_entries()
            self.load_expenses()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error adding expense: {e}")
                

    def load_expenses(self):
        self.clear_tree()
        expenses = self.controller.get_expenses()
        for expense in expenses:
            self.tree.insert("", tk.END, values=expense)

    def filter_expenses(self):
        category = self.filter_category_var.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        min_amount = self.min_amount_entry.get().strip()
        max_amount = self.max_amount_entry.get().strip()

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
            min_amount = float(min_amount) if min_amount else None
            max_amount = float(max_amount) if max_amount else None

            filtered_expenses = self.controller.filter_expenses(category, start_date, end_date, min_amount, max_amount)
            self.display_filtered_expenses(filtered_expenses)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def display_filtered_expenses(self, expenses):
        self.clear_filtered_tree()
        for expense in expenses:
            self.filtered_tree.insert("", tk.END, values=expense)

    def plot_expense_distribution(self):
        try:
            expenses = self.controller.load_expenses()
            df = pd.DataFrame(expenses, columns=['id', 'Amount', 'Category', 'Date', 'Description'])
            category_expenses = df.groupby('Category')['Amount'].sum()

            plt.figure(figsize=(8, 6))
            plt.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title('Expense Distribution by Category')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error plotting expense distribution: {e}")

    def plot_monthly_expenses(self):
        try:
            expenses = self.controller.load_expenses()
            df = pd.DataFrame(expenses, columns=['id', 'Amount', 'Category', 'Date', 'Description'])
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M')
            monthly_expenses = df.groupby('Month')['Amount'].sum()

            plt.figure(figsize=(10, 6))
            plt.bar(monthly_expenses.index.astype(str), monthly_expenses.values)
            plt.xlabel('Month')
            plt.ylabel('Total Expenses')
            plt.title('Monthly Expenses')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error plotting monthly expenses: {e}")

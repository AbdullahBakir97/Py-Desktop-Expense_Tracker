# src/main.py
import tkinter as tk
from tkinter import ttk
from gui import ExpenseTrackerView
from controller import ExpenseTrackerController

def main():
    root = tk.Tk()
    controller = ExpenseTrackerController()
    app = ExpenseTrackerView(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()
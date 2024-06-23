# Expense Tracker

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-yellow.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

## Overview

The **Expense Tracker** is a graphical application built with Python and Tkinter, designed to help users manage their expenses efficiently. It utilizes SQLite for data storage and offers an intuitive interface for adding, categorizing, and analyzing expenses. Whether for personal use or small business needs, this tool aims to simplify expense tracking and financial management.

## Features

- 📊 **Expense Management:**
  - Add, edit, and delete expenses with details such as amount, date, category, and notes.
  - Categorize expenses for better organization and analysis.

- 🗃️ **Data Storage:**
  - Uses SQLite database to store expense records securely locally.
  - Provides robust data management capabilities through SQL queries.

- 📅 **Date Filtering:**
  - Filter expenses by specific dates to view transactions within a specified timeframe.

- 📈 **Expense Analytics:**
  - Generate summaries and visual representations (charts/graphs) of expenses over time or by category.
  - Gain insights into spending patterns for informed financial decisions.

- 🎨 **Customizable Interface:**
  - User-friendly GUI built with Tkinter, offering a responsive and customizable experience.

## Future Development

🚀 **Under Development**

The Expense Tracker is continuously evolving with planned features to enhance functionality and user experience:

- **Expense Report Generation:** Export detailed expense reports in PDF or CSV formats.
- **Budget Planning:** Set budgets and receive alerts when nearing or exceeding limits.
- **Cloud Integration:** Synchronize data across devices and cloud storage for accessibility.
- **Data Insights:** Incorporate machine learning for predictive analytics and spending behavior analysis.
- **Multi-user Support:** Enable multiple user profiles with secure login and personalized settings.
- **Expense Reminders:** Schedule reminders for upcoming bills or recurring expenses.
- **Localization:** Support for multiple languages and currency formats for global usability.

Stay updated with our roadmap and contribute to shaping the future of Expense Tracker by opening issues or submitting pull requests. Your feedback and ideas are crucial for improving the tool!

## Getting Started

### Prerequisites

- 🐍 Python 3.x installed
- 🖼️ Tkinter library (usually included with Python installations)
- 🗄️ SQLite3

### Installation

1. **Clone the repository:**
   
```
   git clone https://github.com/yourusername/expense-tracker.git
   cd python-env-tool
```

2. **Install dependencies:**
   
```
   pip install -r requirements.txt
```

3. **Setup the SQLite database:**
   
```
   python setup_db.py
```

### Usage

1. **Run the application:**

```
    python gui.py
```



. **Explore functionalities:**

- 📅 **Filter by Date:** Use date selectors to view expenses within a specific period.
- 📊 **View Reports:** Analyze expenses with graphical representations.
- 📝 **Add/Edit Expenses:** Input new expenses or modify existing ones easily.

## Sequence Diagram

::: mermaid
sequenceDiagram
    participant User
    participant ExpenseTrackerView
    participant ExpenseTrackerController
    participant ExpenseModel
    participant Preferences

    User->>ExpenseTrackerView: Opens Expense Tracker
    activate ExpenseTrackerView

    ExpenseTrackerView->>ExpenseTrackerController: Request categories
    activate ExpenseTrackerController
    ExpenseTrackerController-->>ExpenseTrackerView: Categories
    deactivate ExpenseTrackerController

    User->>ExpenseTrackerView: Adds new expense
    ExpenseTrackerView->>ExpenseTrackerController: Validate and save expense details
    activate ExpenseTrackerController
    ExpenseTrackerController->>ExpenseModel: add_expense(amount, category, date, description)
    activate ExpenseModel
    ExpenseModel-->>ExpenseTrackerController: Expense saved confirmation
    deactivate ExpenseModel
    deactivate ExpenseTrackerController

    User->>ExpenseTrackerView: Filters expenses by category and date
    ExpenseTrackerView->>ExpenseTrackerController: Request filtered expenses
    activate ExpenseTrackerController
    ExpenseTrackerController->>ExpenseModel: get_expenses()
    activate ExpenseModel
    ExpenseModel-->>ExpenseTrackerController: Filtered expenses
    deactivate ExpenseModel
    deactivate ExpenseTrackerController

    User->>ExpenseTrackerView: Requests expense reports
    ExpenseTrackerView->>ExpenseTrackerController: Generate report
    activate ExpenseTrackerController
    ExpenseTrackerController->>ExpenseModel: get_expenses()
    activate ExpenseModel
    ExpenseModel-->>ExpenseTrackerController: Report data
    deactivate ExpenseModel
    deactivate ExpenseTrackerController

    User->>ExpenseTrackerView: Manages categories (add/remove)
    ExpenseTrackerView->>Preferences: Opens Preferences
    activate Preferences
    Preferences->>ExpenseModel: load_categories_from_db()
    activate ExpenseModel
    ExpenseModel-->>Preferences: Categories
    deactivate ExpenseModel

    Preferences->>ExpenseModel: add_category(category)
    activate ExpenseModel
    ExpenseModel-->>Preferences: Category added confirmation
    deactivate ExpenseModel

    Preferences->>ExpenseModel: remove_category(category)
    activate ExpenseModel
    ExpenseModel-->>Preferences: Category removed confirmation
    deactivate ExpenseModel

    Preferences-->>ExpenseTrackerView: Update categories UI
    deactivate Preferences

    User->>ExpenseTrackerView: Closes Expense Tracker
    ExpenseTrackerView->>ExpenseTrackerController: Close connection
    activate ExpenseTrackerController
    ExpenseTrackerController->>ExpenseModel: close_connection()
    activate ExpenseModel
    ExpenseModel-->>ExpenseTrackerController: Connection closed
    deactivate ExpenseModel
    deactivate ExpenseTrackerController

    ExpenseTrackerView-->>User: Expense Tracker closed
    deactivate ExpenseTrackerView
:::

## Entity-Relationship Diagram

::: mermaid
erDiagram
    EXPENSE {
        id INT PK
        amount FLOAT
        category VARCHAR
        date DATE
        description TEXT
    }
:::


## Visualizations

### Expense Distribution by Category

![Expense Distribution](data/Figure_1.png)

### Monthly Expenses

![Monthly Expenses](data/Figure_2.png)

## Full Expense Report

For a detailed expense report, view the [PDF report](data/pdf.pdf).


![Expense Tracker List](https://github.com/AbdullahBakir97/Py-Desktop-Expense_Tracker/assets/127149804/aa142657-cdbd-4060-8439-74a032fa2ad5)


## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests for any improvements or additional features you'd like to see in the Expense Tracker.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
import unittest
from datetime import datetime
from controller import ExpenseTrackerController

class TestExpenseTrackerController(unittest.TestCase):

    def setUp(self):
        # Initialize ExpenseTrackerController instance
        self.controller = ExpenseTrackerController()

    def test_add_expense_valid(self):
        # Test with valid inputs
        amount = 100.0
        category = "Food"
        date = '2024-06-21'
        description = "Dinner"

        try:
            self.controller.add_expense(amount, category, date, description)
        except Exception as e:
            self.fail(f"Unexpected exception occurred: {e}")

        # Optionally, you can add assertions here to verify the result if needed
        # For example:
        # expenses = self.controller.get_expenses()
        # self.assertEqual(len(expenses), 1, "Expense was not added correctly")

    def test_add_expense_missing_fields(self):
        # Test with missing required fields (amount, category, date)
        amount = 0.0
        category = ""
        date = ""
        description = "Test Expense"

        with self.assertRaises(ValueError):
            self.controller.add_expense(amount, category, date, description)

    def test_add_expense_invalid_date_format(self):
        # Test with invalid date format
        amount = 50.0
        category = "Transportation"
        date = "2023-06-35"  # Invalid date format
        description = "Commuting"

        with self.assertRaises(ValueError):
            self.controller.add_expense(amount, category, date, description)

    def test_add_expense_unexpected_error(self):
        # Test unexpected error handling
        amount = "invalid_amount"  # Invalid amount type
        category = "Miscellaneous"
        date = datetime.now().date()
        description = "Test"

        with self.assertRaises(Exception):
            self.controller.add_expense(amount, category, date, description)

if __name__ == '__main__':
    unittest.main()

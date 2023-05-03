from django.test import SimpleTestCase
from budget.forms import ExpenseForm


class TestForms(SimpleTestCase):

    # Test 25
    def test_expense_form_valid_data(self):
        """
        Test the form expense
        """
        form = ExpenseForm(
            data={
                'title': 'expense1',
                'amount': 1000,
                'category': 'development'
            })
        self.assertTrue(expr=form.is_valid(), msg=print("\033[0;32mTesting 25", sep=" "))

    # Test 26
    def test_expense_form_no_data_is_valid(self):
        """
        Test if the form is valid

        """
        form = ExpenseForm(data={})
        self.assertFalse(expr=form.is_valid(), msg=print("\033[0;32mTesting 26"))

    # Test 27
    def test_expense_form_no_data_errors_count(self):
        """
        Test the quantity of errors on the form
        """
        form = ExpenseForm(data={})
        self.assertEqual(first=len(form.errors), second=3, msg=print("\033[0;32mTesting 27", sep=" "))

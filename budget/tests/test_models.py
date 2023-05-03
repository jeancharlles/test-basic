from django.test import TestCase
from budget.models import Project, Category, Expense


class TestModels(TestCase):
    def setUp(self) -> None:
        self.project1 = Project.objects.create(
            name='Project 1',
            budget=10000
        )
        self.category1 = Category.objects.create(
            project=self.project1,
            name='development'
        )
        self.expense2 = Expense.objects.create(
            project=self.project1,
            title='expense2',
            amount=1000,
            category=self.category1
        )
        self.expense3 = Expense.objects.create(
            project=self.project1,
            title='expense3',
            amount=2000,
            category=self.category1
        )

    # Test 21
    def test_model_project_is_assigned_slug_on_creation(self):
        """
        Test the model during the creation and method save for slug
        """
        self.assertEqual(first=self.project1.slug, second='project-1', msg=print("\033[0;32mTesting 21"))

    # Test 22
    def test_model_budget_left(self):
        """
        Test the model for the method budget_left
        """
        self.assertEqual(first=self.project1.budget_left, second=7000, msg=print("\033[0;32mTesting 22"))

    # Test 23
    def test_model_total_transitions(self):
        """
        Test the model for the method total_transitions 
        """
        self.assertEqual(first=self.project1.total_transactions, second=2, msg=print("\033[0;32mTesting 23"))

    # Test 24
    def test_model_creation(self):
        """
        Test the model for the creation of one object
        """
        self.assertEqual(first=self.project1.name, second='Project 1')
        self.assertEqual(first=self.project1.budget, second=10000)
        self.assertEqual(first=self.category1.name, second='development', msg=print("\033[0;32mTesting 24"))

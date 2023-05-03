import json
import unittest
from django.test import TestCase, Client
from budget.views import project_list, project_detail, ProjectCreateView
from budget.models import Project, Category, Expense
from django.urls import reverse


class TestViews(TestCase):

    # First test without setUp
    # def test_project_list_GET(self):
    #     """
    #     Test the status code of view "list"
    #     """
    #     client = Client()
    #     response = client.get(path=reverse(viewname='list'))
    #     self.assertEqual(response.status_code, 200)

    # First test without setUp
    # def test_project_list_template(self):
    #     """
    #     Test the template used to the view "list"
    #     """
    #     client = Client()
    #     response = client.get(path=reverse(viewname='list'))
    #     self.assertTemplateUsed(response=response, template_name='budget/project-list.html')

    def setUp(self) -> None:
        self.client = Client()
        self.list_url = reverse(viewname='list')
        self.detail_url = reverse(viewname='detail', args=['project1'])

        self.project1 = Project.objects.create(
            name='project1',
            budget=1000
        )

        self.category1 = Category.objects.create(
            project=self.project1,
            name='development'
        )

    # Test 7
    def test_view_project_list_GET(self):
        """
        Test the status code of view project_list
        """
        response = self.client.get(path=self.list_url)
        self.assertEqual(first=response.status_code, second=200)

    # Test 8
    def test_view_project_list_template(self):
        """
        Test the template used for view project_list
        """
        response = self.client.get(path=self.list_url)
        self.assertTemplateUsed(response=response, template_name='budget/project-list.html')

    # Test 9
    def test_view_project_detail_GET_status_code_200(self):
        """
        Test the status code 200 of view project_detail
        """
        response = self.client.get(path=self.detail_url)
        self.assertEqual(first=response.status_code, second=200)

    # Test 10
    def test_view_project_detail_template(self):
        """
        Test the template used for the view project_detail
        """
        response = self.client.get(path=self.detail_url)
        self.assertTemplateUsed(response=response, template_name='budget/project-detail.html')

    # Test 11
    def test_view_project_detail_POST_adds_new_expense1_redirect_302(self):
        """
        Test the view project_detail and your redirect, inserting expense1 and redirect with status code 302
        """
        response = self.client.post(
            path=self.detail_url,
            data={
                'title': 'expense1',
                'amount': 1000,
                'category': 'development'
            })
        self.assertEqual(first=response.status_code, second=302)

    # Test 12
    def test_view_project_detail_POST_adds_new_expense2(self):
        """
        Test the view project_detail and your redirect, inserting expense2, and check the values
        """
        self.client.post(
            path=self.detail_url,
            data={
                'title': 'expense2',
                'amount': 100,
                'category': 'development'
            })
        self.assertEqual(first=self.project1.expenses.first().title, second='expense2')
        self.assertEqual(first=self.project1.expenses.first().amount, second=100)
        self.assertEqual(first=self.project1.expenses.first().category.name, second='development')

    # Test 13
    def test_view_project_detail_POST_no_data_status_code_302(self):
        """
        Test the redirect of view project_detail no data
        """
        response = self.client.post(path=self.detail_url)
        self.assertEqual(first=response.status_code, second=302)

    # Test 14
    def test_view_project_detail_POST_no_data_count(self):
        """
        Test the count of view project_detail no data
        """
        self.client.post(path=self.detail_url)  # Insert no data
        self.assertEqual(first=self.project1.expenses.count(), second=0)

    # Test 15 @unittest.skip(reason="In Progress")
    def test_view_project_detail_DELETE_status_code_204(self):
        """
        Test the status code of view project_detail using delete
        """
        Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=self.category1
        )
        response = self.client.delete(
            path=self.detail_url,
            data=json.dumps({
                'id': 1
            })
        )
        self.assertEqual(first=response.status_code, second=204)

    # Test 16
    def test_view_project_detail_DELETE_count(self):
        """
        Test the count of view project_detail using delete, using method "json.dumps"
        """
        Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=self.category1
        )

        self.client.delete(
            path=self.detail_url,
            data=json.dumps({  # method json.dumps
                'id': 1
            })
        )

        self.assertEqual(self.project1.expenses.count(), 0)

    # Test 17
    def test_view_project_detail_DELETE_no_id_status_code_404(self):
        """
        Test the view project_detail using method delete and no "json.dumps"
        """
        Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=self.category1
        )
        response = self.client.delete(path=self.detail_url)
        self.assertEqual(first=response.status_code, second=404)

    # Test 18
    def test_view_project_detail_DELETE_no_json_dumps_count(self):
        """
        Test the count of view project_detail using method delete no "json.dumps"
        """
        Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=self.category1
        )
        self.client.delete(path=self.detail_url)
        self.assertEqual(first=self.project1.expenses.count(), second=1)

    # Test 19
    def test_view_project_create_POST(self):
        """
        Test the view ProjectCreateView using data
        """
        url_create = reverse(viewname='add')

        self.client.post(
            path=url_create,
            data={
                'name': 'project2',
                'budget': 10000,
                'categoriesString': 'design,development'
            }
        )

        project2 = Project.objects.get(id=2)

        self.assertEqual(first=project2.name, second='project2')
        self.assertEqual(first=project2.budget, second=10000)

    # Test 20
    def test_view_project_create_post_content(self):
        """
        Test the view project_create using method post and verify content name of project and categories
        """
        url_create = reverse(viewname='add')
        self.client.post(
            path=url_create,
            data={
                'name': 'project2',
                'budget': 15000,
                'categoriesString': 'design,development'
            }
        )

        project2 = Project.objects.get(id=2)

        first_category = Category.objects.get(id=2)
        second_category = Category.objects.get(id=3)

        self.assertEqual(first=first_category.project.name, second=project2.name)
        self.assertEqual(first=second_category.project.name, second=project2.name)

        self.assertEqual(first=first_category.name, second='design')
        self.assertEqual(first=second_category.name, second='development', msg=print("\033[0;32mTesting 20"))

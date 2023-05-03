from django.test import TestCase, Client
from django.urls import reverse, resolve
from budget.views import project_list, ProjectCreateView, project_detail


class TestUrls(TestCase):
    # Test 1
    def test_get_url_root(self):
        """
        Test the url root
        """
        response = self.client.get('/')
        self.assertEquals(first=response.status_code, second=200)

    # Test 2
    def test_url_get_list_view(self):
        """
        Test the status code of url reverse of "list"
        """
        response = self.client.get(reverse(viewname='list'))
        self.assertEqual(first=response.status_code, second=200)

    # Test 3
    def test_url_get_list_view_resolved(self):
        """
        Test the url resolved of list with the view project_list
        """
        url_list = reverse(viewname='list')
        self.assertEqual(first=resolve(path=url_list).func, second=project_list)

    # Test 4
    def test_url_add_view(self):
        """
        Test the status code of url add
        """
        response = self.client.get(path='/add/')
        self.assertEqual(first=response.status_code, second=200)

    # Test 5 - Class Based View (CreateView)
    def test_url_add_create_view_resolved(self):
        """
        Test the url resolve add with the view ProjectCreateView
        """
        url_add = reverse(viewname='add')
        self.assertEqual(first=resolve(path=url_add).func.view_class, second=ProjectCreateView)

    # Test 6
    def test_url_detail_view_resolves(self):
        """
        Test the url detail with the view project_detail
        """
        url_detail = reverse(viewname='detail', args=['some-slug'])
        self.assertEqual(first=resolve(path=url_detail).func, second=project_detail)

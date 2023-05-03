import unittest
from selenium import webdriver
from budget.models import Project
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
from selenium.webdriver.common.by import By


class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        options.add_argument(argument='--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Firefox(
            options=options,
            executable_path="\\Users\Jean\WebDrivers\Firefox\geckodriver-v0.33.0-win64"
        )

    def tearDown(self) -> None:
        self.driver.quit()

    # Test 1
    def test_no_project_alert_is_displayed(self):
        self.driver.get(url=self.live_server_url)
        alert = self.driver.find_element(by=By.CLASS_NAME, value='noproject-wrapper')
        self.assertEqual(
            first=alert.find_element(by=By.TAG_NAME, value='h3').text,
            second="Sorry, you don't have any projects, yet."
        )
        time.sleep(5)

    # Test 2
    def test_no_project_alert_button_redirects_to_add_page(self):
        self.driver.get(url=self.live_server_url)
        add_url = self.live_server_url + reverse(viewname='add')
        self.driver.find_element(by=By.TAG_NAME, value='a').click()
        self.assertEqual(first=self.driver.current_url, second=add_url)

    # Test 3
    def test_get_url_general(self):
        self.driver.get('https://www.mozilla.com/')
        # self.driver.get(url="http:localhost:8000")
        time.sleep(5)

    # Test 4
    def test_user_sees_project_list(self):
        project1 = Project.objects.create(
            name='project1',
            budget=10000
        )
        self.driver.get(self.live_server_url)
        time.sleep(5)
        self.assertEqual(first=self.driver.find_element(by=By.TAG_NAME, value='h5').text, second=project1.name)
        self.assertEqual(first=self.driver.find_element(by=By.TAG_NAME, value='h5').text, second='project1')

    def test_user_is_redirected_to_project_detail(self):
        project1 = Project.objects.create(
            name='Project 1',
            budget=1000
        )
        self.driver.get(self.live_server_url)
        detail_url = self.live_server_url + reverse(viewname='detail', args=[project1.slug])
        self.driver.find_element(by=By.LINK_TEXT, value='VISIT').click()
        self.assertEqual(
            first=self.driver.current_url,
            second=detail_url
        )

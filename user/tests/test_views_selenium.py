""" Test with selenium"""
import time

from django.contrib.auth.models import User
from django.test import tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


@tag('selenium')
class MySeleniumTests(StaticLiveServerTestCase):
    """
    Class for test with Selenium
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.user = User.objects.create_user(username='TestUser', password="Testpassword!", is_active=True)

    def test_login(self):
        """
        test login views with selenium
        """
        print(User.objects.get(username='TestUser'))
        self.selenium.get("http://127.0.0.1:8000/accounts/login/")
        self.selenium.find_element_by_id('id_username').send_keys("TestUser")
        self.selenium.find_element_by_id('id_password').send_keys("Testpassword!")
        time.sleep(2)
        self.selenium.find_element_by_id('submit_login').click()

        index_url = "http://127.0.0.1:8000/"
        assert self.selenium.current_url == index_url

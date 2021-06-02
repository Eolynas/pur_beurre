""" Test with selenium"""
import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.webdriver.firefox.webdriver import WebDriver


@tag("selenium")
class MySeleniumTests(StaticLiveServerTestCase):
    """
    Class for test with Selenium
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.user = User.objects.create_user(
            username="TestUser", password="Testpassword!", is_active=True
        )

    def test_login(self):
        """
        test login views with selenium
        """
        print(User.objects.get(username="TestUser"))
        self.selenium.get(f"{self.live_server_url}/accounts/login/")
        self.selenium.find_element_by_id("id_username").send_keys("TestUser")
        self.selenium.find_element_by_id("id_password").send_keys("Testpassword!")
        time.sleep(2)
        self.selenium.find_element_by_id("submit_login").click()

        index_url = f"{self.live_server_url}/"
        assert self.selenium.current_url == index_url

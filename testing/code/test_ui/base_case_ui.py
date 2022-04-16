import os
from base_case import BaseCase
from selenium import webdriver
import pytest
import allure
from ui.pages.login_page import LoginPage
from selenium.webdriver.chrome.options import Options


class BaseCaseUI(BaseCase):

    @pytest.fixture(scope='function', autouse=True)
    def init_ui(self, init_system, driver, ui_report):
        self.driver = driver
        self.login_page = LoginPage(driver=driver)

    def get_driver(self):
        capabilities = dict()
        capabilities['browserName'] = 'chrome'
        capabilities['enableVNC'] = True
        capabilities['version'] = '96.0'
        browser = webdriver.Remote(command_executor='http://selenoid:4444/wd/hub',
                                   desired_capabilities=capabilities)
        browser.maximize_window()
        return browser

    @pytest.fixture(scope='function')
    def driver(self):
        url = f'http://myapp:4003'
        with allure.step('Init browser'):
            browser = self.get_driver()
            browser.get(url)

        yield browser

        browser.quit()

    @pytest.fixture(scope='function')
    def ui_report(self, driver, request, temp_dir):
        failed_tests_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_tests_count:
            self.make_a_shot('failure.png')
            browser_log = os.path.join(temp_dir, 'browser.log')
            with open(browser_log, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")

            with open(browser_log, 'r') as f:
                allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

    @pytest.fixture(scope='function')
    def registry_page(self):
        return self.login_page.go_to_registry_page()

    def make_a_shot(self, name=None):
        name = name + '.png'
        screenshot = os.path.join(self.test_dir, name)
        self.driver.get_screenshot_as_file(screenshot)
        allure.attach.file(screenshot, name=name, attachment_type=allure.attachment_type.PNG)


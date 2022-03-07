import logging
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager


# @pytest.fixture
# def base_page(driver):
#     return BasePage(driver=driver)
#
#
# @pytest.fixture
# def main_page(driver):
#     return MainPage(driver=driver)
#
#
# @pytest.fixture
# def search_page(driver):
#     return SearchPage(driver=driver)


def get_driver(selenoid_host):
    # browser_name = app-config.txt['browser']
    # selenoid = app-config.txt['selenoid']
    # vnc = app-config.txt['vnc']

    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": '/home/selenium/Downloads'})
    capabilities = dict()
    # capabilities['version'] += '_vnc'
    capabilities['enableVNC'] = True

    browser = webdriver.Remote(f'http://{selenoid_host}:4444/wd/hub', options=options,
                               desired_capabilities=capabilities)
    browser.maximize_window()
    return browser


@pytest.fixture(scope='function')
def driver():
    browsers = []

    def _driver(app_host, selenoid_host):
        url = f'http://{app_host}:8083'
        with allure.step('Init browser'):
            browser = get_driver(selenoid_host)
            browsers.append(browser)
            browser.get(url)
        return browser

    yield _driver
    for browser in browsers:
        browser.quit()


# @pytest.fixture(scope='function', params=['chrome', 'firefox'])
# def all_drivers(app-config.txt, request):
#     url = app-config.txt['url']
#     app-config.txt['browser'] = request.param
#
#     browser = get_driver(app-config.txt)
#     browser.get(url)
#     yield browser
#     browser.quit()
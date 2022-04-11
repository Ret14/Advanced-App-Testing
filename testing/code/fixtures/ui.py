import logging
import allure
import pytest
from selenium import webdriver


def get_driver():
    capabilities = dict()
    capabilities['browserName'] = 'chrome'
    capabilities['enableVNC'] = True

    browser = webdriver.Remote(f'http://selenoid:4444/wd/hub',
                               desired_capabilities=capabilities)
    browser.maximize_window()
    return browser


@pytest.fixture(scope='function')
def driver():
    browsers = []

    def _driver():
        url = f'http://myapp:4003'
        with allure.step('Init browser'):
            browser = get_driver()
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
import logging
import string
import random
import time
import allure
from selenium.webdriver import ActionChains
from ui.locators import locators
from utils.decorators import wait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):

    locators = locators.BaseLocators
    app_url = 'http://myapp:4003'

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('test')
        self.logger.info(f'Going to {self.__class__.__name__}')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Filling up {locator} field')
    def fill_up(self, locator, query):
        self.find(locator).click()
        self.find(locator).clear()
        self.find(locator).send_keys(query)
        self.logger.info(f'Filling up {locator} field')

    def search_by_text(self, query, expected=True):
        return self.is_on_page(self.format_locator(self.locators.TEXT_SEARCH, query)) and expected

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Clicking on {locator}')
    def click(self, locator, timeout=None):
        self.logger.info(f'Clicking on {locator}')
        for i in range(3):
            try:
                self.find(locator, timeout=timeout)
                elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                self.scroll_to(elem)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == 2:
                    raise

    def is_on_page(self, locator):
        return self.driver.find_elements(*locator)

    @staticmethod
    def format_locator(locator: tuple, value=None):
        return locator[0], locator[1].format(value)

    @allure.step('Waiting for possible redirects')
    def redirect_wait(self, timeout=2, interval=0.5):
        current_url = self.driver.current_url
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.driver.current_url != current_url:
                current_url = self.driver.current_url
                start_time = time.time()
            time.sleep(interval)
        return current_url

    @staticmethod
    def read_file(filename):
        file_lines = []
        with open(filename, 'r') as f:
            for line in f:
                file_lines.append(line.strip())

        return file_lines

    def random_ascii(self, min_len=None, max_len=None):
        if max_len is None:
            max_len = min_len

        letters_set = self.read_file('./utils/printable.txt')[0]

        return ''.join(random.choice(letters_set) for _ in range(random.randint(min_len, max_len)))

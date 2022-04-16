from ui.pages.base_page import BasePage
from ui.locators import locators
import allure


class RegistryPage(BasePage):

    locators = locators.RegistryPageLocators

    @allure.description("""Signing up and then signing in""")
    def register_and_login(self, username, password, email):
        self.fill_up(self.locators.USERNAME_INPUT, username)
        self.fill_up(self.locators.EMAIL_INPUT, email)
        self.fill_up(self.locators.PASS_INPUT, password)
        self.fill_up(self.locators.PASS_CONFIRM_INPUT, password)

        self.click(self.locators.CHECKBOX_INPUT)
        self.click(self.locators.SUBMIT_BTN)
        current_url = self.redirect_wait(1)

        return current_url

    @allure.description("""Checking if possible restriction messages pop up""")
    def catch_validation_error(self):
        valid_dict = {'username': True, 'password': True, 'email': True}
        if self.search_by_text('username'):
            valid_dict['username'] = False
        elif self.search_by_text('ssword'):
            valid_dict['password'] = False
        elif self.search_by_text('email'):
            valid_dict['email'] = False

        return valid_dict






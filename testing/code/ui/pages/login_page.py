from ui.pages.base_page import BasePage
from ui.locators import locators
import allure

from ui.pages.registry_page import RegistryPage


class LoginPage(BasePage):

    locators = locators.LoginPageLocators

    @allure.step('Authorizing in the app')
    def authorize(self, login, password):
        self.fill_up(self.locators.USERNAME_INPUT, login)
        self.fill_up(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.SUBMIT_BTN)
        current_url = self.redirect_wait(timeout=1)
        return current_url

    def go_to_registry_page(self):
        self.click(self.locators.REGISTRY_FIELD)
        return RegistryPage(driver=self.driver)

from ui.pages.base_page import BasePage
from ui.locators import locators
import allure


class MainPage(BasePage):

    locators = locators.MainPageLocators

    @allure.step("""Clicking logout button""")
    def logout(self):
        self.click(self.locators.LOGOUT_BTN)
        url_after_logout = self.redirect_wait(1)
        return url_after_logout

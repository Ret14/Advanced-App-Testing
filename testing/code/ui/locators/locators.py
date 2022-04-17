from selenium.webdriver.common.by import By


class BaseLocators:
    TEXT_SEARCH = (By.XPATH, '//*[contains(text(), "{}")]')


class RegistryPageLocators(BaseLocators):
    USERNAME_INPUT = (By.ID, 'username')
    EMAIL_INPUT = (By.ID, 'email')
    PASS_INPUT = (By.ID, 'password')
    PASS_CONFIRM_INPUT = (By.ID, 'confirm')
    CHECKBOX_INPUT = (By.ID, 'term')
    SUBMIT_BTN = (By.ID, 'submit')


class LoginPageLocators(BaseLocators):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    SUBMIT_BTN = (By.ID, 'submit')
    REGISTRY_FIELD = (By.XPATH, '//a')


class MainPageLocators(BaseLocators):
    LOGOUT_BTN = (By.ID, 'logout')

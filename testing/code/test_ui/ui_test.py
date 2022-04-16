from test_ui.base_case_ui import BaseCaseUI
import pytest
import allure


class TestUI(BaseCaseUI):

    @allure.description("""Signing in with correct credentials""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_ui_login_positive(self):
        url_after_login = self.login_page.authorize(*self.user_data[0:2])
        assert url_after_login.endswith('/welcome/') and self.check_user_active(self.user_data[0], 1)
        self.make_a_shot('login_positive')

    @allure.description("""Signing in with incorrect password""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_ui_login_negative_false_password(self):
        self.user_data[1] = self.random_ascii(1, 255)
        url_after_login = self.login_page.authorize(*self.user_data[0:2])
        assert not url_after_login.endswith('/welcome/')
        self.make_a_shot('login_negative_false_password')

    @allure.description("""Signing in with incorrect login""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_ui_login_negative_false_login(self):
        self.user_data[0] = self.random_ascii(6, 16)
        url_after_login = self.login_page.authorize(*self.user_data[0:2])
        assert not url_after_login.endswith('/welcome/')
        self.make_a_shot('login_negative_false_username')


class TestUIRegistryFieldValidation(BaseCaseUI):

    @pytest.mark.parametrize('username_length, expected',
                             [(5, False), (6, True), (16, True), (17, False)])
    @allure.description("""Trying to signin up with strict username length""")
    def test_ui_username_validation(self, username_length, expected, request):

        registry_page = request.getfixturevalue('registry_page')
        self.user_data[0] = self.random_ascii(username_length)
        url_after_registry = registry_page.register_and_login(*self.user_data)
        self.make_a_shot(f'register_with_username_{self.user_data[0]}')
        assert (url_after_registry.endswith('/welcome/') == expected) and \
               (registry_page.catch_validation_error()['username'] == expected)

    @pytest.mark.parametrize('email_length, expected', [(64, True), (65, False)])
    @allure.description("""Trying to signin up with strict email length""")
    def test_ui_username_validation(self, email_length, expected, request):

        registry_page = request.getfixturevalue('registry_page')
        self.user_data[2] = self.random_ascii(email_length)
        url_after_registry = registry_page.register_and_login(*self.user_data)
        self.make_a_shot(f'signing_up_and_email_length_is_{email_length}')
        assert (url_after_registry.endswith('/welcome/') == expected) and \
               (registry_page.catch_validation_error()['email'] == expected)

    @pytest.mark.parametrize('password_length, expected', [(255, True), (256, False)])
    @allure.description("""Trying to signin up with strict password length""")
    def test_ui_username_validation(self, password_length, expected, request):

        registry_page = request.getfixturevalue('registry_page')
        self.user_data[1] = self.random_ascii(password_length)
        url_after_registry = registry_page.register_and_login(*self.user_data)
        self.make_a_shot(f'signing_up_and_password_length_is_{password_length}')
        assert (url_after_registry.endswith('/welcome/') == expected) and \
               (registry_page.catch_validation_error()['password'] == expected)

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

    @allure.description("""Initiating logout""")
    def test_ui_logout(self, main_page):
        url_after_logout = main_page.logout()
        assert not url_after_logout.endswith('/welcome/') and self.check_user_active(self.user_data[0], 0)
        self.make_a_shot('after_logout')


class TestUIRegistryFieldValidation(BaseCaseUI):

    @pytest.mark.parametrize('field_type, field_length, expected',
                             [('username', 5, False), ('username', 6, True), ('username', 16, True),
                              ('username', 17, False), ('email', 64, True), ('email', 65, False),
                              ('password', 1, True), ('password', 255, True), ('password', 256, False)])
    @allure.description("""Testing {field_type} field validation on sign up page""")
    def test_ui_validation_all(self, field_type, field_length, expected, request):
        registry_page = request.getfixturevalue('registry_page')
        if field_type == 'username':
            self.user_data[0] = self.random_ascii(field_length)
        elif field_type == 'password':
            self.user_data[1] = self.random_ascii(field_length)
        else:
            self.user_data[2] = self.random_email_with_fixed_len(field_length)

        url_after_registry = registry_page.register_and_login(*self.user_data)
        assert (url_after_registry.endswith('/welcome/') == expected) and \
               (registry_page.catch_validation_error()[field_type] == expected) and \
               (self.check_user_access(self.user_data[0], 1) == expected)
        self.make_a_shot(f'signing_up;{field_type}_length_is_{field_length}')

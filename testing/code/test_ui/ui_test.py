from test_ui.base_case_ui import BaseCaseUI
import pytest
import allure


class TestUi(BaseCaseUI):

    @allure.description("""Signing in with correct credentials""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_login_positive(self):
        url_after_login = self.login_page.authorize(*self.user_data[0:2])
        assert url_after_login.endswith('/welcome/')
        self.make_a_shot('login_positive')

    @allure.description("""Signing in with incorrect password""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_login_negative_false_password(self):
        self.user_data[1] = self.random_ascii(1, 255)
        url_after_login = self.login_page.authorize(*self.user_data[0:2])
        assert not url_after_login.endswith('/welcome/')
        self.make_a_shot('login_negative_false_password')

    @allure.description("""Signing in with incorrect login""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_login_negative_false_login(self):
        self.user_data[0] = self.random_ascii(5, 16)
        url_after_login = self.login_page.authorize(*self.user_data[0:2])
        assert not url_after_login.endswith('/welcome/')
        self.make_a_shot('login_negative_false_username')

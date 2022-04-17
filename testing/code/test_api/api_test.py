import pytest
import allure
from test_api.base_case_api import BaseCaseApi


class TestApi(BaseCaseApi):

    # @allure.description("""Logging in with correct credentials via API""")
    # @pytest.mark.usefixtures('new_user_to_db', 'not_authorized')
    # def test_login_positive(self):
    #     response = self.api_client.post_login(*self.user_data[0:2])
    #     assert response.status_code == 200 and self.check_user_active(self.username, 1)
    #
    # @allure.description("""Logging in with incorrect username via API""")
    # @pytest.mark.usefixtures('new_user_to_db', 'not_authorized')
    # def test_login_negative_false_username(self):
    #     self.user_data[0] = self.random_ascii(6, 16)
    #     response = self.api_client.post_login(*self.user_data[0:2])
    #     assert response.status_code == 401 and self.check_user_active(self.username, 0)
    #
    # @allure.description("""Logging in with incorrect password via API""")
    # @pytest.mark.usefixtures('new_user_to_db', 'not_authorized')
    # def test_login_negative_false_password(self):
    #     self.user_data[1] = self.random_ascii(1, 255)
    #     response = self.api_client.post_login(*self.user_data[0:2])
    #     assert response.status_code == 401 and self.check_user_active(self.username, 0)

    @allure.description("""Adding new user via API""")
    def test_add_user(self, new_user):
        response = new_user
        assert response.status_code == 201, 'Status code must be 201'
        assert self.check_user_pass_email(*self.user_data)

    @allure.description("""Adding user with already existing username, password and email via API""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_add_existing_user(self):
        response = self.api_client.post_add_user(*self.user_data)
        assert response.status_code == 304

    @allure.description("""Deleting not-existing user via API""")
    def test_del_fake_user(self):
        response = self.api_client.get_delete_user(self.username)
        assert response.status_code == 404

    @allure.description("""Deleting an existing user via API""")
    @pytest.mark.xfail(strict=False)
    @pytest.mark.usefixtures('new_user_to_db')
    def test_del_user(self):
        response = self.api_client.get_delete_user(self.username)
        assert response.status_code == 204 and not self.check_user(self.username)

    @allure.description("""Getting application status via API""")
    def test_status(self):
        response = self.api_client.get_status()
        assert response.status_code == 200

    @allure.description("""Blocking user via API""")
    @pytest.mark.xfail(strict=False)
    @pytest.mark.usefixtures('new_user_to_db')
    def test_block_user(self):
        response = self.api_client.get_block_user(self.user_data[0])
        assert response.status_code == 200 and self.check_user_access(self.user_data[0], 0)

    @allure.description("""Unblocking user via API""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_unblock_user(self):
        self.api_client.get_block_user(self.user_data[0])
        response = self.api_client.get_unblock_user(self.user_data[0])
        assert response.status_code == 200 and self.check_user_access(self.user_data[0], 1)

    @allure.description("""Trying to add user with already existing email via API""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_negative_add_user_with_existing_email(self):
        self.user_data[0] = self.random_ascii(6, 16)
        response = self.api_client.post_add_user(*self.user_data)
        assert response.status_code == 304 and not self.check_user_pass_email(*self.user_data)

    @allure.description("""Trying to add user with already existing username via API""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_negative_add_user_with_existing_username(self):
        self.user_data[2] = self.fake.email()
        response = self.api_client.post_add_user(*self.user_data)
        assert response.status_code == 304 and not self.check_user_pass_email(*self.user_data)


class TestApiFieldValid(BaseCaseApi):

    @allure.description("""Positive testing of the email field validation in API""")
    @pytest.mark.parametrize('email', BaseCaseApi.read_file('./utils/emails_valid.txt'))
    def test_email_validation_positive(self, email):
        self.user_data[2] = email
        response = self.api_client.post_add_user(*self.user_data)
        assert self.check_user_pass_email(*self.user_data) and response.ok
        self.api_client.get_delete_user(self.user_data[0])

    @allure.description("""Negative testing of the email field validation in API""")
    @pytest.mark.parametrize('email', BaseCaseApi.read_file('./utils/emails_invalid.txt'))
    def test_email_validation_negative(self, email):
        self.user_data[2] = email
        response = self.api_client.post_add_user(*self.user_data)
        assert response.status_code != 500 and not self.check_user_pass_email(*self.user_data)

    @allure.description("""Testing of the username field validation in API""")
    @pytest.mark.parametrize('username_length, presence_in_db',
                             [(5, False), (6, True), (16, True), (17, False)])
    def test_username_validation(self, username_length, presence_in_db):
        self.user_data[0] = self.random_ascii(username_length)
        response = self.api_client.post_add_user(*self.user_data)
        assert response.status_code != 500 and \
               (self.check_user_pass_email(*self.user_data) == presence_in_db)

from test_cases.base_case import BaseCase
import pytest
import allure


class TestApi(BaseCase):

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
    @pytest.mark.usefixtures('new_user_to_db')
    def test_del_user(self):
        response = self.api_client.get_delete_user(self.username)
        assert response.status_code == 204 and not self.check_user(self.username)

    @allure.description("""Getting application status via API""")
    def test_status(self):
        response = self.api_client.get_status()
        assert response.status_code == 200

    @allure.description("""Blocking user via API""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_block_user(self):
        response = self.api_client.get_block_user(self.username)
        assert response.status_code == 200 and self.check_user_access(self.username, 0)

    @allure.description("""Unblocking user via API""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_unblock_user(self):
        self.api_client.get_block_user(self.username)
        response = self.api_client.get_unblock_user(self.username)
        assert response.status_code == 200 and self.check_user_access(self.username, 1)

    @allure.description("""Trying to add user with already existing email via API""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_negative_add_user_with_existing_email(self):
        new_username = self.random_ascii(5, 16)
        response = self.api_client.post_add_user(new_username, *self.user_data[1:3])
        assert response.status_code != 500 and not response.ok and \
               not self.check_user_pass_email(new_username, *self.user_data[1:3])

    @allure.description("""Trying to add user with already existing username via API""")
    @pytest.mark.usefixtures('new_user_to_db')
    def test_negative_add_user_with_existing_username(self):
        new_email = self.fake.email()
        response = self.api_client.post_add_user(*self.user_data[0:2], new_email)
        assert response.status_code != 500 and not response.ok and \
               not self.check_user_pass_email(*self.user_data[0:2], new_email)


class TestApiFieldValid(BaseCase):

    @allure.description("""Positive testing of the email field validation in API""")
    @pytest.mark.parametrize('email', BaseCase.read_file('emails_valid.txt'))
    def test_fields_validation_positive(self, email):
        response = self.api_client.post_add_user(*self.user_data[0:2], email)
        assert self.check_user_pass_email(*self.user_data[0:2], email) and response.ok
        self.api_client.get_delete_user(self.user_data[0])

    @allure.description("""Negative testing of the email field validation in API""")
    @pytest.mark.parametrize('email', BaseCase.read_file('emails_invalid.txt'))
    def test_fields_validation_negative(self, email):
        response = self.api_client.post_add_user(*self.user_data[0:2], email)
        assert response.status_code != 500 and not response.ok and \
               not self.check_user_pass_email(*self.user_data[0:2], email)

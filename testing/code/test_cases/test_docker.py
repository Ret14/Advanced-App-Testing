from test_cases.base_case import BaseCase
import pytest


class TestApi(BaseCase):

    def test_add_user(self, new_user):
        response = new_user
        assert response.status_code == 201, 'Must be 201'
        assert self.check_user_pass_email(*self.user_data)

    @pytest.mark.usefixtures('new_user')
    def test_add_existing_user(self):
        response = self.api_client.post_add_user(*self.user_data)
        assert response.status_code == 304

    def test_del_fake_user(self):
        response = self.api_client.get_delete_user(self.username)
        assert response.status_code == 404

    @pytest.mark.usefixtures('new_user')
    def test_del_user(self):
        response = self.api_client.get_delete_user(self.username)
        assert response.status_code == 204 and not self.check_user(self.username)

    def test_status(self):
        response = self.api_client.get_status()
        assert response.status_code == 200

    @pytest.mark.usefixtures('new_user')
    def test_block_user(self):
        response = self.api_client.get_block_user(self.username)
        assert response.status_code == 200 and self.check_user_access(self.username, 0)

    def test_unblock_user(self):
        self.test_block_user()
        response = self.api_client.get_unblock_user(self.username)
        assert response.status_code == 200 and self.check_user_access(self.username, 1)

    @pytest.mark.usefixtures('new_user')
    def test_add_user_with_existing_email(self):
        new_username = self.random_ascii(5, 16)
        self.user_data[0] = new_username
        response = self.api_client.post_add_user(*self.user_data)
        assert response.status_code != 500
        assert self.check_user_pass_email(*self.user_data), 'Not found in the users table'


class TestApiFieldValid(BaseCase):

    @pytest.mark.parametrize(
        'login,password,email',
        [
            (BaseCase.random_ascii(5, 16),
             BaseCase.random_ascii(1, 256),
             'valid_email') for _ in range(18)
        ]
    )
    def test_fields_validation_positive(self, login, password, email, request):
        email = request.getfixturevalue(email)
        response = self.api_client.post_add_user(login, password, email)
        assert self.check_user_pass_email(login, password, email)
        self.api_client.get_delete_user(login)

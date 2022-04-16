import os
import pytest
from base_case import BaseCase


class BaseCaseApi(BaseCase):

    @pytest.fixture(scope='function', autouse=True)
    def init_api(self, init_system, api_client):
        self.api_client = api_client

    @pytest.fixture(scope='function')
    def new_user(self, user_data):
        yield self.api_client.post_add_user(*user_data)
        self.api_client.get_delete_user(user_data[0])

    @pytest.fixture(scope='function')
    def not_authorized(self):
        self.api_client.get_logout()
        yield
        self.api_client.post_login(os.environ['USERNAME'], os.environ['PASSWORD'])

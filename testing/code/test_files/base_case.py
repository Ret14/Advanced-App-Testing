import random
import string
import time
import pytest
from API.api_client import ApiClient
from SQL.models.model import AppUsers
from SQL.mysql_orm.client import MysqlORMClient


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def start_system(self, user_data, credentials, logger):
        self.mysql_client = MysqlORMClient()
        self.mysql_client.connect()
        self.api_client = ApiClient(credentials)
        self.user_data = user_data
        self.username = user_data[0]
        yield
        self.mysql_client.connection.close()

    def check_user(self, username):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
                AppUsers.username == username).all()

    def check_user_access(self, username, access):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.access == access).all()

    @staticmethod
    def generate_string(length=6):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        random_string = random_string + str(int(time.time()) % 10000)
        return random_string

    def check_user_pass_email(self, username, password, email):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.password == password,
            AppUsers.email == email).all()

    @pytest.fixture(scope='function')
    def new_user(self, user_data):
        yield self.api_client.post_add_user(user_data)

        self.api_client.get_delete_user(user_data[0])

    @pytest.fixture(scope='function')
    def user_data(self):
        return self.generate_string(4), self.generate_string(4), self.generate_string(4)+'@aa.aa'

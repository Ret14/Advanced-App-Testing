import pytest
from SQL.models.model import AppUsers
from SQL.mysql_orm.client import MysqlORMClient
import string
import random
from faker import Faker


class BaseCase:
    fake = Faker()

    @pytest.fixture(scope='function', autouse=True)
    def start_system(self, user_data, logger, api_client):
        self.mysql_client = MysqlORMClient()
        self.mysql_client.connect()
        self.api_client = api_client
        #self.api_client = ApiClient(*credentials)
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
    def random_ascii(min_len, max_len):
        letters_set = string.printable
        for symbol in ('"', "'", '/', '\\'):
            letters_set = letters_set.replace(symbol, '')

        return ''.join(random.choice(letters_set) for _ in range(random.randint(min_len, max_len)))

    def check_user_pass_email(self, username, password, email):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.password == password,
            AppUsers.email == email).all()

    @pytest.fixture(scope='function')
    def new_user(self, user_data):
        yield self.api_client.post_add_user(*user_data)
        self.api_client.get_delete_user(user_data[0])

    @pytest.fixture(scope='function')
    def user_data(self):
        return self.random_ascii(5, 16), self.random_ascii(1, 255), self.fake.email()

    @staticmethod
    def read_file(filename):
        file_lines = []
        with open(filename, 'r') as f:
            for line in f:
                file_lines.append(line.strip())

        return file_lines

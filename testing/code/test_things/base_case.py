import random
import string
import time

import pytest
from code.API.api_client import ApiClient
from code.SQL.models.model import AppUsers
from code.SQL.mysql_orm.client import MysqlORMClient


class BaseCase:

    hostnames = None
    api_client = None

    @pytest.fixture(scope='function', autouse=True)
    def start_system(self, docker_compose, user_data, credentials, logger):
        self.mysql_client = MysqlORMClient(user='root', password='pass', db_name='TEST',
                                               host='0.0.0.0')
        self.mysql_client.connect(db_created=True)
        self.api_client = ApiClient(credentials[0], credentials[1])
        self.user_data = user_data
        yield
        self.mysql_client.connection.close()

    def check_user_in_db(self, username):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
                AppUsers.username == username).all()

    def check_user_access(self, username, access):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.access == access).all()

    def generate_string(self, length=6):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        random_string = random_string + str(int(time.time()) % 10000)
        return random_string

    def hard_check(self, username, password, email):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.password == password,
            AppUsers.email == email).all()

    @pytest.fixture(scope='function')
    def prepare_user(self, user_data):
        self.api_client.post_add_user(user_data['username'], user_data['password'],
                                      user_data['email'])
        yield
        self.api_client.get_delete_user(user_data['username'])

    @pytest.fixture(scope='function')
    def user_data(self):
        return {'username': self.generate_string(4), 'password': self.generate_string(4),
                'email': self.generate_string(4)+'@aa.aa'}






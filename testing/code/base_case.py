import random
import string
import pytest
from faker import Faker
from SQL.mysql_orm.client import MysqlORMClient
from SQL.models.model import AppUsers


class BaseCase:

    fake = Faker()

    @pytest.fixture(scope='function')
    def init_system(self, logger, temp_dir, user_data):
        self.mysql_client = MysqlORMClient()
        self.mysql_client.connect()
        self.test_dir = temp_dir
        self.user_data = user_data
        self.username = user_data[0]
        yield
        self.mysql_client.connection.close()

    def check_user(self, username):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
                AppUsers.username == username).all()

    def check_user_active(self, username, active):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.active == active).all()

    def check_user_access(self, username, access):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.access == access).all()

    def random_ascii(self, min_len=None, max_len=None):
        if max_len is None:
            max_len = min_len

        letters_set = self.read_file('./utils/printable.txt')[0]

        return ''.join(random.choice(letters_set) for _ in range(random.randint(min_len, max_len)))

    def check_user_pass_email(self, username, password, email):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.password == password,
            AppUsers.email == email).all()

    @pytest.fixture(scope='function')
    def new_user_to_db(self, user_data):
        self.mysql_client.session.commit()
        new_user = AppUsers(username=user_data[0],
                            password=user_data[1],
                            email=user_data[2],
                            access=1
                            )
        self.mysql_client.session.add(new_user)
        self.mysql_client.session.commit()
        yield
        self.mysql_client.session.query(AppUsers).filter(AppUsers.username == user_data[0],
                                                         AppUsers.password == user_data[1],
                                                         AppUsers.email == user_data[2]
                                                         ).delete()
        self.mysql_client.session.commit()

    @pytest.fixture(scope='function')
    def user_data(self):
        return [self.random_ascii(6, 16), self.random_ascii(1, 255), self.fake.email()]

    @staticmethod
    def read_file(filename):
        file_lines = []
        with open(filename, 'r') as f:
            for line in f:
                file_lines.append(line.strip())

        return file_lines

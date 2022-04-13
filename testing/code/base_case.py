import random
import string
import pytest
from faker import Faker
from SQL.mysql_orm.client import MysqlORMClient
from SQL.models.model import AppUsers


class BaseCase:

    fake = Faker()

    @pytest.fixture(scope='function')
    def init_system(self, user_data, logger, temp_dir, get_char_set):
        self.mysql_client = MysqlORMClient()
        self.mysql_client.connect()
        self.test_dir = temp_dir
        self.user_data = user_data
        self.username = user_data[0]
        self.letters_set = get_char_set
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

    def random_ascii(self, min_len, max_len):

        return ''.join(random.choice(self.letters_set) for _ in range(random.randint(min_len, max_len)))

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
        return [self.random_ascii(5, 16), self.random_ascii(1, 255), self.fake.email()]

    @staticmethod
    def read_file(filename):
        file_lines = []
        with open(filename, 'r') as f:
            for line in f:
                file_lines.append(line.strip())

        return file_lines

    @pytest.fixture(scope='session')
    def get_char_set(self):
        letters_set = string.printable
        for symbol in ('"', "'", '/', '\\'):
            letters_set = letters_set.replace(symbol, '')
        return letters_set

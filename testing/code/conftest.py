import logging
import os
import allure
import pytest
from API.api_client import ApiClient


@pytest.fixture(scope='function')
def logger(temp_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.INFO
    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)


def pytest_configure(config):
    base_dir = '/src/logs'
    config.base_temp_dir = base_dir


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        os.chmod("/tmp/allure", 0o777)


@pytest.fixture(scope='function')
def temp_dir(request):
    components = request.node.nodeid.split("::")
    # filename = components[0]
    # test_class = components[1] if len(components) == 3 else None
    test_func_with_params = components[-1]
    test_func = test_func_with_params.split('[')[0]
    test_params = test_func_with_params.split('[')[1][:-1].split('-')
    test_name = f"{test_func}['{test_params[0]}']"
    test_dir = os.path.join(request.config.base_temp_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


# @pytest.fixture(scope='session')
# def credentials(repo_root, file_name='credentials.txt'):
#     cred_path = os.path.join(repo_root, file_name)
#     with open(cred_path, 'r') as f:
#         user = f.readline().strip()
#         password = f.readline().strip()
#
#     return user, password


@pytest.fixture(scope='session')
def api_client():
    return ApiClient(os.environ['USERNAME'], os.environ['PASSWORD'])


@pytest.fixture(scope='session')
def valid_email():
    with open('emails_valid.txt', 'r') as f:
        yield f.readline().strip()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))

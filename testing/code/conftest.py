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
        for directory in ("/tmp/allure", "/src/logs", "/tmp/allure-report"):
            os.chmod(directory, 0o777)


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir,
                            request._pyfuncitem.node.originalname.replace('/', '_').replace(':', '_'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def api_client():
    return ApiClient(os.environ['USERNAME'], os.environ['PASSWORD'])


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))

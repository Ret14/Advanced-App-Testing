import logging
import requests

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 300


class ApiClient:

    def __init__(self, username, password):
        self.session = requests.Session()
        self.app_url = 'http://0.0.0.0:8083'
        self.post_login(username, password)

    def get_status(self):
        self.log_pre(url=f'{self.app_url}/status', summary='Getting app status')
        response = self.session.get(url=f'{self.app_url}/status')
        self.log_post(response)
        return response

    def post_add_user(self, username, password, email):
        data = {
            "username": username,
            "password": password,
            "email": email
        }
        self.log_pre(url=f'{self.app_url}/api/add_user', summary='Adding user')
        resp = self.session.post(url=f'{self.app_url}/api/add_user', json=data)
        self.log_post(resp)
        return resp

    def get_delete_user(self, username):
        self.log_pre(url=f'{self.app_url}/api/del_user/{username}', summary='Deleting user')
        resp = self.session.get(url=f'{self.app_url}/api/del_user/{username}')
        self.log_post(resp)
        return resp

    def get_block_user(self, username):
        self.log_pre(url=f'{self.app_url}/api/block_user/{username}', summary='Blocking user')
        resp = self.session.get(url=f'{self.app_url}/api/block_user/{username}')
        self.log_post(resp)
        return resp

    def get_unblock_user(self, username):
        self.log_pre(url=f'{self.app_url}/api/accept_user/{username}', summary='Unblocking user')
        resp = self.session.get(url=f'{self.app_url}/api/accept_user/{username}')
        self.log_post(resp)
        return resp

    def post_login(self, login, password):
        json = {
            'username': login,
            'password': password,
            'submit': 'Login'
        }
        self.log_pre(url=f'{self.app_url}/login', summary='Logging in')
        resp = self.session.post(url=f'{self.app_url}/login', json=json, allow_redirects=True)
        self.log_post(resp)
        return resp

    @staticmethod
    def log_pre(url, summary, expected_status=200):
        logger.info(f' * {summary} * Performing request:\n'
                    f'URL: {url}\n'
                    f'expected status: {expected_status}\n')

    @staticmethod
    def log_post(response):
        log_str = f'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n'
                            f'{response.text[:MAX_RESPONSE_LENGTH]}'
                            )
            elif logger.level == logging.DEBUG:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: {response.text}\n\n'
                            )
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n'
                        )

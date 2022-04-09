import logging
import requests

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 300


class ApiClient:

    def __init__(self, username, password):
        self.session = requests.Session()
        self.app_url = 'http://myapp:4003'
        self.post_login(username, password)

    def get_status(self):
        response = self.logged_request(method='GET', url=f'{self.app_url}/status',
                                       summary='Getting app status')
        return response

    def post_add_user(self, username, password, email):
        data = {
            "username": username,
            "password": password,
            "email": email
        }

        response = self.logged_request(method='POST', url=f'{self.app_url}/api/add_user',
                                       summary='Adding user', json=data)
        return response

    def get_delete_user(self, username):

        response = self.logged_request(method='GET', url=f'{self.app_url}/api/del_user/{username}',
                                       summary='Deleting user')
        return response

    def get_block_user(self, username):

        response = self.logged_request(method='GET', url=f'{self.app_url}/api/block_user/{username}',
                                       summary='Blocking user')
        return response

    def get_unblock_user(self, username):

        response = self.logged_request(method='GET', url=f'{self.app_url}/api/accept_user/{username}',
                                       summary='Unblocking user')
        return response

    def post_login(self, login, password):
        data = {
            'username': login,
            'password': password,
            'submit': 'Login'
        }

        response = self.logged_request(method='POST', url=f'{self.app_url}/login',
                                       summary='Logging in', json=data)
        return response

    @staticmethod
    def log_pre(method, url, summary, json=None):
        data = ''
        if not json is None:
            for elem in json:
                data += f'{elem}: {json[elem]}\n'

        logger.info(f'\n'
                    f'COMMENT: {summary}\n'
                    f'METHOD: {method}\n'
                    f'URL: {url}\n'
                    f'DATA: {data if data else "None"}\n'
                    )

    @staticmethod
    def log_post(response):
        # log_str = f'RESPONSE STATUS: {response.status_code}'
        #
        # if len(response.text) > MAX_RESPONSE_LENGTH:
        #     if logger.level == logging.INFO:
        #         logger.info(f'{log_str}\n'
        #                     f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
        #                     f'Use DEBUG logging.\n'
        #                     f'{response.text[:MAX_RESPONSE_LENGTH]}'
        #                     )
        #     elif logger.level == logging.DEBUG:
        #         logger.info(f'{log_str}\n'
        #                     f'RESPONSE CONTENT: {response.text if response.text else "None"}\n\n'
        #                     )
        # else:
        #     logger.info(f'{log_str}\n'
        #                 f'RESPONSE CONTENT: {response.text if response.text else "None"}\n'
        #                 )

        logger.info(f'\n'
                    f'RESPONSE STATUS: {response.status_code}\n'
                    f'RESPONSE CONTENT: {response.text if response.text else "None"}\n'
                    )

    def logged_request(self, summary, method, url, allow_redirects=True, json=None, data=None):
        self.log_pre(method, url, summary, json)
        response = self.session.request(method=method, url=url, allow_redirects=allow_redirects,
                                        json=json, data=data)
        self.log_post(response)
        return response

from code.test_things.base_case import BaseCase


class TestApi(BaseCase):
    def test_add_user(self):
        response = self.api_client.post_add_user(self.user_data['username'],
                                                 self.user_data['password'],
                                                 self.user_data['email']
                                                 )
        assert response.status_code == 201, 'Must be 201'
        assert self.hard_check(self.user_data['username'],
                                                 self.user_data['password'],
                                                 self.user_data['email'])

    def test_add_existing_user(self, prepare_user):
        response = self.api_client.post_add_user(self.user_data['username'],
                                                 self.user_data['password'],
                                                 self.user_data['email']
                                                 )
        assert response.status_code == 304

    def test_del_fake_user(self):
        response = self.api_client.get_delete_user(self.user_data['username'])
        assert response.status_code == 404

    def test_del_user(self, prepare_user):
        response = self.api_client.get_delete_user(self.user_data['username'])
        assert response.status_code == 204 and not self.check_user_in_db(self.user_data['username'])

    def test_status(self):
        resp = self.api_client.get_status()
        assert resp.status_code == 200

    def test_block_user(self, prepare_user):
        resp = self.api_client.get_block_user(self.user_data['username'])
        assert resp.status_code == 200 and self.check_user_access(self.user_data['username'], 0)

    def test_unblock_user(self, prepare_user):
        self.test_block_user(prepare_user)
        resp = self.api_client.get_unblock_user(self.user_data['username'])
        assert resp.status_code == 200 and self.check_user_access(self.user_data['username'], 1)

    def test_add_user_with_existing_email(self, prepare_user):
        new_username = self.user_data['username'][0:7]
        response = self.api_client.post_add_user(new_username,
                                                 self.user_data['password'],
                                                 self.user_data['email']
                                                 )
        assert response.status_code != 500
        assert self.hard_check(new_username, self.user_data['password'],
                               self.user_data['email']), 'Not found in the users table'

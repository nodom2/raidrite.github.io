from app.auth import Auth
from app import settings
import unittest


class TestAuth(unittest.TestCase):
    def setUp(self):
        auth_args = {'client_id': settings.TWITCH_CLIENT_ID, 'client_secret': settings.TWITCH_CLIENT_SECRET}
        self.test_auth = Auth(**auth_args)

    def test_auth_has_cid(self):
        self.assertEqual(self.test_auth.client_id, settings.TWITCH_CLIENT_ID)

    def test_auth_has_secr(self):
        self.assertEqual(self.test_auth.client_secret, settings.TWITCH_CLIENT_SECRET)

    def test_auth_has_auth_tok(self):
        self.assertTrue(hasattr(self.test_auth, 'auth_tok'))
        self.assertFalse(self.test_auth.auth_tok == "")
        self.assertTrue('access_token' in self.test_auth.auth_tok)
        self.assertTrue(len(self.test_auth.auth_tok['access_token']) > 0)
        self.assertFalse(self.test_auth.auth_tok['access_token'] == "")

    def test_auth_has_bear_tok(self):
        self.assertTrue(hasattr(self.test_auth, 'bear_tok'))
        self.assertFalse(self.test_auth.bear_tok == "")
        # Check Authorization field
        self.assertTrue('Authorization' in self.test_auth.bear_tok)
        self.assertTrue(len(self.test_auth.bear_tok['Authorization']) > 0)
        self.assertFalse(self.test_auth.bear_tok['Authorization'] == "")
        # Check Client_ID field
        self.assertTrue('Client_ID' in self.test_auth.bear_tok)
        self.assertTrue(len(self.test_auth.bear_tok['Client_ID']) > 0)
        self.assertFalse(self.test_auth.bear_tok['Client_ID'] == "")


if __name__ == '__main__':
    unittest.main()

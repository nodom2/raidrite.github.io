from auth import Auth
import config
import unittest


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.test_auth = Auth(config.client_id, config.client_secr)

    def test_auth_has_cid(self):
        self.assertEqual(self.test_auth.client_id, config.client_id)

    def test_auth_has_secr(self):
        self.assertEqual(self.test_auth.client_secret, config.client_secr)

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

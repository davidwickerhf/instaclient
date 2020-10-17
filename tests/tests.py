import unittest, time
from instaclient import InstaClient

class TestClient(unittest.TestCase):
    """Test InstaClient methods"""
    def __init__(self):
        super().__init__()
        self.client = None

    def test_init(self):
        """
        Test Class __init__()
        """
        username = input('Enter your instagram username: ')
        password = input('Enter your instagram password')
        self.client = InstaClient(username, password, 'chromedriver.exe')
        self.assertNotEqual(self.client, None, 'Should Be of Type Client. Client not created')

    def test_login(self):
        """
        Test Class login()
        """
        response = self.client.login()
        self.assertEqual(response, True, 'Should be True (connected)')

    def test_search_tag(self):
        """
        Test Class search_tag()
        """
        # Test existing tag
        tag = input('Enter an existing IG Tag')
        response = self.client.search_tag(tag) 
        self.assertEqual(response, True, 'Response is false, should be True. Search Existing Tag not Successful')
        # Test inexisting tag
        tag = input('Enter an inexisting IG Tag')
        response = self.client.search_tag(tag)
        self.assertEqual(response, True,  'Response is false, should be True. Search NonExisting Tag not Successful')

    def test_nav_user(self):
        """
        Test Class nav_user()
        """
        # Test Existing User
        user = input('Enter an existing IG username')
        response = self.client.nav_user(user)
        self.assertEqual(response, True, 'Response is false, should be True. Search Existing User failed.')
        # Test NonExisting User
        user = input('Enter an inexisting IG username')
        response = self.client.nav_user(user)
        self.assertEqual(response, True, 'Response is false, should be True. Search InExisting User failed.')

    def test_nav_user_dm(self):
        """
        Test Class nav_user_dm()
        """
        # Test existing user 
        # Test Existing User
        user = input('Enter an existing IG username')
        response = self.client.nav_user_dm(user)
        self.assertEqual(response, True, 'Response is false, should be True. Navifate to Existing User DMs failed.')

        # Test inexisting user
        user = input('Enter an inexisting IG username')
        response = self.client.nav_user_dm(user)
        self.assertEqual(response, True, 'Response is false, should be True. Navifate to InExisting User DMs failed.')

# TODO test_send_dm()
# TODO test_nav_user_followers()
# TODO test_get_followers()
# TODO test_follow_user()
# TODO test_unfollow_user()
# TODO test_get_user_images()



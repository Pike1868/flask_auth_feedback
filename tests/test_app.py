import unittest
from app import create_app
from app.models import db, User, Feedback


class UserTestCase(unittest.TestCase):
    """Tests for routes for Users."""

    def setUp(self):
        """Create test client, add sample data."""
        self.app = create_app('Testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.testuser = User.register(username="testuser",
                                      pwd="testuser",
                                      email="test@test.com",
                                      first_name="Test",
                                      last_name="User")

        db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
        db.drop_all()

    def test_user_registration(self):
        with self.client as c:
            response = c.post('/register',
                              data={'username': 'test2', 'password': 'password2',
                                    'email': 'test2@test.com', 'first_name': 'Test2', 'last_name': 'User2'},
                              follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            user = User.query.get("test2")
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'test2')

    def test_user_login(self):
        with self.client as c:
            response = c.post('/login',
                              data={'username': 'testuser',
                                    'password': 'testuser'},
                              follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            print(response.data)
            self.assertIn(b"Welcome Back, testuser!", response.data)

    def test_user_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'
            response = c.post('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Goodbye!", response.data)

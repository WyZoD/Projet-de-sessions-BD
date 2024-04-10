import os
import unittest
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Projet.database import get_db_connection
from server import app
from werkzeug.serving import make_server


class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.test_username = 'testuser12356'
        self.test_email = 'testuser@example12356.com'

    def test_hello_world(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):
        new_user_data = {
            'username': self.test_username,
            'password': 'testpassword',
            'email': self.test_email,
            'name': 'Test User',
            'address': '123 Test St'
        }
        # Send a POST request to the signup endpoint with the new user data
        response = self.client.post('/addSignup/', data=new_user_data, follow_redirects=False)

        self.assertTrue('/login/' in response.headers['Location'], "Redirection to login page expected after signup")

    # To kill the created user for the test
    def tearDown(self):
        print("Starting tearDown process...")
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # SQL to delete the test user
                    sql = "DELETE FROM Users WHERE username = %s"
                    cursor.execute(sql, (self.test_username,))
                    conn.commit()

        except Exception as e:
            print(f"Error in tearDown: {e}")
        else:
            print("tearDown completed successfully.")


class TestUserSignup(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.base_url = "/addSignup/"
        self.common_password = 'testpassword'
        self.common_name = 'Test User'
        self.common_address = '123 Test St'
        self.created_usernames = []

    def test_signup_with_duplicate_username(self):

        user1_data = {
            'username': 'uniqueuser',
            'password': self.common_password,
            'email': 'user1@example.com',
            'name': self.common_name,
            'address': self.common_address
        }

        # User 2 data, same username as user 1, different email
        user2_data = {
            'username': 'uniqueuser',  # Duplicate username
            'password': self.common_password,
            'email': 'user2@example.com',  # Different email
            'name': self.common_name,
            'address': self.common_address
        }
        self.created_usernames.append(user1_data['username'])

        response = self.app.post(self.base_url, data=user1_data)
        self.assertTrue('/login/' in response.headers['Location'], "User 1 should be successfully created.")
        response = self.app.post(self.base_url, data=user2_data)
        # Check not in login page /todo should check if the banner is there waiting for the merge/pr
        self.assertNotIn('/login/', response.headers.get('Location', ''),
                         "Duplicate username should not be allowed.")

        # Cleanup
        self.cleanup_users([user1_data['email'], user2_data['email']])

    def test_signup_with_duplicate_email(self):
        user1_data = {
            'username': 'user1unique',
            'password': self.common_password,
            'email': 'unique@example.com',
            'name': self.common_name,
            'address': self.common_address
        }

        # User 2 data, different username as user 1, same email
        user2_data = {
            'username': 'user2unique',  # Different username
            'password': self.common_password,
            'email': 'unique@example.com',  # Duplicate email
            'name': self.common_name,
            'address': self.common_address
        }
        self.created_usernames.append(user1_data['username'])

        response = self.app.post(self.base_url, data=user1_data)
        self.assertTrue('/login/' in response.headers['Location'], "User 1 should be successfully created.")
        response = self.app.post(self.base_url, data=user2_data)
        # Check not in login page /todo should check if the banner is there waiting for the merge/pr
        self.assertNotIn('/login/', response.headers.get('Location', ''),
                         "Duplicate email should not be allowed.")

        # Cleanup
        self.cleanup_users([user1_data['email'], user2_data['email']])
    def tearDown(self):
        self.cleanup_users(self.created_usernames)

    def cleanup_users(self, usernames):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                for username in usernames:
                    sql = "DELETE FROM Users WHERE username = %s"
                    cursor.execute(sql, (username,))
            conn.commit()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # unittest.main()

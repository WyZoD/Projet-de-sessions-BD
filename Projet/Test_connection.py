import os
import unittest
import time
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Projet.database import get_db_connection
from server import app
from Projet import server
from werkzeug.serving import make_server

class TestUserSignup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['FLASK_TESTING'] = '1'
        app.config['TESTING'] = True
        # Start Flask app in a separate thread
        cls.server = make_server('127.0.0.1', 5000, app)
        cls.server_thread = Thread(target=cls.server.serve_forever)
        cls.server_thread.start()

    def setUp(self):
        chrome_options = Options()

        self.client = app.test_client()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.base_url = "http://127.0.0.1:5000"

    def test_signup_process(self):
        self.driver.get(f"{self.base_url}/signup")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(
            "testuser123")
        self.driver.find_element(By.NAME, "name").send_keys("Test User")
        self.driver.find_element(By.NAME, "email").send_keys("testuser123@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("testpassword")
        self.driver.find_element(By.NAME, "address").send_keys("123 Test St")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login"))
        self.assertTrue(self.driver.current_url.endswith("/login/"),
                        "User should be redirected to login page after signup.")

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask server
        cls.server.shutdown()
        cls.server_thread.join()
        os.environ.pop('FLASK_TESTING', None)  # Clean up environment variable

    def tearDown(self):
        self.driver.quit()
        # Cleanup the database
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM Users WHERE username = %s"
                cursor.execute(sql, ("testuser123",))
                conn.commit()


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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # unittest.main()

import unittest
from Projet.database import get_db_connection
from server import app

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


    # To kill the create user for the test
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
    unittest.main()

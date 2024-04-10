import time
import unittest
import os
import unittest
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from Projet.database import get_db_connection
from server import app
from werkzeug.serving import make_server

class TestUserSignup(unittest.TestCase):
    ## Start the server
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

    # test Zone

    def test_add_to_cart_without_login(self):
        # Navigate directly to the product listing page
        self.driver.get(f"{self.base_url}")

        # Wait for the product listings to be visible and click the first product link
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".products .product a"))
        ).click()

        # Try to add the product to the cart
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "form[action*='/add-to-cart/'] button[type='submit']"))
        ).click()

        # Check if the current URL is the login page
        current_url = self.driver.current_url
        self.assertIn("/login/", current_url, "Not redirected to login page after attempting to add to cart without logging in.")

    def test_entire_process(self):

        # Signup
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

        # Login
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(
            "testuser123@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("testpassword")
        self.driver.find_element(By.CSS_SELECTOR, "form[action='/login'] button[type='submit']").click()

        # Ensure we're on the correct page that lists products. Adjust this URL as needed.
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".products .product a"))
        )
        # Find the 1st product and click
        first_product_link = self.driver.find_element(By.CSS_SELECTOR, ".products .product:first-of-type a")
        first_product_link.click()

        # Wait for the page to load by checking the url + time
        WebDriverWait(self.driver, 10).until(EC.url_contains("/product/"))
        current_url = self.driver.current_url

        # Assert that the URL contains the word "product"
        self.assertIn("product", current_url, "URL does not contain 'product'.")

        # Check if in the product page
        self.assertTrue("/product/" in current_url and current_url.split("/product/")[1].startswith("1"),
                        "URL does not match expected '/product/1/' pattern.")

        # Select the rating. Here, we're choosing 5.
        rating_select = Select(self.driver.find_element(By.ID, "note"))
        rating_select.select_by_value('5')

        # Fake comment
        self.driver.find_element(By.ID, "commentaire").send_keys("This is a test review. Amazing product!")
        self.driver.find_element(By.CSS_SELECTOR, "form[action='/add-review/1/'] button[type='submit']").click()

        # Verify the review appears on the page
        review_text = self.driver.find_element(By.XPATH,
                                               "//div[contains(@class, 'review')]//p[contains(text(), 'This is a test review. Amazing product!')]").text
        self.assertIn("This is a test review. Amazing product!", review_text, "Review did not appear as expected.")

        # Click "Add to Cart"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form[action*='/add-to-cart/'] button[type='submit']"))
        ).click()

        # Navigate to the Cart page
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/cart/']"))
        ).click()

        # Ensure the Cart page is loaded
        WebDriverWait(self.driver, 10).until(EC.url_contains("/cart"))

        # Check that the cart is not empty by confirming the presence of cart-item class
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-item"))
        )
        cart_items = self.driver.find_elements(By.CSS_SELECTOR, ".cart-item")
        self.assertGreater(len(cart_items), 0, "Cart is unexpectedly empty.")

        # Place the order
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form[action*='/place-order'] button[type='submit']"))
        ).click()

        # Wait for the flash message to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Your order has been placed.')]"))
        )

        # Verify the flash message
        flash_message = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Your order has been placed.')]").text
        self.assertIn("Your order has been placed.", flash_message,
                      "Order confirmation message did not appear as expected.")

    # SHUTDOWN THE SERVER
    @classmethod
    def tearDownClass(cls):
        # Stop the Flask server
        cls.server.shutdown()
        cls.server_thread.join()
        os.environ.pop('FLASK_TESTING', None)  # Clean up environment variable

    def tearDown(self):
        # Connect to the database
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                
                # Delete any OrderItems for the test user by joining on Commands (Orders) table
                delete_order_items_sql = """
                DELETE OrderItems
                FROM OrderItems
                JOIN Commands ON OrderItems.OrderID = Commands.OrderID
                WHERE Commands.Username = %s
                """
                cursor.execute(delete_order_items_sql, ("testuser123",))

                # Delete any Commands for the test user
                delete_commands_sql = "DELETE FROM Commands WHERE Username = %s"
                cursor.execute(delete_commands_sql, ("testuser123",))

                # Delete any CartItems for the test user
                delete_cart_items_sql = "DELETE FROM CartItems WHERE Username = %s"
                cursor.execute(delete_cart_items_sql, ("testuser123",))

                # Delete any ProductReviews for the test user
                delete_reviews_sql = "DELETE FROM ProductReviews WHERE Username = %s"
                cursor.execute(delete_reviews_sql, ("testuser123",))

                # Delete the test user
                delete_user_sql = "DELETE FROM Users WHERE Username = %s"
                cursor.execute(delete_user_sql, ("testuser123",))

            # Commit the transactions to finalize the cleanup
            conn.commit()

        super().tearDown()


if __name__ == '__main__':
    unittest.main()

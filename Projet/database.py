import pymysql
from flask import logging
from flask.cli import load_dotenv
import os
import pymysql.cursors

from werkzeug.security import generate_password_hash

# Load environment variables
load_dotenv()


# Establish database connection
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get("host"),
        port=int(os.environ.get("port")),
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        db=os.environ.get("database"),
        autocommit=True
    )


# Add new user to the database
def add_user(username, password, email, name, address):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("Insert into users (username, password, email, name, address, InscriptionDate) "
                               "values (%s, %s, %s, %s, %s, NOW())",
                               (username, password, email, name, address,))
                connection.commit()
                return True
            except Exception as e:
                print(e)
                connection.rollback()
                return False


# Retrieve user details by email
def get_user_by_email(email):
    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                return cursor.fetchone()
    except Exception as e:
        print(e)
        return None


# Get all products from the database
def get_all_products():
    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Products")
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return []


# Get a single product by ID
def get_product_by_id(product_id, conn=None):
    own_connection = False

    if conn is None:
        conn = get_db_connection()
        own_connection = True

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM Products WHERE ProductID = %s", (product_id,))
            product = cursor.fetchone()

        if own_connection:
            conn.close()

        return product
    except Exception as e:
        print(f"An error occurred while fetching product by ID: {e}")
        if own_connection and conn:
            conn.close()
        return None


# Get reviews by product ID
def get_reviews_by_product_id(product_id):
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT r.*, u.Name AS UserName 
            FROM ProductReviews r 
            JOIN Users u ON r.Username = u.Username 
            WHERE ProductID = %s
            ORDER BY Date DESC""", (product_id,))
        reviews = cursor.fetchall()
    return reviews


# Add a review to a product
def add_product_review(product_id, username, note, commentaire):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO ProductReviews (ProductID, Username, Note, Commentaire, Date)
            VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(sql, (product_id, username, note, commentaire))
        conn.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()


# add an item to the cart
def add_item_to_cart(username, product_id, quantity):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO CartItems (Username, ProductID, Quantity) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE Quantity = Quantity + %s""",
                           (username, product_id, quantity, quantity))
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False


# get the items in the cart
def get_cart_items(username):
    items = []
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT p.ProductID, p.Name, p.Price, c.Quantity
                FROM CartItems c
                JOIN Products p ON c.ProductID = p.ProductID
                WHERE c.Username = %s""",
                           (username,))
            items = cursor.fetchall()
    except Exception as e:
        print(e)
    return items


# update the quantity of an item in the cart
def update_cart_item_quantity(username, product_id, new_quantity):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE CartItems 
            SET Quantity = %s 
            WHERE Username = %s AND ProductID = %s
            """
            cursor.execute(sql, (new_quantity, username, product_id))
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# remove an item from the cart
def remove_item_from_cart(username, product_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM CartItems WHERE Username = %s AND ProductID = %s"
            cursor.execute(sql, (username, product_id))
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# create an order
def create_order(username, delivery_address, total, conn=None):
    own_connection = False
    if conn is None:
        conn = get_db_connection()
        own_connection = True
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Commands (Username, DeliveryAddress, Total, DateCommand, Status) 
            VALUES (%s, %s, %s, NOW(), 'Pending')
            """
            cursor.execute(sql, (username, delivery_address, total))
            order_id = conn.insert_id()
        if own_connection:
            conn.commit()
        return order_id
    except Exception as e:
        if own_connection:
            conn.rollback()
        raise e
    finally:
        if own_connection:
            conn.close()


# add an item to an order
def add_order_item(order_id, product_id, quantity, price, conn=None):
    own_connection = False
    if conn is None:
        conn = get_db_connection()
        own_connection = True
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(sql, (order_id, product_id, quantity, price))
        if own_connection:
            conn.commit()
    except Exception as e:
        if own_connection:
            conn.rollback()
        print(f"An error occurred while adding an order item: {e}")
    finally:
        if own_connection:
            conn.close()


# update the quantity of a product
def update_product_quantity(product_id, quantity_change, conn=None):
    own_connection = False
    if conn is None:
        conn = get_db_connection()
        own_connection = True

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Stock FROM Products WHERE ProductID = %s", (product_id,))
            result = cursor.fetchone()
            if result is None:
                raise ValueError(f"No product found with ProductID {product_id}")

            current_stock = result[0]
            new_stock = current_stock + quantity_change

            if new_stock < 0:
                raise ValueError(
                    f"Insufficient stock for product ID {product_id}. Current stock: {current_stock}, attempted change: {quantity_change}")

            cursor.execute("""
                UPDATE Products 
                SET Stock = %s 
                WHERE ProductID = %s
            """, (new_stock, product_id))

        if own_connection:
            conn.commit()
        return True
    except (pymysql.MySQLError, ValueError) as e:
        if own_connection:
            conn.rollback()
        print(f"An error occurred while updating product quantity: {e}")
        return False
    finally:
        if own_connection:
            conn.close()


# clear the cart
def clear_cart(username, conn=None):
    own_connection = False
    if conn is None:
        conn = get_db_connection()
        own_connection = True
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM CartItems WHERE Username = %s"
            cursor.execute(sql, (username,))
        if own_connection:
            conn.commit()
    except Exception as e:
        if own_connection:
            conn.rollback()
        print(f"An error occurred while clearing the cart: {e}")
    finally:
        if own_connection:
            conn.close()


# get all orders for a user
def get_orders(username):
    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Commands WHERE Username = %s", (username,))
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return []


# get all items in an order
def get_order_items(order_id):
    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_query = """
                    SELECT o.*, p.Name 
                    FROM OrderItems o 
                    JOIN Products p ON o.ProductID = p.ProductID
                    WHERE o.OrderID = %s
                """
                cursor.execute(sql_query, (order_id,))
                results = cursor.fetchall()
                return results
    except Exception as e:
        print(f"Error: {e}")
        return []


# get the total sales by category
def get_total_sales_by_category():
    query = """
    SELECT c.Name AS CategoryName, SUM(o.Quantity * o.UnitPrice) AS TotalSales
    FROM OrderItems o
    JOIN Products p ON o.ProductID = p.ProductID
    JOIN Categories c ON p.CategorieID = c.CategorieID
    GROUP BY c.CategorieID
    ORDER BY TotalSales DESC;
    """
    with get_db_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()


# get the total sales by product
def get_never_ordered_products():
    query = """
    SELECT *
    FROM Products
    WHERE ProductID NOT IN (SELECT DISTINCT ProductID FROM OrderItems);
    """
    with get_db_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()


# get the most popular product
def get_most_popular_product():
    query = """
    SELECT p.Name, SUM(oi.Quantity) AS TotalQuantity
    FROM Products p
    JOIN OrderItems oi ON p.ProductID = oi.ProductID
    GROUP BY p.ProductID
    ORDER BY TotalQuantity DESC
    LIMIT 1;
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
    return result


# get the highest spending customer
def get_highest_spending_customer():
    query = """
    SELECT u.Name, SUM(oi.Quantity * oi.UnitPrice) AS TotalSpent
    FROM Users u
    JOIN Commands c ON u.Username = c.Username
    JOIN OrderItems oi ON c.OrderID = oi.OrderID
    GROUP BY u.Username
    ORDER BY TotalSpent DESC
    LIMIT 1;
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
    return result


# get the average rating per category
def get_average_rating_per_category():
    query = """
    SELECT cat.Name AS CategoryName, AVG(pr.Note) AS AverageRating
    FROM Categories cat
    JOIN Products p ON cat.CategorieID = p.CategorieID
    JOIN ProductReviews pr ON p.ProductID = pr.ProductID
    GROUP BY cat.CategorieID
    ORDER BY AverageRating DESC;
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
    return results


# get the percentage of products that have never been sold
def get_percentage_never_sold():
    query = """
    SELECT ROUND((COUNT(DISTINCT p.ProductID) / (SELECT COUNT(*) FROM Products) * 100), 2) AS PercentageNeverSold
    FROM Products p
    LEFT JOIN OrderItems oi ON p.ProductID = oi.ProductID
    WHERE oi.ProductID IS NULL;
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
    return result

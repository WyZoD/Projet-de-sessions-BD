import pymysql
from flask.cli import load_dotenv
import os
import pymysql.cursors
import bcrypt


from werkzeug.security import generate_password_hash

load_dotenv()


def get_db_connection():
    return pymysql.connect(
        host=os.environ.get("host"),
        port=int(os.environ.get("port")),
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        db=os.environ.get("database"),
        autocommit=True
    )


def add_user(username, password, email, name, address):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("Insert into users (username, password, email, name, address, InscriptionDate) "
                               "values (%s, %s, %s, %s, %s, NOW())",
                               (username, hashed_password, email, name, address,))
                connection.commit()
                return True
            except Exception as e:
                print(e)
                connection.rollback()
                return False


def get_user_by_email(email):
    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                return cursor.fetchone()
    except Exception as e:
        print(e)
        return None


def get_all_products():
    try:
        with get_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Products")
                return cursor.fetchall()
    except Exception as e:
        print(e)
        return []


def get_product_by_id(product_id):
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Products WHERE ProductID = %s", (product_id,))
        product = cursor.fetchone()
    return product


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


#CART -------------------------------------------------
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


def create_order(username):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Commands (Username, DateCommand, Status)
            VALUES (%s, NOW(), 'Pending')
            """
            cursor.execute(sql, (username,))
            order_id = cursor.lastrowid
        conn.commit()
        return order_id
    except Exception as e:
        print(f"An error occurred while creating the order: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def add_order_item(order_id, product_id, quantity, price):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO OrderItems (OrderID, ProductID, Quantite, PrixUnitaire)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (order_id, product_id, quantity, price))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while adding an order item: {e}")
        conn.rollback()
    finally:
        conn.close()


def update_product_quantity(product_id, quantity_change):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Stock FROM Products WHERE ProductID = %s", (product_id,))
            current_stock = cursor.fetchone()[0]

            if current_stock + quantity_change < 0:
                print("Attempted to reduce stock below zero. Operation cancelled.")
                return False

            sql = """
            UPDATE Products 
            SET Stock = Stock + %s 
            WHERE ProductID = %s
            """
            cursor.execute(sql, (quantity_change, product_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"An error occurred while updating product quantity: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def clear_cart(username):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM CartItems WHERE Username = %s"
            cursor.execute(sql, (username,))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while clearing the cart: {e}")
        conn.rollback()
    finally:
        conn.close()




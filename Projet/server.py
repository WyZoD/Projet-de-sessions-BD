import random
from flask import Flask, render_template, request, flash, redirect, url_for, session, g, jsonify, abort
from werkzeug.security import check_password_hash
import bcrypt
import re
from database import *

app = Flask(__name__)
app.config['TESTING'] = True
app.secret_key = 'mega_secret_key'


def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


# base route
@app.route("/")
def index():
    if 'username' in session:
        logged_in = True
        username = session['username']
    else:
        logged_in = False
        username = None
    products = get_all_products()
    return render_template('index.html', logged_in=logged_in, username=username, products=products)


# this route is used to get the user's username
@app.before_request
def before_request():
    g.logged_in = 'username' in session
    g.username = session.get('username')


# Signup page
@app.route("/signup/")
def signup():
    return render_template("signup.html")


# this route is used to add a new user to the database
@app.route("/addSignup/", methods=["POST"])
def add_signup():
    username = request.form.get("username", type=str)
    password = request.form.get("password", type=str)
    email = request.form.get("email", type=str)
    name = request.form.get("name", type=str)
    address = request.form.get("address", type=str)

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    if add_user(username, hashed_password, email, name, address):
        return redirect(url_for('login'))
    else:
        flash("User not added, this username or email address is already in use")
        return redirect(url_for('signup'))


# route to the product according to id
@app.route("/product/<int:product_id>/")
def product_page(product_id):
    product = get_product_by_id(product_id)
    reviews = get_reviews_by_product_id(product_id)
    logged_in = 'username' in session
    return render_template('product_page.html', product=product, reviews=reviews, logged_in=logged_in,
                           username=session.get('username'))


# this route is used to add a review to a product
@app.route("/add-review/<int:product_id>/", methods=["POST"])
def add_review(product_id):
    if 'username' not in session:
        flash("You must be logged in to add a review.")
        return redirect(url_for('login'))

    username = session['username']
    note = request.form['note']
    commentaire = request.form['commentaire']

    if add_product_review(product_id, username, note, commentaire):
        flash("Your review has been added.")
    else:
        flash("An error occurred while adding your review.")

    return redirect(url_for('product_page', product_id=product_id))


# this route is used to log the user in
@app.route("/login/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode('utf-8')

        user = get_user_by_email(email)

        if user and bcrypt.checkpw(password, user['Password'].encode('utf-8')):
            session['username'] = user['Username']
            return redirect(url_for('index'))
        else:
            error = "Invalid email or password"
            return render_template("login.html", error=error)
    return render_template("login.html", error=error)


# this route is used to add a product to the cart
@app.route("/add-to-cart/", methods=["POST"])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity", 1)

    if add_item_to_cart(username, product_id, quantity):
        flash("Item added to cart successfully")
    else:
        flash("Failed to add item to cart")

    return redirect(url_for('index'))


# this route is used to show the cart
@app.route("/cart/")
def show_cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cart_items = get_cart_items(username)
    logged_in = 'username' in session
    return render_template('cart.html', cart_items=cart_items, logged_in=logged_in, username=username)


# this route is used to log the user out
@app.route("/logout/")
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))


# this route is used to update the quantity of a product in the cart
@app.route("/update-quantity/<int:product_id>/", methods=["POST"])
def update_quantity(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    new_quantity = request.form.get('quantity', type=int)
    username = session['username']

    if new_quantity > 0:
        update_cart_item_quantity(username, product_id, new_quantity)
        flash("Quantity updated successfully.")
    else:
        flash("Invalid quantity.")

    return redirect(url_for('show_cart'))


# this route is used to remove a product from the cart
@app.route("/remove-from-cart/<int:product_id>/", methods=["POST"])
def remove_from_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    remove_item_from_cart(username, product_id)

    flash("Item removed from cart.")
    return redirect(url_for('show_cart'))


# this route is used to place an order
@app.route("/place-order/", methods=["POST"])
def place_order():
    if 'username' not in session:
        flash("You need to be logged in to place an order.", "error")
        return redirect(url_for('login'))

    username = session['username']
    delivery_address = request.form.get('delivery_address')  # Assuming delivery address comes from the form

    conn = get_db_connection()
    try:
        conn.begin()
        cart_items = get_cart_items(username)

        total = sum(item['Price'] * item['Quantity'] for item in cart_items)

        if not cart_items:
            raise Exception("Your cart is empty.")

        for item in cart_items:
            product = get_product_by_id(item['ProductID'], conn)
            if item['Quantity'] > product['Stock']:
                raise Exception(f"Insufficient stock for product ID {item['ProductID']}.")

        order_id = create_order(username, delivery_address, total, conn)

        for item in cart_items:
            update_product_quantity(item['ProductID'], -item['Quantity'], conn)
            add_order_item(order_id, item['ProductID'], item['Quantity'], item['Price'], conn)
        clear_cart(username, conn)
        conn.commit()
        flash("Your order has been placed successfully.")
    except Exception as e:
        conn.rollback()
        flash(f"An error occurred: {e}")
    finally:
        conn.close()
    return redirect(url_for('show_orders'))


# this route is used to show the user's orders
@app.route("/orders/")
def show_orders():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    orders = get_orders(username)

    for order in orders:
        order_id = order['OrderID']
        order['items'] = get_order_items(order_id)

    logged_in = 'username' in session
    return render_template('orders.html', orders=orders, logged_in=logged_in, username=username)


# this route is used to show the fun facts
@app.route("/fun-fact/")
def fun_fact():
    if 'username' not in session:
        flash("You need to be logged in to view fun facts.", "warning")
        return redirect(url_for('login'))

    most_popular_product = get_most_popular_product()
    highest_spending_customer = get_highest_spending_customer()
    average_rating_per_category = get_average_rating_per_category()
    percentage_never_sold = get_percentage_never_sold()
    sales_facts = get_total_sales_by_category()
    never_ordered_products = get_never_ordered_products()

    fun_facts = []

    if sales_facts:
        for fact in sales_facts:
            fun_facts.append(
                f"Category {fact['CategoryName']} has total sales of ${fact['TotalSales']:.2f}!")

    if never_ordered_products:
        product_count = len(never_ordered_products)
        fun_facts.append(f"Did you know? We have {product_count} products that have never been ordered!")

    if most_popular_product:
        fun_facts.append(
            f"The most popular product is {most_popular_product[0]} with {most_popular_product[1]} units sold.")

    if highest_spending_customer:
        fun_facts.append(
            f"Our highest spending customer is {highest_spending_customer[0]}, spending a total of ${highest_spending_customer[1]:.2f}.")

    if average_rating_per_category:
        for category in average_rating_per_category:
            fun_facts.append(f"Category {category[0]} has an average product rating of {category[1]:.2f} stars.")

    if percentage_never_sold:
        fun_facts.append(f"{percentage_never_sold[0]}% of our products have never been sold.")

    if not fun_facts:
        fun_facts.append("Our website is growing every day. Check back soon for more interesting facts!")

    return render_template("fun_fact.html", fun_facts=fun_facts)

# this work only in testing environment
@app.route('/shutdown', methods=['POST'])
def shutdown():
    if not app.config['TESTING']:
        abort(404)
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server is shutting down...'


if __name__ == '__main__':
    app.run()  # DO NOT PUT DEBUG=TRUE

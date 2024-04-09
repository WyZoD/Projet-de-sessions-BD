from flask import Flask, render_template, request, flash, redirect, url_for, session, g, abort
from werkzeug.security import check_password_hash
import bcrypt

from database import *

app = Flask(__name__)
app.config['TESTING'] = True
app.secret_key = 'dsadsadasdasdasdasdas'


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


@app.before_request
def before_request():
    g.logged_in = 'username' in session
    g.username = session.get('username')


@app.route("/signup/")
def signup():
    return render_template("signup.html")


@app.route("/addSignup/", methods=["POST"])
def add_signup():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    name = request.form["name"]
    address = request.form["address"]

    if add_user(username, password, email, name, address):
        return redirect(url_for('login'))
    else:
        flash("User not added, this username or email address is already in use")
        return redirect(url_for('signup'))


from flask import session


@app.route("/product/<int:product_id>/")
def product_page(product_id):
    product = get_product_by_id(product_id)
    reviews = get_reviews_by_product_id(product_id)
    logged_in = 'username' in session
    return render_template('product_page.html', product=product, reviews=reviews, logged_in=logged_in,
                           username=session.get('username'))


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


@app.route("/cart/")
def show_cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cart_items = get_cart_items(username)
    logged_in = 'username' in session
    return render_template('cart.html', cart_items=cart_items, logged_in=logged_in, username=username)


@app.route("/logout/")
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))


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


@app.route("/remove-from-cart/<int:product_id>/", methods=["POST"])
def remove_from_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    remove_item_from_cart(username, product_id)

    flash("Item removed from cart.")
    return redirect(url_for('show_cart'))


@app.route("/place-order/", methods=["POST"])
def place_order():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cart_items = get_cart_items(username)

    if not cart_items:
        flash("Your cart is empty.")
        return redirect(url_for('show_cart'))

    order_id = create_order(username)

    for item in cart_items:
        success = update_product_quantity(item['ProductID'], -item['Quantity'])
        if not success:
            flash(f"Could not place order for {item['Name']} due to insufficient stock.")
            return redirect(url_for('show_cart'))
        add_order_item(order_id, item['ProductID'], item['Quantity'], item['Price'])

    clear_cart(username)  #
    flash("Your order has been placed.")
    return redirect(url_for('show_cart'))


@app.route('/shutdown', methods=['POST'])
def shutdown():
    if not app.config['TESTING']:
        # Prevent using this route in non-testing environments
        abort(404)
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server is shutting down...'


if __name__ == '__main__':
    app.run(debug=True)  # essentials for the tests

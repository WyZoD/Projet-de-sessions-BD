from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
import bcrypt

from database import *

app = Flask(__name__)
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
        flash("User added successfully")
        return redirect(url_for('login'))
    else:
        flash("User not added, this username or email address is already in use")
        return redirect(url_for('signup'))


@app.route("/login/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode('utf-8')
        user = get_user_by_email(email)

        if user and bcrypt.checkpw(password, user['Password'].encode('utf-8')):
            flash("Logged in successfully!")
            session['username'] = user['Username']
            return redirect(url_for('index'))
        else:
            error = "Invalid email or password"
            return render_template("login.html", error=error)
    return render_template("login.html", error=error)


@app.route("/logout/")
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

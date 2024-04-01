from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

from database import *

app = Flask(__name__)
app.secret_key = 'dsadsadasdasdasdasdas'


@app.route("/")
def index():
    return render_template("index.html")


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
    if request.method == "POST":
        pass
    return render_template("login.html")



if __name__ == '__main__':
    app.run()
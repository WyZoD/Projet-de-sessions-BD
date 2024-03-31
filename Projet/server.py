from flask import Flask, render_template, request, jsonify

from database import Database

app = Flask(__name__)

db = Database()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, redirect
from flask_session import Session
import requests
import sqlite3
from catch import check_status, request_qr_code

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def home():
  return render_template("index.html")

@app.route("/start", methods=["GET", "POST"])
def start():
  qrcode = request_qr_code()
  items = []
  result = check_status(qrcode, items)

  return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
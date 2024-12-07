from flask import Flask, render_template, request, session 
from flask_session import Session
import requests
from catch import check_status, request_qr_code

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def home():
  return render_template("index.html")

@app.route("/events", methods=["GET", "POST"])
def events():
  return render_template("events.html", apple = "spplr")

@app.route("/host", methods=["GET", "POST"])
def host():
  return render_template("host.html")

if __name__ == '__main__':
    app.run(debug=True)
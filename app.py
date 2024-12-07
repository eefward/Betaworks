from flask import Flask, render_template, request, redirect
from flask_session import Session
import requests
import sqlite3

from functions import create_db

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("events", check_same_thread=False)
cur = con.cursor()
create_db()

@app.route("/", methods=["GET", "POST"])
def home():
  return render_template("index.html")

@app.route("/events", methods=["GET", "POST"])
def events():
  return render_template("events.html")

@app.route("/host", methods=["GET", "POST"])
def host():
  if request.method == "post":
     date = request.form.get("date")
     start = request.form.get("start")
     end = request.form.get("end")
     location = request.form.get("location")
     desc = request.form.get("desc")

     if not (date and start and end and location and desc): return "fill it all out"
     cur.execute("INSERT INTO events (date, start_time, end_time, description",
                 (date, start, end, desc))
     con.commit()
     return redirect("/")
  return render_template("host.html")

if __name__ == '__main__':
    app.run(debug=True)
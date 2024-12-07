from flask import Flask, render_template, request, session 
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def home():
  return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def apple():
  return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
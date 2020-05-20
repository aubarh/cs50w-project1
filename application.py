import os, json
from flask import Flask, session, render_template, request, jsonify, flash
from flask_session import Session
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":    # reached route via POST

        # check username
        if not request.form.get("username"):
            return render_template("error.html", message="Username not provided")

        # check db for username
        checkUsername = db.exectue("SELECT * FROM users WHERE username = :username",
                {"username":request.form.get("username")}).fetchone()

        # username already exists
        if checkUsername:
            return render_template("error.html", message="Username taken.")

        # check password
        elif  not request.form.get("password"):
            return render_template("error.html", message="Password not provided")

        # Hash password
        pwHash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # insert new user
        db.execute("INSERT INTO users (username, pasword) VALUES (:username, :pawssword)",
                {"username":request.form.get("username"),
                    "password":pwHash})
        db.commit()

        flash('Account created', 'info')

        return redirect("/login")

    else:   # reached route via GET
        return render_template("register.html")

@app.route("/login")
def login():
    return render_template("index.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()

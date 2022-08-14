import os

from flask import Flask, request, session, render_template, redirect, url_for
from sqlalchemy import create_engine, text
from argon2 import PasswordHasher

app = Flask(__name__)

ph = PasswordHasher()
engine = create_engine(f"sqlite:///{os.getcwd()}/database.db")

app.secret_key = os.urandom(24)

with engine.connect() as conn:
    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS logins (
                `password` VARCHAR(100) NULL,
                `username` VARCHAR(64) NULL UNIQUE,
                PRIMARY KEY (`username`)
            );
            """
        )
    )


@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    uname = request.form.get("username")
    passw = request.form.get("password")

    if not uname or not passw:
        return render_template("login.html", message="Please fill in all fields")

    with engine.connect() as conn:
        rslt = conn.execute(
            text(
                """
                SELECT * FROM logins WHERE `username`=:uname;
                """
            ),
            {
                "uname": uname
            }
        )
        rslt = rslt.all()
    if rslt == []:
        return render_template("login.html", message="Username not found")

    try:
        ph.verify(rslt[0][0], passw)
        session["username"] = uname
        return render_template("index.html")
    except:
        return render_template("login.html", message="Incorrect password")


@app.route("/register", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("register.html")

    uname = request.form.get("username")
    passw = request.form.get("password")
    passw2 = request.form.get("confirm-password")

    if uname == "" or passw == "" or passw2 == "":
        return render_template("register.html", message="Please fill in all fields")

    if passw != passw2:
        return render_template("register.html", message="Passwords do not match")

    with engine.connect() as conn:
        rslt = conn.execute(
            text(
                """
                SELECT * FROM logins WHERE `username`=:uname;
                """
            ),
            {
                "uname": uname
            }
        )
        rslt = rslt.all()
    if len(rslt) != 0:
        return render_template("register.html", message="Username already exists")

    hashed = ph.hash(passw)
    with engine.connect() as conn:
        conn.execute(
            text(
                """
                INSERT INTO logins (password, username) VALUES (:hashed, :uname);
                """
            ),
            {
                "hashed": hashed,
                "uname": uname
            }
        )
    return render_template("login.html", message="Successfully registered")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("login.html")


if __name__ == "__main__":
    app.run()

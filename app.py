from flask import Flask, render_template, redirect, url_for, request
from user import User

app: Flask = Flask(__name__)
current_user: User | None = None
users: list[User] = list()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username: str = request.form["username"]
        password: str = request.form["password"]
        email: str = request.form["email"]
        gender: str = request.form["gender"]
        users.append(User(username, password, email, gender))
    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run()

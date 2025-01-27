from flask import Flask, render_template, redirect, request
from werkzeug import Response

from classes import User, Login

app: Flask = Flask(__name__)
# app.debug = True
current_user: User | None = None
users: list[User] = list()


@app.route("/")
def home():
    if current_user is None:
        return redirect("login")
    else:
        return render_template("user.html", user=current_user)


@app.route("/signup", methods=["POST", "GET"])
def signup() -> str | Response:
    global current_user
    if current_user is None:
        if request.method == "POST":
            username: str = request.form["username"]
            password: str = request.form["password"]
            email: str = request.form["email"]
            gender: str = request.form["gender"]
            users.append(User(username, password, email, gender))
            current_user = users[-1]
            return render_template("user.html", user=current_user)
        return render_template("signup.html", user=current_user)
    else:
        return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login() -> str | Response:
    if current_user is None:
        if request.method == "POST":
            username: str = request.form["username"]
            password: str = request.form["password"]
            login_object: Login = Login(username, password)
            for user in users:
                if user == login_object:
                    return render_template("user.html", user=user)
        return render_template("login.html", user=current_user)
    else:
        return redirect("/")


@app.route("/user")
def userinfo():
    return render_template("user.html", user=current_user)


if __name__ == "__main__":
    app.run()

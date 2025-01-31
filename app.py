from flask import Flask, render_template, redirect, request, jsonify
from werkzeug.wrappers import Response
from classes import User, Login

app: Flask = Flask(__name__)
current_user: tuple[int, User] | None = None
users: list[tuple[int, User]] = list()


@app.route("/")
def home() -> str | Response:
    if current_user is None:
        return redirect("login")
    return render_template("user.html", user=current_user)


@app.route("/signup", methods=["POST", "GET"])
def signup() -> str | Response:
    global current_user
    if current_user is None:
        if request.method == "POST":
            username: str = request.form.get("username", "")
            password: str = request.form.get("password", "")
            email: str = request.form["email"]
            gender: str = request.form["gender"]
            users.append(
                (
                    len(users) - 1 if len(users) > 0 else 0,
                    User(username, password, email, gender),
                )
            )
            current_user = users[-1]
            return redirect("/")
        return render_template("signup.html", user=current_user)
    return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login() -> str | Response:
    global current_user
    if current_user is None:
        if request.method == "POST":
            username: str = request.form["username"]
            password: str = request.form["password"]
            login_object: Login = Login(username, password)
            for user in users:
                if user[1] == login_object:
                    current_user = user
                    return redirect("/")
        return render_template("login.html", user=current_user)
    return redirect("/")


@app.route("/logout", methods=["POST"])
def logout():
    global current_user
    current_user = None
    return jsonify(success=True)


@app.route("/updateuser", methods=["POST", "GET"])
def updateuser() -> str | Response:
    global current_user
    if current_user is None:
        return redirect("login")
    if request.method == "POST":
        changed_username: str = request.form["username"]
        changed_password: str = request.form["password"]
        changed_email: str = request.form["email"]
        changed_gender: str = request.form["gender"]
        changed_user: tuple[int, User] = current_user[0], User(
            changed_username, changed_password, changed_email, changed_gender
        )
        users.insert(current_user[0], changed_user)
        users.pop(current_user[0] + 1)
        current_user = changed_user
        return redirect("/")

    return render_template("datachange.html", user=current_user)


if __name__ == "__main__":
    app.run()

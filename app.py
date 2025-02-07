from flask import Flask, render_template, redirect, request, jsonify
import sqlite3 as sql
from werkzeug.wrappers import Response

app: Flask = Flask(__name__)
current_user: tuple[str, str, str, str] | None = None


@app.route("/")
def home() -> str | Response:
    if current_user is None:
        return redirect("login")
    return render_template("user.html", user=current_user)


@app.route("/signup", methods=["POST", "GET"])
def signup() -> str | Response:
    global current_user

    if current_user is not None:
        return redirect("/")

    if request.method == "POST":
        username: str = request.form["username"]
        password: str = request.form["password"]
        email: str = request.form["email"]
        gender: str = request.form["gender"]

        connection = sql.connect("user.db")
        connection.autocommit = True
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"""
                    INSERT INTO "user"
                    VALUES(?, ?, ?, ?)
                """,
                (username, password, email, gender),
            )
        except sql.IntegrityError:
            return render_template("signup.html", error="email exists")

        current_user = username, password, email, gender

        connection.close()

        return redirect("/")

    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login() -> str | Response:
    global current_user

    if current_user is not None:
        return redirect("/")

    if request.method == "POST":
        email: str = request.form["email"]
        password: str = request.form["password"]

        connection = sql.connect("user.db")
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM user;")
        for user in cursor.fetchall():
            if user[2] == email and user[1] == password:
                current_user = user
                connection.close()
                return redirect("/")
        connection.close()
        return render_template("login.html", error="user not found")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout() -> Response:
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

        connection = sql.connect("user.db")
        connection.autocommit = True
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"""
		    		UPDATE user
		    		SET username = ?,
		    		password = ?,
		    		email = ?,
		    		gender = ?
		    		WHERE username = ?
		    	""",
                (
                    changed_username,
                    changed_password,
                    changed_email,
                    changed_gender,
                    current_user[0],
                ),
            )
        except sql.IntegrityError:
            return render_template("datachange.html", error="email exists")

        connection.close()

        changed_user: tuple[str, str, str, str] = (
            changed_username,
            changed_password,
            changed_email,
            changed_gender,
        )
        current_user = changed_user

        return redirect("/")
    return render_template("datachange.html", user=current_user)


if __name__ == "__main__":
    app.run(debug=True)

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
        current_user = users[-1]
        return redirect(url_for('user'))
    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username: str = request.form['username']
        password: str = request.form['password']
    return render_template("login.html")

@app.route('/user')
def userinfo():
    return render_template('user.html', user=current_user)


if __name__ == "__main__":
    app.run()

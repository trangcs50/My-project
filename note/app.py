from cs50 import SQL
from flask import Flask, render_template, request, redirect, flash
from flask_session import Session
from flask_login import UserMixin, login_required, current_user, login_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "mysecretkey"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
db = SQL("sqlite:///note.db")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def user_loader(user_id):
    rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if rows:
        row = rows[0]
        return User(row["id"], row["username"], row["password"])
    return None


@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        error = False
        if not username:
            flash("Must provide username")
            error = True
        password = request.form.get("password")
        if not password:
            flash("Must provide password")
            error = True
        hash_password = generate_password_hash(password)
        confirmation = request.form.get("confirmation")
        if not confirmation:
            flash("Must provide confirmation")
            error = True
        if password != confirmation:
            flash("Invalid confirmation or password")
            error = True
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if rows:
            flash("This username has already been used")
            error = True
        if error:
            return render_template("register.html")
        db.execute("INSERT INTO users(username, password) VALUES(?, ?)", username, hash_password)
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        error = False
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username:
            flash("Must provide username")
            error = True
        password = request.form.get("password")
        if not password:
            flash("Must provide password")
            error = True
        if not rows or not check_password_hash(rows[0]["password"], password):
            flash("Invalid username or password")
            error = True

        if error:
            return render_template("login.html")
        
        if rows:
            row = rows[0]
            user = User(row["id"], row["username"], row["password"])
            login_user(user)
            return redirect("/")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
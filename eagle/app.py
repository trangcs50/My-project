from flask import Flask, request, render_template, redirect, url_for, flash
import re
import os
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myminigrab'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
db = SQL("sqlite:///grab.db")
Session(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, name, phone, address, password_hash, role):
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address
        self.password_hash = password_hash
        self.role = role
@login_manager.user_loader
def user_loader(user_id):
    rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if rows:
        row = rows[0]
        return User(row["id"], row["name"], row["phone"], row["address"], row["password_hash"], row["role"])
    return None

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        error = False
        username = request.form.get("username")
        if not username:
            flash("Must provide username")
            error = True
        password = request.form.get("password")
        if not password:
            flash("Must provide password")
            error = True
        rows = db.execute("SELECT * FROM users WHERE name = ?", username)
        if not rows or not check_password_hash(rows[0]["password_hash"], password):
            flash("Invalid username or password") 
            error = True
        if error:
            return render_template("login.html")
        if rows:
            row = rows[0]
            user = User(row["id"], row["name"], row["phone"], row["address"], row["password_hash"], row["role"])
            login_user(user)
        if rows[0]['role'] == 'customer':
            return redirect(url_for("index_customer"))
        elif rows[0]['role'] == 'restaurant':
            return redirect(url_for("index_restaurant"))
    return render_template("login.html")

@app.route("/")
@login_required
def index_customer():
    rows = db.execute("SELECT * FROM dishes")
    return render_template("index_c.html", rows=rows)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        error = False
        username = request.form.get("username")
        if not username:
            flash("Must provide username")
            error = True
        password = request.form.get("password")
        if not password:
            flash("Must provide password")
            error = True
        confirmation = request.form.get("confirmation")
        if not confirmation:
            flash("Must provide confirmation")
            error = True
        if password != confirmation:
            flash("Invalid password or confirmation")
            error = True
        rows = db.execute("SELECT * FROM users WHERE name = ?", username)
        if rows:
            flash("This username has already existed")
            error = True
        option = request.form.get("option")
        if not option:
            flash("Must provide option")
            error = True
        if option not in ['customer', 'restaurant']:
            flash("Invalid option")
            error = True
        phone = request.form.get("phone")
        if not phone:
            flash("Must provide phone number")
            error = True
        if len(str(phone)) > 15 and len(str(phone)) < 9 or not re.fullmatch(r"^\+?[0-9]{9,15}$", phone):
            flash("Invalid phone number")
            error = True
        address = request.form.get("address")
        if not address:
            flash("Must provide address")
            error = True
        if not re.fullmatch(r"^[0-9]{1,5}(,\s*|\s+)[A-Za-z\s]+(,\s*[A-Za-z\s]+)*$", address):
            flash("Invalid address")
            error = True
        if error:
            return render_template("register.html")
        hash_password = generate_password_hash(password)
        db.execute("INSERT INTO users(name, password_hash, role, address, phone) VALUES(?, ?, ?, ?, ?)", username, hash_password, option, address, phone)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/role", methods=["POST", "GET"])
def role():
    if request.method == "POST":
        name = request.form.get("name")
        error = False
        if not name:
            flash("Must provide Restaurant's name")
            error = True
        address = request.form.get("address_restaurant")
        if not address:
            flash("Must provide address")
            error = True
        if not re.fullmatch(r"^[0-9]{1,5}(,\s*|\s+)[A-Za-z\s]+(,\s*[A-Za-z\s]+)*$", address):
            flash("Invalid address")
            error = True
        phonenumber = request.form.get("phone_restaurant")
        if not phonenumber:
            flash("Must provide Phone Number")
            error = True
        if not re.fullmatch(r"^\+?[0-9]{9,15}$", phonenumber):
            flash("Invalid Phone Number")
            error = True
        dish = request.form.get("dishes")
        if not dish:
            flash("Must provide your main dish")
            error = True
        price = request.form.get("price")
        if not price:
            flash("Must provide price")
            error = True
        description = request.form.get("description")
        if error:
            return render_template("role.html")
        db.execute("INSERT INTO restaurants(name, address, phone) VALUES(?, ?, ?)", name, address, phonenumber )
        rows = db.execute("SELECT * FROM restaurants WHERE address = ?", address)
        db.execute("INSERT INTO dishes( restaurant_id ,name, price, description) VALUES(?,?, ?, ?)", rows[0]['id'], dish, price, description)
        return redirect(url_for("index_restaurant"))
    return render_template("role.html")

@app.route("/index_r")
def index_restaurant():
    return render_template("index_r.html")

@app.route("/cart", methods=["POST", "GET"])
def cart():
    
    return "My cart"
if __name__ == "__main__":
    app.run(debug=True)
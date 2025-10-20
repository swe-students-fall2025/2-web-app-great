from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from .db import get_db

login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(UserMixin):
    def __init__(self, doc):
        self.id = str(doc['_id'])
        self.email = doc.get('email')
        self.name = doc.get('name', self.email)

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    doc = db.users.find_one({'_id': ObjectId(user_id)})
    return User(doc) if doc else None

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        db = get_db()
        user = db.users.find_one({"email": email})
        if user and check_password_hash(user.get("password_hash",""), password):
            login_user(User(user))
            flash("Welcome back!", "ok")
            return redirect(url_for("main.index"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        db = get_db()
        if db.users.find_one({"email": email}):
            flash("Email already registered.", "error")
            return render_template("register.html")
        db.users.insert_one({
            "name": name,
            "email": email,
            "password_hash": generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        })
        flash("Account created. Please log in.", "ok")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "ok")
    return redirect(url_for("main.index"))

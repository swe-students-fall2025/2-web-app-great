# loopu/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db import get_db
from bson.objectid import ObjectId
from datetime import date

bp = Blueprint("main", __name__)

# Home page
@bp.route("/")
def index():
    return render_template("index.html")

# Item listing page
@bp.route("/items")
def items_list():
    db = get_db()
    items = list(db.items.find().sort("_id", -1))
    return render_template("my_listing.html", items=items)

# Add a new item
@bp.route("/items/add", methods=["GET", "POST"])
def items_add():
    db = get_db()
    if request.method == "POST":
        doc = {
            "title": request.form.get("title", "").strip(),
            "price": float(request.form.get("price", 0) or 0),
            "category": request.form.get("category", "").strip(),
            "school": request.form.get("school", "").strip(),
            "description": request.form.get("description", "").strip(),
            "image_url": request.form.get("image_url", "").strip(),
            "post_date": date.today().isoformat(),
        }
        db.items.insert_one(doc)
        flash("Item created!", "success")
        return redirect(url_for("main.items_list"))
    return render_template("publish.html")

# Shortcut alias: /publish -> /items/add
@bp.route("/publish")
def publish_alias():
    return redirect(url_for("main.items_add"))

# Shopping cart page (currently static placeholder)
@bp.route("/cart")
def cart():
    return render_template("cart.html")

# Checkout (GET: show form; POST: process form)
@bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    # Example order data (replace with real session/db data)
    order = {
        "item_title": "IKEA study table",
        "item_price": 20,
        "qty": 1,
    }
    order["total"] = order["item_price"] * order["qty"]

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        pickup = request.form.get("pickup", "").strip()
        email = request.form.get("email", "").strip()
        payment = request.form.get("payment", "").strip()

        # TODO: Save order into database
        # db = get_db()
        # db.orders.insert_one({...})

        flash("Order placed! ✅", "success")
        return redirect(url_for("main.index"))

    return render_template("checkout.html", **order)

# Remove item from cart (placeholder)
@bp.route("/cart/remove/<item_id>")
def cart_remove(item_id):
    # TODO: Remove item_id from session or db
    flash("Removed from cart (placeholder).", "info")
    return redirect(url_for("main.cart"))

# Contact seller (simple version)
@bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        msg = request.form.get("message", "").strip()
        # TODO: Save message into db or send via WebSocket
        flash(f"Message sent: {msg}", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")

# Edit item
@bp.route("/items/edit/<item_id>", methods=["GET", "POST"])
def items_edit(item_id):
    db = get_db()
    try:
        oid = ObjectId(item_id)
    except Exception:
        flash("Invalid item id", "error")
        return redirect(url_for("main.items_list"))

    item = db.items.find_one({"_id": oid})
    if not item:
        flash("Item not found", "error")
        return redirect(url_for("main.items_list"))

    if request.method == "POST":
        db.items.update_one(
            {"_id": oid},
            {
                "$set": {
                    "title": request.form.get("title"),
                    "price": float(request.form.get("price", 0) or 0),
                    "category": request.form.get("category"),
                    "school": request.form.get("school"),
                    "description": request.form.get("description"),
                }
            },
        )
        flash("Item updated!", "success")
        return redirect(url_for("main.items_list"))

    return render_template("edit.html", item=item)

# Delete item
@bp.route("/items/delete/<item_id>")
def items_delete(item_id):
    db = get_db()
    try:
        oid = ObjectId(item_id)
        db.items.delete_one({"_id": oid})
        flash("Item deleted!", "info")
    except Exception:
        flash("Invalid item id", "error")
    return redirect(url_for("main.items_list"))

# Login (plain text check; use hash + Flask-Login in real app)
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db()
        user = db.users.find_one({"email": email})

        if user and user.get("password") == password:
            flash("Login successful!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid email or password", "error")

    return render_template("login.html")

# My listings (currently all items; later filter by user_id in session)
@bp.route("/my-listing")
def my_listing():
    db = get_db()
    items = list(db.items.find().sort("_id", -1))
    return render_template("my_listing.html", items=items)

# Item detail
@bp.route("/items/<item_id>")
def item_detail(item_id):
    db = get_db()
    try:
        oid = ObjectId(item_id)
    except Exception:
        flash("Invalid item id", "error")
        return redirect(url_for("main.my_listing"))

    it = db.items.find_one({"_id": oid})
    if not it:
        flash("Item not found", "error")
        return redirect(url_for("main.my_listing"))

    # Add default post_date if missing
    if "post_date" not in it or not it["post_date"]:
        it["post_date"] = date.today().isoformat()

    return render_template("product_detail.html", item=it)

# Signup
@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        name = request.form.get("name", "").strip()
        school = request.form.get("school", "").strip()

        if not email.endswith(".edu"):
            flash("Please use your school .edu email", "error")
            return redirect(url_for("main.signup"))

        db = get_db()
        existing = db.users.find_one({"email": email})
        if existing:
            flash("Email already registered", "error")
            return redirect(url_for("main.signup"))

        db.users.insert_one({
            "email": email,
            "password": password,   # ⚠️ Use hashed password in production
            "name": name,
            "school": school,
        })
        flash("Signup successful! Please login.", "success")
        return redirect(url_for("main.login"))

    return render_template("signup.html")

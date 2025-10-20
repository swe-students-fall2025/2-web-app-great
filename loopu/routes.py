from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bson import ObjectId
from .db import get_db

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    db = get_db()
    items = list(db.items.find().sort([("_id",-1)]))
    return render_template("index.html", items=items)

@bp.route("/item/<item_id>")
def product_detail(item_id):
    db = get_db()
    try:
        item = db.items.find_one({"_id": ObjectId(item_id)})
    except Exception:
        item = None
    if not item:
        flash("Item not found.", "error")
        return redirect(url_for("main.index"))
    return render_template("product_detail.html", item=item)

@bp.route("/publish", methods=["GET","POST"])
@login_required
def publish():
    db = get_db()
    if request.method == "POST":
        data = {
            "title": request.form.get("title","").strip(),
            "price": float(request.form.get("price","0") or 0),
            "category": request.form.get("category","").strip(),
            "school": request.form.get("school","").strip(),
            "desc": request.form.get("desc","").strip(),
            "owner_id": ObjectId(current_user.id)
        }
        db.items.insert_one(data)
        flash("Item published.", "ok")
        return redirect(url_for("main.my_listing"))
    return render_template("publish.html")

@bp.route("/my-listing")
@login_required
def my_listing():
    db = get_db()
    items = list(db.items.find({"owner_id": ObjectId(current_user.id)}).sort([("_id",-1)]))
    return render_template("my_listing.html", items=items)

@bp.route("/edit/<item_id>", methods=["GET","POST"])
@login_required
def edit(item_id):
    db = get_db()
    item = db.items.find_one({"_id": ObjectId(item_id), "owner_id": ObjectId(current_user.id)})
    if not item:
        flash("Item not found or no permission.", "error")
        return redirect(url_for("main.my_listing"))
    if request.method == "POST":
        update = {
            "title": request.form.get("title","").strip(),
            "price": float(request.form.get("price","0") or 0),
            "category": request.form.get("category","").strip(),
            "school": request.form.get("school","").strip(),
            "desc": request.form.get("desc","").strip(),
        }
        db.items.update_one({"_id": item["_id"]}, {"$set": update})
        flash("Item updated.", "ok")
        return redirect(url_for("main.my_listing"))
    return render_template("edit.html", item=item)

@bp.route("/delete/<item_id>", methods=["POST"])
@login_required
def delete(item_id):
    db = get_db()
    db.items.delete_one({"_id": ObjectId(item_id), "owner_id": ObjectId(current_user.id)})
    flash("Item deleted.", "ok")
    return redirect(url_for("main.my_listing"))

@bp.route("/search")
def search():
    db = get_db()
    keyword = request.args.get("q","").strip()
    results = []
    if keyword:
        results = list(db.items.find({
            "$or": [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"desc": {"$regex": keyword, "$options": "i"}},
                {"category": {"$regex": keyword, "$options": "i"}},
                {"school": {"$regex": keyword, "$options": "i"}}
            ]
        }).sort([("_id",-1)]))
    return render_template("search.html", keyword=keyword, items=results)

@bp.route("/contact/<item_id>")
def contact(item_id):
    return render_template("not_available.html")

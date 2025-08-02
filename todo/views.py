from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import Todo

bp = Blueprint("views", __name__)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        return render_template("index.html", todos=todos)
    return render_template("index.html")


@bp.route("/add", methods=["POST"])
@login_required
def add():
    todo_text = request.form.get("todo")
    new_todo = Todo(text=todo_text, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("views.index"))


@bp.route("/delete/<int:todo_id>")
@login_required
def delete(todo_id):
    todo_to_delete = Todo.query.get_or_404(todo_id)
    if todo_to_delete.user_id != current_user.id:
        flash("You don't have permission to delete this item.", "danger")
        return redirect(url_for("views.index"))
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for("views.index"))

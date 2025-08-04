from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import Todo

bp = Blueprint("views", __name__)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        todos = (
            Todo.query.filter_by(user_id=current_user.id)
            .order_by(db.asc(Todo.complete))
            .all()
        )
        return render_template("index.html", todos=todos)
    return render_template("index.html")


@bp.route("/add", methods=["POST"])
@login_required
def add():
    todo_text = request.form.get("todo")
    new_todo = Todo(text=todo_text, user_id=current_user.id)  # type: ignore
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("views.index"))


@bp.route("/delete/<int:todo_id>")
@login_required
def delete(todo_id):
    todo_to_delete = Todo.query.filter_by(
        id=todo_id, user_id=current_user.id
    ).first_or_404()
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for("views.index"))


@bp.route("/complete/<int:todo_id>", methods=["POST"])
@login_required
def complete(todo_id):
    todo_to_complete = Todo.query.filter_by(
        id=todo_id, user_id=current_user.id
    ).first_or_404()
    todo_to_complete.complete = not todo_to_complete.complete
    db.session.commit()
    flash("To-do item status updated.", "success")
    return redirect(url_for("views.index"))


@bp.route("/edit/<int:todo_id>", methods=["GET", "POST"])
@login_required
def edit(todo_id):
    todo_to_edit = Todo.query.filter_by(
        id=todo_id, user_id=current_user.id
    ).first_or_404()
    if request.method == "POST":
        new_text = request.form.get("todo")
        if new_text:
            todo_to_edit.text = new_text
            db.session.commit()
            flash("To-do item updated successfully.", "success")
        return redirect(url_for("views.index"))

    return render_template("edit.html", todo=todo_to_edit)

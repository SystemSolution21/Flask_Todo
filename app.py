from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

todos = []


@app.route("/")
def index():
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    todo = request.form.get("todo")
    if todo:
        todos.append(todo)
    return redirect(url_for("index"))


@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

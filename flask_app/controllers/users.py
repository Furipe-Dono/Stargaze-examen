from flask import (
    render_template,
    redirect,
    request,
    session,
    flash
)

from flask_app import app, bcrypt
from flask_app.models.user import User


@app.route("/")
def index():

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():

    if not User.validate_registration(request.form):
        return redirect("/")

    password_hash = bcrypt.generate_password_hash(
        request.form["password"]
    )

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": password_hash
    }

    user_id = User.create(data)

    session["user_id"] = user_id
    session["first_name"] = request.form["first_name"]

    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login():

    user = User.get_by_email({
        "email": request.form["email"]
    })

    if not user:
        flash(
            "Correo o contraseña incorrectos.",
            "login"
        )
        return redirect("/")

    if not bcrypt.check_password_hash(
        user.password,
        request.form["password"]
    ):
        flash(
            "Correo o contraseña incorrectos.",
            "login"
        )
        return redirect("/")

    session["user_id"] = user.id
    session["first_name"] = user.first_name

    return redirect("/dashboard")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
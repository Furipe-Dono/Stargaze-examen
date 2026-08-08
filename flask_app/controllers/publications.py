from flask import (
    render_template,
    redirect,
    request,
    session,
    flash
)

from flask_app import app
from flask_app.models.publication import Publication


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    publications = Publication.get_all({
        "user_id": session["user_id"]
    })

    return render_template(
        "dashboard.html",
        publications=publications
    )


@app.route("/publications/create", methods=["POST"])
def create_publication():

    if "user_id" not in session:
        return redirect("/")

    if not Publication.validate_publication(request.form):
        return redirect("/dashboard")

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "event_date": request.form["event_date"],
        "location": request.form["location"],
        "user_id": session["user_id"]
    }

    Publication.create(data)

    return redirect("/dashboard")


@app.route("/publications/edit/<int:id>")
def edit_publication(id):

    if "user_id" not in session:
        return redirect("/")

    publication = Publication.get_by_id({
        "id": id
    })

    if not publication:
        return redirect("/dashboard")

    if publication.user_id != session["user_id"]:
        flash(
            "No tienes permiso para editar esta publicación.",
            "publication"
        )
        return redirect("/dashboard")

    return render_template(
        "edit_publication.html",
        publication=publication
    )


@app.route("/publications/update/<int:id>", methods=["POST"])
def update_publication(id):

    if "user_id" not in session:
        return redirect("/")

    publication = Publication.get_by_id({
        "id": id
    })

    if not publication:
        return redirect("/dashboard")

    if publication.user_id != session["user_id"]:
        return redirect("/dashboard")

    if not Publication.validate_publication(
        request.form,
        publication_id=id
    ):
        return redirect(f"/publications/edit/{id}")

    data = {
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"],
        "event_date": request.form["event_date"],
        "location": request.form["location"]
    }

    Publication.update(data)

    return redirect("/dashboard")


@app.route("/publications/delete/<int:id>")
def delete_publication(id):

    if "user_id" not in session:
        return redirect("/")

    publication = Publication.get_by_id({
        "id": id
    })

    if not publication:
        return redirect("/dashboard")

    if publication.user_id != session["user_id"]:
        return redirect("/dashboard")

    Publication.delete({
        "id": id
    })

    return redirect("/dashboard")


@app.route("/publications/like/<int:id>")
def like_publication(id):

    if "user_id" not in session:
        return redirect("/")

    Publication.add_like({
        "user_id": session["user_id"],
        "publication_id": id
    })

    return redirect("/dashboard")
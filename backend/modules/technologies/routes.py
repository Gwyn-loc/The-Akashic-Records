
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from database import db
from database.models import Technology
from backend.modules.technologies.forms import TechnologySubmissionForm

bp = Blueprint("technologies", __name__, url_prefix="/technologies")


@bp.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    form = TechnologySubmissionForm()

    if form.validate_on_submit():
        technology = Technology(
            name=form.name.data.strip(),
            year=form.year.data,
            era=form.era.data.strip(),
            category=form.category.data.strip(),
            inventor=form.inventor.data.strip(),
            place_of_origin=form.place_of_origin.data.strip(),
            description=form.description.data.strip(),
            significance=form.significance.data.strip(),
            source=form.source.data.strip(),
            user_id=current_user.id,
            status="pending",
        )

        db.session.add(technology)
        db.session.commit()

        flash("Your technology submission has been sent for administrator review.", "success")
        return redirect(url_for("technologies.submit"), code=303)

    return render_template("technologies/submit.html", form=form), (
        422 if form.is_submitted() else 200
    )

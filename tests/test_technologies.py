
from database import db
from database.models import Technology
from tests.conftest import PASSWORD, csrf, login, post_form


def technology_values(**overrides):
    values = {
        "name": "Printing Press",
        "year": "1440",
        "era": "Renaissance",
        "category": "Communication",
        "inventor": "Johannes Gutenberg",
        "place_of_origin": "Mainz, Germany",
        "description": (
            "A mechanical printing technology that used movable "
            "metal type to reproduce written text efficiently."
        ),
        "significance": (
            "The printing press helped spread knowledge, improve "
            "access to books, and encourage literacy."
        ),
        "source": "Encyclopaedia Britannica - History of Printing",
    }
    values.update(overrides)
    return values


def create_technology(app, user_id, status, **overrides):
    with app.app_context():
        values = technology_values(**overrides)
        technology = Technology(
            name=values["name"],
            year=int(values["year"]),
            era=values["era"],
            category=values["category"],
            inventor=values["inventor"],
            place_of_origin=values["place_of_origin"],
            description=values["description"],
            significance=values["significance"],
            source=values["source"],
            user_id=user_id,
            status=status,
        )
        db.session.add(technology)
        db.session.commit()
        return technology.id


def test_public_api_only_shows_approved_technologies(app, client, users):
    create_technology(app, users["ada"], "approved")
    create_technology(
        app,
        users["ada"],
        "pending",
        name="Pending Invention",
    )
    create_technology(
        app,
        users["ada"],
        "rejected",
        name="Rejected Invention",
    )

    response = client.get("/api/v1/technologies")

    assert response.status_code == 200
    records = response.json["data"]
    names = [record["name"] for record in records]

    assert "Printing Press" in names
    assert "Pending Invention" not in names
    assert "Rejected Invention" not in names


def test_member_cannot_approve_reject_or_delete_technology(
    app, client, users
):
    technology_id = create_technology(
        app, users["ada"], "pending"
    )
    login(client)

    approve = post_form(
        client,
        f"/admin/technologies/{technology_id}/approve",
    )
    reject = post_form(
        client,
        f"/admin/technologies/{technology_id}/reject",
    )
    delete = post_form(
        client,
        f"/admin/technologies/{technology_id}/delete",
    )

    assert approve.status_code == 403
    assert reject.status_code == 403
    assert delete.status_code == 403

    with app.app_context():
        technology = db.session.get(Technology, technology_id)
        assert technology is not None
        assert technology.status == "pending"


def test_valid_submission_is_saved_as_pending(app, client, users):
    login(client)

    response = post_form(
        client,
        "/technologies/submit",
        **technology_values(),
    )

    assert response.status_code == 303

    with app.app_context():
        technology = db.session.scalar(
            db.select(Technology).where(
                Technology.name == "Printing Press"
            )
        )
        assert technology is not None
        assert technology.status == "pending"
        assert technology.user_id == users["ada"]


def test_incomplete_submission_is_rejected(app, client, users):
    login(client)

    response = post_form(
        client,
        "/technologies/submit",
        **technology_values(name=""),
    )

    assert response.status_code == 422

    with app.app_context():
        count = db.session.scalar(
            db.select(db.func.count(Technology.id))
        )
        assert count == 0


from database import db
from database.models.base import OwnedRecord


class Technology(OwnedRecord, db.Model):
    __tablename__ = "technologies"

    name = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    era = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    inventor = db.Column(db.String(150), nullable=False)
    place_of_origin = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    significance = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
        index=True
    )

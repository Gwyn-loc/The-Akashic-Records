
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
)


class TechnologySubmissionForm(FlaskForm):
    name = StringField(
        "Technology name",
        validators=[DataRequired(), Length(max=150)]
    )

    year = IntegerField(
        "Approximate year (use negative numbers for BCE)",
        validators=[DataRequired(), NumberRange(min=-1000000)]
    )

    era = StringField(
        "Historical era",
        validators=[DataRequired(), Length(max=100)]
    )

    category = StringField(
        "Technology category",
        validators=[DataRequired(), Length(max=100)]
    )

    inventor = StringField(
        "Inventor or originating civilization",
        validators=[DataRequired(), Length(max=150)]
    )

    place_of_origin = StringField(
        "Place of origin",
        validators=[DataRequired(), Length(max=150)]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired(), Length(min=10, max=5000)]
    )

    significance = TextAreaField(
        "Historical significance",
        validators=[DataRequired(), Length(min=10, max=5000)]
    )

    source = TextAreaField(
        "Historical sources or references",
        validators=[DataRequired(), Length(min=5, max=3000)]
    )

    submit = SubmitField("Submit innovation")

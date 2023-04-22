from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class EditBookForm(FlaskForm):
    book_rating = FloatField('Rating', validators=[DataRequired()])
    submit = SubmitField('Change Rating')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

class AddBookForm(FlaskForm):
    book_title = StringField('Title', [DataRequired()])
    book_author = StringField('Author', [DataRequired()])
    book_rating = FloatField('Rating', validators=[DataRequired()])
    submit = SubmitField('Add Book')
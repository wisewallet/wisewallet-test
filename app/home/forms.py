from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Users


class SearchForm(FlaskForm):
    """
    Form for users to create new account
    """
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

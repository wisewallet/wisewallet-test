from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PropertyForm(FlaskForm):
    """
    Form for admin to add or edit a Property
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
#
# class CompanyForm(FlaskForm):
#     """
#     Form for admin to add or edit a Company Data
#     """
#     name = StringField('Name', validators=[DataRequired()])
#     category = StringField('Category',validators=[DataRequired()])
#     property = Property.query.filter_by(Property.id).all():
#     submit = SubmitField('Submit')

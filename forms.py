from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms_components import TimeField, StringField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length


class TripForm(FlaskForm):
    """Form for creating a trip"""

    # name = StringField('Trip name', validators=[DataRequired()])
    start_date = DateField('Start Date of Trip', validators=[DataRequired()])
    start_time = TimeField('Start time')
    end_date = DateField('End Date of Trip', validators=[DataRequired()])
    end_time = TimeField('End time')
    number_of_people = IntegerField('Number of people',validators=[DataRequired()] )
    


class UserAddForm(FlaskForm):
    """Form for adding users."""

    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

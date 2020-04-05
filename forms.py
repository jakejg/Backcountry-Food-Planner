from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms_components import TimeField, StringField, IntegerField, SelectField, DateTimeField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length



class TripForm(FlaskForm):
    """Form for creating a trip"""

    # name = StringField('Trip name', validators=[DataRequired()])
    start_date_time = DateTimeLocalField('Start Date and Time of Trip', format='%Y-%m-%dT%H:%M')
    end_date_time = DateTimeLocalField('End Date and Time of Trip', format='%Y-%m-%dT%H:%M')
    number_of_people = IntegerField('Number of people',validators=[DataRequired()] )

class SelectMealForm(FlaskForm):
    """Form for selecting meals from a list"""

class CreateMealForm(FlaskForm):

    first_i = HiddenField()
    second_i = HiddenField()
    third_i = HiddenField()
    fourth_i = HiddenField()
    

# add dynamic fields
    

    # breakfast = SelectField("Breakfast")
    # lunch = SelectField("Lunch")
    # dinner = SelectField("Dinner")
    
    

class UserAddForm(FlaskForm):
    """Form for adding users."""

    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

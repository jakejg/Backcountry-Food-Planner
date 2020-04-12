from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms_components import TimeField, IntegerField, SelectField, DateTimeField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, AnyOf, InputRequired, ValidationError



class TripForm(FlaskForm):
    """Form for creating a trip"""

    start_date_time = DateTimeLocalField('Start Date and Time of Trip', format='%Y-%m-%dT%H:%M')
    end_date_time = DateTimeLocalField('End Date and Time of Trip', format='%Y-%m-%dT%H:%M')
    number_of_people = IntegerField('Number of people', validators=[DataRequired()] )
    name = StringField('Give your trip a name')

def validate_dates(start, end):

    if end < start:
        return True

class SelectMealForm(FlaskForm):
    """Form for selecting meals from a list"""

def populate_select_meal_form(meal_data):
    """Add fields to the select meal form for each meal"""
    fields = {}

    for n in range(meal_data["Breakfast"]):
        fields[f"breakfast{n}"] = "Breakfast"
            
    for n in range(meal_data["Lunch"]):
        fields[f"lunch{n}"] = "Lunch"
       
    for n in range(meal_data["Dinner"]):
        fields[f"dinner{n}"] = "Dinner"

    for key, value in fields.items():
        if meal_data[value] > 0:
            setattr(SelectMealForm, key, SelectField(value, coerce=int))
    
    return fields

class CreateMealForm(FlaskForm):

    first_i = HiddenField()
    second_i = HiddenField()
    third_i = HiddenField()
    fourth_i = HiddenField()
    title = StringField('Name of Meal', validators=[DataRequired()])
    type_ = SelectField('Type of Meal', choices=[("Breakfast","Breakfast"), ("Lunch","Lunch"),("Dinner","Dinner")], validators=[DataRequired()])
    
class CreateUserAccount(FlaskForm):

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email(message="That email doesn't seem valid")])
    password = PasswordField("Password", validators=[InputRequired()])
    
class LoginUser(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
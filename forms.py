from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms_components import TimeField, StringField, IntegerField, SelectField, DateTimeField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, AnyOf, InputRequired



class TripForm(FlaskForm):
    """Form for creating a trip"""

    # name = StringField('Trip name', validators=[DataRequired()])
    start_date_time = DateTimeLocalField('Start Date and Time of Trip', format='%Y-%m-%dT%H:%M')
    end_date_time = DateTimeLocalField('End Date and Time of Trip', format='%Y-%m-%dT%H:%M')
    number_of_people = IntegerField('Number of people',validators=[DataRequired()] )

class SelectMealForm(FlaskForm):
    """Form for selecting meals from a list"""

def populate_select_meal_form(meal_data):
    """Add fields to the select meal form for each meal"""
    fields = {}

    for n in range(meal_data["breakfasts"]):
        fields[f"breakfast{n}"] = "breakfast"
            
    for n in range(meal_data["lunches"]):
        fields[f"lunch{n}"] = "lunch"
       
    for n in range(meal_data["dinners"]):
        fields[f"dinner{n}"] = "dinner"

    for key, value in fields.items():
        setattr(SelectMealForm, key, SelectField(value, coerce=int))
    
    return fields

class CreateMealForm(FlaskForm):

    first_i = HiddenField()
    second_i = HiddenField()
    third_i = HiddenField()
    fourth_i = HiddenField()
    title = StringField('Name of Meal', validators=[DataRequired()])
    type_ = StringField('Type of Meal', validators=[DataRequired(), AnyOf(["breakfast", "lunch", "dinner"], message="You Must pick breakfast, lunch, or dinner")])
    
class CreateUserAccount(FlaskForm):

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email(message="That email doesn't seem valid")])
    password = PasswordField("Password", validators=[InputRequired()])
    
class LoginUser(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
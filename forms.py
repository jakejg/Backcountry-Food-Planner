from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms_components import TimeField, IntegerField, SelectField, DateTimeField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, AnyOf, InputRequired, ValidationError
from models import Meal
from datetime import datetime, timedelta

d3= timedelta(days=3)

class TripForm(FlaskForm):
    """Form for creating a trip"""

    start_date_time = DateTimeLocalField('Start Date and Time of Trip', format='%Y-%m-%dT%H:%M', default=datetime.today, validators=[DataRequired(message="Enter a date mm/dd/yyy and time")])
    end_date_time = DateTimeLocalField('End Date and Time of Trip', format='%Y-%m-%dT%H:%M', default=datetime.today() + d3, validators=[DataRequired(message="Enter a date mm/dd/yyy and time")])
    number_of_people = IntegerField('Number of people', validators=[InputRequired()])
    name = StringField('Give your trip a name', validators=[DataRequired()])

def validate_dates(start, end, form):

    if end < start:
        form.end_date_time.errors = ["End date/time is earlier than start date/time."]
        return True

    if end.day == start.day:
        form.end_date_time.errors = ["Trip must be at least one night"]
        return True
    
    if start < datetime.today():
        form.start_date_time.errors = ["Trip must start after the current date and time"]
        return True

    if (end.date() - start.date()) > timedelta(days=365):
        form.end_date_time.errors = ["Trip can't be longer than 365 days"]
        return True

def validate_number_of_people(num):
    if num < 1:
        return True

    

    

class SelectMealForm(FlaskForm):
    """Form for selecting meals from a list"""

def populate_select_meal_form(meal_data):
    """Delete old fields and add new fields to the select meal form for each meal"""
    for field in SelectMealForm()._fields:
        if field != 'csrf_token':
            delattr(SelectMealForm, field)
    
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

def populate_choices(form, fields, trip):
    for key, value in fields.items():
        form[key].choices = [(m.id, m.title) for m in [*Meal.query.filter(Meal.type_==value, Meal.public==True), *Meal.query.filter(Meal.type_==value, Meal.user_id==trip.user_id)]]

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
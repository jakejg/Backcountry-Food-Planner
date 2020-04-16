import os
from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
from models import db, connect_db, Trip, Meal, User, TripMeal, Ingredient
from forms import TripForm, SelectMealForm, SelectField, CreateMealForm, CreateUserAccount, LoginUser, validate_dates, populate_select_meal_form, validate_length, validate_number_of_people
from api_requests import search_for_a_food, get_nutrition_data, get_data_from_api_results
from unit_conversions import to_lbs
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///food_planner'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

@app.before_request
def add_user_to_g():
    """If user is logged in, add current user to Flask global."""

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


# Trip routes ///////////////////////////////////

@app.route('/', methods=["GET", "POST"])
def home():
    """Show form for creating a trip"""

    form = TripForm()

    if form.validate_on_submit():
        if validate_dates(form.start_date_time.data, form.end_date_time.data):

            form.end_date_time.errors = ["End date/time is earlier than start date/time."]
        
            return render_template('create_trip.html', form=form)

        if validate_length(form.start_date_time.data, form.end_date_time.data):

            form.end_date_time.errors = ["Trip must be at least one night"]
        
            return render_template('create_trip.html', form=form)

        if validate_number_of_people(form.number_of_people.data):

            form.number_of_people.errors = ["Please enter at least 1 person"]

            return render_template('create_trip.html', form=form)

        # check if user is logged in if not log them in as a guest user

        if 'user_id' not in session:
            User.log_in_as_guest()

  
        trip = Trip(start_date_time=form.start_date_time.data,
                    end_date_time=form.end_date_time.data,
                    number_of_people=form.number_of_people.data,
                    name=form.name.data,
                    user_id=session.get('user_id')
                    )
        db.session.add(trip)
        db.session.commit()

        session['trip_id'] = trip.id

        return redirect(url_for('select_meals', trip_id=trip.id))
       
    return render_template('create_trip.html', form=form)

@app.route('/select-meals/<int:trip_id>', methods=["GET", "POST"])
def select_meals(trip_id):
    """Select meals for a trip"""

    trip = Trip.query.get_or_404(trip_id)

    if not authorize(trip.user_id):
        raise Unauthorized()
    
    meal_data = trip.get_meal_numbers()

    fields = populate_select_meal_form(meal_data)

    form = SelectMealForm()

    for key, value in fields.items():
        form[key].choices = [(m.id, m.title) for m in [*Meal.query.filter(Meal.type_==value, Meal.public==True), *Meal.query.filter(Meal.type_==value, Meal.user_id==trip.user_id)]]
    
    if form.validate_on_submit():
        for key, value in form.data.items():
            if key != 'csrf_token':
                r = TripMeal(trip_id=trip.id, meal_id=form[key].data)
                db.session.add(r)
                db.session.commit()

        return redirect(url_for('show_meal_plan', trip_id=trip.id))
   
    return render_template('select_meals.html', meal_data=meal_data, form=form)

@app.route('/meal-plan/<int:trip_id>')
def show_meal_plan(trip_id):
    """Show meal numbers and nutrition info, organized by meal type"""

    trip = Trip.query.get_or_404(trip_id)

    if not authorize(trip.user_id):
        raise Unauthorized()

    meal_numbers = trip.get_meal_numbers()
    meals = trip.trip_meal
    nutrition_data = [meal.meals.get_total_nutrition_data() for meal in meals]
   
    return render_template('meal_plan.html', trip=trip, meals=meals, meal_numbers=meal_numbers, nutrition_data=nutrition_data)

@app.route('/packing-list/<int:trip_id>')
def show_packing_list(trip_id):
    """Show a printable packing list with ingredients and wieghts"""

    trip = Trip.query.get_or_404(trip_id)

    if not authorize(trip.user_id):
        raise Unauthorized()

    weights = trip.get_total_ingredient_weights()
    weights = {key: to_lbs(val) for key, val in weights.items()}

    return render_template('packing_list.html', weights=weights, trip=trip)

@app.route('/meal', methods=["GET", "POST"])
def show_create_meal_page():
    """Show create a meal form and handle data"""
    form = CreateMealForm()
  
    if form.validate_on_submit():  
        
        meal = Meal(title=form.title.data, type_=form.type_.data, user_id=session.get('user_id'))

        for key, value in form.data.items():
            
            if key != 'csrf_token' and key != 'title' and key !='type_' and value:
                ingr = Ingredient.create_ingredient(get_nutrition_data(value))
                meal.ingredients.append(ingr)
                db.session.commit()

        return redirect(url_for('show_create_meal_page', form=form))

    return render_template('create_meal.html', form=form)

@app.route('/meal/api', methods=["POST"])
def api():
    """Get search term from, and return data"""

    params = request.json['params']

    search_result = search_for_a_food(params.get('item'), params.get('brandOwner'))

    if len(search_result.content) > 300000:
        error_response = jsonify(error="Response is too large to display")
        return (error_response, 500)

    
    return jsonify(get_data_from_api_results(search_result.json()))

# User Routes///////////////////////////////

@app.route('/register', methods=["GET", "POST"])
def register():
    """ Allow a new user to register"""

    form = CreateUserAccount()

    if form.validate_on_submit():
        try:
            f = form
            user = User.register(f.username.data, 
                                f.password.data,
                                f.email.data,
                                f.first_name.data,
                                f.last_name.data,
                                False)
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/users/register.html', form=form)

        session.clear()
        session['user_id'] = user.id
        session['guest'] = False
        return redirect(url_for('user_info', username=user.username))

    return render_template('/users/register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Authenticate a user"""

    form = LoginUser()
    
    if form.validate_on_submit():
        f = form
        user = User.login(f.username.data, f.password.data)
        
        if user:
            session.clear()
            session['user_id'] = user.id
            session['guest'] = False
            return redirect(url_for('user_info', username=user.username))

        elif user is None:
            form.username.errors = ["Username Not Found"]
        else:
            form.password.errors = ["Incorrect Password"]
    
    return render_template('/users/login.html', form=form)


@app.route('/users/<username>')
def user_info(username):
    """Show info about a user"""

    user = User.get_by_username(username)

    if not authorize(user.id):
        raise Unauthorized()

    return render_template('/users/user_info.html', user=user)

    
@app.route('/logout')
def logout():
    """Log a user out"""
    session.clear()

    flash("You are now logged out")
    return redirect(url_for('home'))

def authorize(user_id):
    """ Check if a user has permission to access a page"""

    return user_id == session.get('user_id')
         

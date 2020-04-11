import os
from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from models import db, connect_db, Trip, Meal, User, TripMeal, Ingredient
from forms import TripForm, SelectMealForm, SelectField, CreateMealForm, CreateUserAccount, LoginUser, validate_dates, populate_select_meal_form
from api_requests import search_for_a_food, get_nutrition_data
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
    meal_data = trip.get_meal_numbers()

    fields = populate_select_meal_form(meal_data)
    
    form = SelectMealForm()
    
    for key, value in fields.items():
        form[key].choices = [(m.id, m.title) for m in Meal.query.filter_by(type_=value)]

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
    meal_numbers = trip.get_meal_numbers()
    meals = trip.trip_meal
    nutrition_data = [meal.meals.get_total_nutrition_data() for meal in meals]
   
    return render_template('meal_plan.html', meals=meals, meal_numbers=meal_numbers, nutrition_data=nutrition_data)

@app.route('/packing-list/<int:trip_id>')
def show_packing_list(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    weights = trip.get_total_ingredient_weights()
    weights = {key: to_lbs(val) for key, val in weights.items()}

    return render_template('packing_list.html', weights=weights, trip=trip)

@app.route('/meal', methods=["GET", "POST"])
def show_create_meal_page():
    """Show create a meal form and handle data"""
    form = CreateMealForm()
  
    if form.validate_on_submit():  
        
        meal = Meal(title=form.title.data, type_=form.type_.data)

        for key, value in form.data.items():
            
            if key != 'csrf_token' and key != 'title' and key !='type_' and value:
                ingr = create_ingredient(get_nutrition_data(value))
                meal.ingredients.append(ingr)
                db.session.commit()

        return redirect(url_for('show_create_meal_page', form=form))

    return render_template('create_meal.html', form=form)

@app.route('/meal/api', methods=["POST"])
def api():
    """Get search term from, and return data"""

    params = request.json['params']
   
    return search_for_a_food(params.get('item'), params.get('brandOwner'))

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
                                f.last_name.data)
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/users/register.html', form=form)

        session['user_id'] = user.id
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
            session['user_id'] = user.id
            return redirect(url_for('user_info', username=user.username))

        elif user is None:
            form.username.errors = ["Username Not Found"]
        else:
            form.password.errors = ["Incorrect Password"]
    
    return render_template('/users/login.html', form=form)


@app.route('/users/<username>')
def user_info(username):
    """Show info about a user"""

    user = User.query.filter_by(username=username).first()

    if not authorize(user.id):
        raise Unauthorized()

    return render_template('/users/user_info.html', user=user)

    
@app.route('/logout')
def logout():
    """Log a user out"""
    session.pop('user_id')
    flash("You are now logged out")
    return redirect(url_for('home'))


def create_ingredient(food):
    """Check if ingredient exists and if not 
     create a new ingredient from a food"""

    ingredient = Ingredient.query.filter_by(fdcId=food['fdcId']).first()

    if ingredient is None:
        if food['foodClass'] == "Branded":
            n = food['labelNutrients']
            ingredient = Ingredient(name=food['description'],
                                     fdcId=food['fdcId'],
                                     brand=food['brandOwner'],
                                     ingredient_list=food.get('ingredients', "No Ingredients Listed"),
                                     serving_size=food.get('servingSize', 0),
                                     serving_size_unit=food.get('servingSizeUnit'),
                                     fat=n.get('fat', 0).get('value', 0),
                                     saturated_fat=n.get('saturatedFat', {}).get('value',0),
                                     trans_fat=n.get('transFat', {}).get('value',0),
                                     cholesterol=n.get('cholesterol', {}).get('value',0),
                                     sodium=n.get('sodium', {}).get('value',0),
                                     carbohydrates=n.get('carbohydrates', {}).get('value',0),
                                     fiber=n.get('fiber', {}).get('value',0),
                                     sugars=n.get('sugars', {}).get('value',0),
                                     protein=n.get('protein', {}).get('value',0),
                                     calcium=n.get('calcium', {}).get('value',0),
                                     iron=n.get('iron', {}).get('value',0),
                                     calories=n.get('calories', {}).get('value',0))
            db.session.add(ingredient)
            db.session.commit()

    return ingredient

def authorize(user_id):
    """ Check if a user has permission to access a page"""

    return user_id == session.get('user_id')
         
    

import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from models import db, connect_db, Trip, Meal, User, TripMeal, Ingredient
from datetime import date, time
from forms import TripForm, SelectMealForm, SelectField, CreateMealForm
from api_key import fdc_key

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///food_planner'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

@app.route('/', methods=["GET", "POST"])
def home():

    form = TripForm()

    if form.validate_on_submit():
        trip = Trip(start_date_time=form.start_date_time.data,
                    end_date_time=form.end_date_time.data,
                    number_of_people=form.number_of_people.data)
        db.session.add(trip)
        db.session.commit()

        return redirect(url_for('select_meals', trip_id=trip.id))

    return render_template('create_trip.html', form=form)

@app.route('/select-meals/<int:trip_id>', methods=["GET", "POST"])
def select_meals(trip_id):

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
        return redirect(url_for('show_meal_plan'))

    return render_template('select_meals.html', meal_data=meal_data, form=form)

@app.route('/meal-plan/<int:trip_id>')
def show_meal_plan(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    # for meal in trip.meals:
    #     meal.get_ingredient_weights()
    #     meal.get_nutrition_info()


@app.route('/meal', methods=["GET", "POST"])
def create_a_meal():
    form = CreateMealForm()

    if form.validate_on_submit():
        for key, value in form.data.items():
            if key != 'csrf_token' or not value:
                get_nutrition_info(value)


    return render_template('create_meal.html', form=form)



@app.route('/meal/api', methods=["POST"])
def api():
    """Get search term from create meal form, and return data"""

    params = request.json['params']

    return search_for_a_food(params)
    

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

def search_for_a_food(params):
    """Make  make search request to fdc api"""

    base_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={fdc_key}"

    resp = requests.get(base_url, params).json()

    return resp

def get_nutrition_info(fdc_id):
    base_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={fdc_key}"

    resp = requests.get(base_url).json()
    
    if resp['foodClass'] == "Branded":
        n = resp['labelNutrients']
        ingredient = Ingredient(name=resp['description'],
                                 fdcId=resp['fdcId'],
                                 brand=resp['brandOwner'],
                                 ingredient_list=resp['ingredients'],
                                 fat=n['fat']['value'])
        db.session.add(ingredient)
        db.session.commit()
        import pdb; pdb.set_trace()
             
        #                          saturated_fat=n.saturatedFat.value,
        #                          trans_fat=n.transFat.value,
        #                          cholesterol=n.cholesterol.value,
        #                          sodium=n.sodium.value,
        #                          carbohydrates=n.carbohydrates.value,
        #                          fiber=n.fiber.value,
        #                          sugars=n.sugars.value,
        #                          protein=n.protein.value,
        #                          calcium=n.calcium.value,
        #                          iron=n.iron.value,
        #                          calories=n.calories.value)
       
        # import pdb; pdb.set_trace()
    

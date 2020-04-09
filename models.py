import requests
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    username = db.Column(db.Text, 
                        unique=True,
                        nullable=False)
    email = db.Column(db.Text,
                    unique=True,
                    nullable=False)
    password = db.Column(db.Text, 
                        nullable=False)
    trips = db.relationship('Trip', backref='user')

class Trip(db.Model):

    __tablename__ = "trips"

    id = db.Column(db.Integer,
                    primary_key=True)

    name = db.Column(db.Text)

    start_date_time = db.Column(db.DateTime,
                                nullable=False)
    end_date_time = db.Column(db.DateTime,
                                nullable=False)
    number_of_people = db.Column(db.Integer,
                                nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    meals = db.relationship('Meal', secondary='trip_meal', backref='trips')

    trip_meal = db.relationship('TripMeal', backref='trips')

    def get_bc_days(self):
        return (self.end_date_time - self.start_date_time).days - 1
    
    def get_date_range(self):

        one_day = timedelta(days=1)
        dates = []
        while self.start_date_time <= self.end_date_time:
            dates.append(self.start_date_time)
            self.start_date_time += one_day
        
        return dates

    def get_meal_numbers(self):
        """Get numbers for each type of meal"""

        bc_meals = self.get_bc_days()

        breakfasts = bc_meals 
        lunches = bc_meals 
        dinners = bc_meals 

        # add start day meals
        if self.start_date_time.hour < 13:
            lunches += 1
            dinners += 1

        elif self.start_date_time.hour < 19:
            dinners += 1

        # add end day meals
        if self.end_date_time.hour < 12:
            breakfasts += 1

        elif self.end_date_time.hour < 18:
            breakfasts += 1
            lunches += 1
        
        else:
            breakfasts += 1
            lunches += 1
            dinners += 1

        return {
            "total_meals": breakfasts + lunches + dinners,
            "breakfasts" : breakfasts,
            "lunches" : lunches,
            "dinners" : dinners,
        }

class Meal(db.Model):
    
    __tablename__ = "meals"

    id = db.Column(db.Integer,
                    primary_key=True)
    title = db.Column(db.Text,
                        nullable=False)
    type_ = db.Column(db.Text,
                        nullable=False)
    
    ingredients = db.relationship('Ingredient', secondary='meal_ingredient', order_by='MealIngredient.id', backref='meals')

    trip_meal = db.relationship('TripMeal', backref='meals')

    weight = db.Column(db.Float,
                        default=317.515)

    def get_ingredient_weights(self):
        ing = self.ingredients
     
        weights = {}
        
        if len(ing) == 4:
            p,s,a1,a2 = ing
            weights[p.name] = self.weight*.75
            weights[s.name] = self.weight*.083
            weights[a1.name] = self.weight*.083
            weights[a2.name] = self.weight*.083

        elif len(ing) == 3:
            p,s,a1 = ing
            weights[p.name] = self.weight*.75
            weights[s.name] = self.weight*.125
            weights[a1.name] = self.weight*.125

        elif len(ing) == 2:
            p,s = ing
            weights[p.name] = self.weight*.75
            weights[s.name] = self.weight*.25
        else:
            weights[ing[0].name] = self.weight
        
        rounded = {key: round(val, 2) for key, val in weights.items()}
        
        return rounded

    def get_total_nutrition_data(self):
        """Get the total nutrition data for a meal"""

        total = {}

        for key, value in self.get_ingredient_weights().items():

            ing = Ingredient.query.filter_by(name=key).first()

            for nutrient in ing.get_nutrient_names():

                amount = getattr(ing, nutrient) / ing.serving_size * value
                total[nutrient] = total.get(nutrient, 0) + round(amount, 2)

        return total

class Ingredient(db.Model):

    __tablename__ = "ingredients"

    id = db.Column(db.Integer,
                    primary_key=True)
    
    name = db.Column(db.Text)

    fdcId = db.Column(db.Integer)

    brand = db.Column(db.Text)

    ingredient_list = db.Column(db.Text)

    serving_size = db.Column(db.Float)

    serving_size_unit = db.Column(db.Text)

    fat = db.Column(db.Float)

    saturated_fat = db.Column(db.Float)

    trans_fat = db.Column(db.Float)

    cholesterol = db.Column(db.Float)

    sodium = db.Column(db.Float)

    carbohydrates = db.Column(db.Float)

    fiber = db.Column(db.Float)

    sugars = db.Column(db.Float)

    protein = db.Column(db.Float)

    calcium = db.Column(db.Float)

    iron = db.Column(db.Float)

    calories = db.Column(db.Float)

    def get_nutrient_names(self):
        """Get a list of nutrient names"""

        return ["fat", 
                "saturated_fat", 
                "trans_fat", 
                "cholesterol", 
                "sodium", 
                "carbohydrates",
                "fiber",
                "sugars",
                "protein",
                "calcium",
                "iron",
                "calories"]


class MealIngredient(db.Model):

    __tablename__ = "meal_ingredient"
    
    id = db.Column(db.Integer, primary_key=True)

    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))

    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))


class TripMeal(db.Model):

    __tablename__ = "trip_meal"

    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))

    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


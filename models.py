import requests
from api_key import fdc_key
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

    meals = db.relationship('Meal', secondary='trip_meal', backref='user')

    def get_bc_days(self):
        return (self.end_date_time - self.start_date_time).days - 1

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
    title = db.Column(db.Text)

    type_ = db.Column(db.Text)

    primary_ingredient = db.Column(db.Text,
                                    nullable=False)
    secondary_ingredient = db.Column(db.Text)

    additional_ingredient1 = db.Column(db.Text)

    additional_ingredient2 = db.Column(db.Text)

    weight = db.Column(db.Float,
                        default=2.1)

    def get_ingredient_weights(self):
        p = self.primary_ingredient
        s = self.secondary_ingredient 
        a1 = self.additional_ingredient1 
        a2 = self.additional_ingredient2

        ingredients = [p, s, a1, a2]

        weights = {}
        
        if ingredients[3]:
            weights[p] = self.weight*.375
            weights[s] = self.weight*.375
            weights[a1] = self.weight*.125
            weights[a2] = self.weight*.125

        elif ingredients[2]:
            weights[p] = self.weight*.375
            weights[s] = self.weight*.375
            weights[a1] = self.weight*.25

        elif ingredients[1]:
            weights[p] = self.weight*.5
            weights[s] = self.weight*.5
        else:
            weights[p] = self.weight
        
        rounded = {key: round(val, 2) for key, val in weights.items()}
        
        return rounded

    def get_nutrition_info(self):
        get_fdcID()

        

    def get_fdcID():
        foods = self.get_ingredient_weights()

        food_ids = []
        for food, weight in foods.items():
            resp = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search", 
                                params={"api_key": fdc_key, "query": food }).json()
            
            import pdb; pdb.set_trace()
            food_ids.append()
        


class TripMeal(db.Model):

    __tablename__ = "trip_meal"
    
    id = db.Column(db.Integer,
                    primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))

    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))



def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


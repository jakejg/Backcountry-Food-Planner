import requests
from datetime import datetime, timedelta
from flask import session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from .utils import to_lbs, get_random_word

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
    guest = db.Column(db.Boolean,
                        nullable=False)
    trips = db.relationship('Trip', backref='user')

    meals = db.relationship('Meal', backref='user')

    @classmethod
    def register(cls, username, password, email, first_name, last_name, guest):
        """Generate a hash for a password and create a new user or update a guest user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

       
        if 'user_id' in session:
            user = User.query.get(session.get('user_id'))

            user.username=username, 
            user.password=hashed_utf8, 
            user.email=email, 
            user.first_name=first_name, 
            user.last_name=last_name, 
            user.guest=guest

            return user

        else:
            return cls(username=username,
                    password=hashed_utf8,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    guest=guest)

    
    @classmethod
    def login(cls, username, password):
        """Check if a user exists and if the password matches the username"""

        user = User.query.filter_by(username=username).first()

        if not user:
            return None
        elif bcrypt.check_password_hash(user.password, password):
            return user
        else: 
            return False
    
    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def log_in_as_guest(cls):
        """Create a new guest user and log them in"""

        word = get_random_word(4) + get_random_word(4)
        guestuser = cls.register(word, "123", word, word, word, True)

        db.session.add(guestuser)
        db.session.commit()

        session['user_id'] = guestuser.id
        session['guest'] = True

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
        """Gets number of full trip days or bc days"""

        bc_days = (self.end_date_time.date() - self.start_date_time.date()).days -1
        
        return bc_days if bc_days > -1 else 0
            
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
            "Breakfast" : breakfasts,
            "Lunch" : lunches,
            "Dinner" : dinners,
        }
    
    def get_total_ingredient_weights(self):
        """ Get the total amount of each ingredient to pack for a trip"""

        meals = self.trip_meal
        total = {}
        for meal in meals:
            for key, val in meal.meals.get_ingredient_weights().items():
                total[key] = total.get(key, 0) + round(val, 2)

        return {key: val*self.number_of_people for key, val in total.items()}
    
    def get_total_food_weight(self):
        """Get the total food weight for the trip in lbs"""
        total = 0
        for val in self.get_total_ingredient_weights().values():
            total += val
        return to_lbs(total)

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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    public = db.Column(db.Boolean,
                        default=False)

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
                total[nutrient] = round(total.get(nutrient, 0) + amount, 2)
            
        return total
    
    def check_for_dietary_restrictions(self, diet):
        not_vegetarian = {"PORK", "BEEF", "SAUSAGE", "CHICKEN", "BACON", "LARD", "HAM", "TURKEY", "FISH"}
        not_vegan = {*not_vegetarian, "MILK", "CHEESE", "EGGS", "WHEY", "BUTTER", "CREAM", "GELATIN"}
        not_gluten_free = {"WHEAT", "GLUTEN"}
        contains = set()

        for ingredient in self.ingredients:

            if diet == 'vegan' or diet == 'all':
                for word in not_vegan:
                    if word in ingredient.ingredient_list:
                        contains.add(word)

            if diet == 'vegetarian' or diet == 'all':
                for word in not_vegetarian:
                    if word in ingredient.ingredient_list:
                        contains.add(word)

            if diet == 'gluten free' or diet == 'all':
                for word in not_gluten_free:
                    if word in ingredient.ingredient_list:
                        contains.add(word)

        return contains

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

    @classmethod
    def create_ingredient(cls, food):
        """Check if ingredient exists and if not 
         create a new ingredient from a food"""

        ingredient = Ingredient.query.filter_by(fdcId=food.get('fdcId')).first()

        if ingredient is None:
            if food.get('foodClass') == "Branded":
                n = food.get('labelNutrients')
                ingredient = Ingredient(name=food.get('description'),
                                         fdcId=food.get('fdcId'),
                                         brand=food.get('brandOwner'),
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

    @classmethod
    def delete_old_trip_meals(self, trip):
        """Clear meal associations for a trip"""

        for trip_meal in trip.trip_meal:
            db.session.delete(trip_meal)
        db.session.commit()

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


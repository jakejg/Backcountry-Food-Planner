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
    username = db.Column(db.Text)
    email = db.Column(db.Text,
                    nullable=False)
    password = db.Column(db.Text, 
                        nullable=False)
    trips = db.relationship('Trip', backref='user')

class Trip(db.Model):

    __tablename__ = "trips"

    id = db.Column(db.Integer,
                    primary_key=True)

    name = db.Column(db.Text)

    start_date = db.Column(db.Date,
                                nullable=False)
    start_time = db.Column(db.Time,
                                nullable=False)
    end_date = db.Column(db.Date,
                                nullable=False)
    end_time = db.Column(db.Time,
                                nullable=False)
    number_of_people = db.Column(db.Integer,
                                nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    meals = db.relationship('Meal', secondary='trip_meal', backref='user')

    def get_bc_days(self):
        return (self.end_date - self.start_date).days - 1

    def get_meal_numbers(self):
        """Get numbers for each type of meal"""

        bc_meals = self.get_bc_days()

        breakfasts = bc_meals 
        lunches = bc_meals 
        dinners = bc_meals 

        # add start day meals
        if self.start_time.hour < 13:
            lunches += 1
            dinners += 1

        elif self.start_time.hour < 19:
            dinners += 1

        # add end day meals
        if self.end_time.hour < 12:
            breakfasts += 1

        elif self.end_time.hour < 18:
            breakfasts += 1
            lunches += 1
        
        else:
            breakfasts += 1
            lunches += 1
            dinners += 1

        return = {
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

    additional_ingredint1 = db.Column(db.Text)

    additional_ingredint2 = db.Column(db.Text)

    weight = db.Column(db.Text)

    calories = db.Column(db.Integer)

    fiber = db.Column(db.Integer)

    protein = db.Column(db.Integer)

    sugar = db.Column(db.Integer)

    fat = db.Column(db.Integer)


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


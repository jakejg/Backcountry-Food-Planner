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

    # @classmethod
    # def get_start_day_meals(start_time):
    #     """Get number of meals for the first day"""

    #     start_day_meals = 3

    #     if start_time.hour > 7:
    #         meals -= 1
    #     elif start_time.hour > 13:
    #         meals -= 2
    #     elif star_time.hour > 18:
    #         meals -= 3
        
    #     return start_day_meals
    # @classmethod
    # def get_end_day_meals(end_time):
    #     """Get number of meals for the last day"""

    #     end_day_meals = 3

    #     if end_time.hour < 18:
    #         meals -= 1
    #     if end_time.hour < 12:
    #         meals -=2

    #     return end_day_meals

    # @classmethod
    # def get_meal_info():
    #     bc_meals = Trip.get_bc_days()*3

    #     meal_info = {
    #         "total_meals": Trip.get_start_meals() + Trip.get_end_day_meals(),
    #         "breakfasts" : bc_meals


    #     }


   


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


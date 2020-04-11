import os
from unittest import TestCase
from models import db, connect_db, User, Trip, Meal, Ingredient, TripMeal
from datetime import datetime
os.environ['DATABASE_URL'] = "postgresql:///food_planner_test"
from app import app, create_ingredient, get_nutrition_data

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


# seed the test database with some meals

# breakfast
b1 = Meal(title="Oatmeal", 
        type_="breakfast"
        )

oats = create_ingredient(get_nutrition_data(368739))
b1.ingredients.append(oats)

raisins = create_ingredient(get_nutrition_data(408107))
b1.ingredients.append(raisins)

sugar = create_ingredient(get_nutrition_data(519364))
b1.ingredients.append(sugar)


# lunch
l1 = Meal(title="Pita and Hummus", 
        type_="lunch"
        )

pita = create_ingredient(get_nutrition_data(384233))
l1.ingredients.append(pita)

hummus = create_ingredient(get_nutrition_data(475281))
l1.ingredients.append(hummus)


# dinner
d1 = Meal(title="Rice and Beans", 
        type_="dinner"
        )

rice = create_ingredient(get_nutrition_data(447921))
d1.ingredients.append(rice)

beans = create_ingredient(get_nutrition_data(381573))
d1.ingredients.append(beans)

db.session.commit()


class TripTests(TestCase):

    def setUp(self):
        """Set up a User and a new Trip"""

        self.user = User.register("tester1",
                                "password",
                                "test@t.com",
                                "john",
                                "smith")
        db.session.add(self.user)
        db.session.commit()
        
        self.trip = Trip(start_date_time=datetime(2020, 4, 8, 10, 00), 
                        end_date_time=datetime(2020, 4, 10, 15, 00),
                        number_of_people=3,
                        name="TestTrip",
                        user_id= self.user.id)
        
        db.session.add(self.trip)
        db.session.commit()

    def tearDown(self):
        TripMeal.query.delete()
        Trip.query.delete()
        User.query.delete()
        

        db.session.commit()

    def test_get_bc_days(self):
        """Check if correct number of days are returned"""

        self.assertEqual(self.trip.get_bc_days(), 1)

    def get_meal_numbers(self):
        """Check if correct number of meals are returned"""

        nums = trip.get_meal_numbers()

        self.assertEqual(nums['total_meals'], 7)
        self.assertEqual(nums['breakfasts'], 2)
        self.assertEqual(nums['lunches'], 3)
        self.assertEqual(nums['dinners'], 2)

        
    


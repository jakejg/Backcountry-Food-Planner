import os
from app import app
from unittest import TestCase
from app.models import db, connect_db, User, Trip, Meal, Ingredient, TripMeal
from datetime import datetime
os.environ['DATABASE_URL'] = "postgresql:///food_planner_test"
from app.api_requests import get_nutrition_data

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


# seed the test database with some meals

# breakfast
b1 = Meal(title="Oatmeal", 
        type_="breakfast"
        )

oats = Ingredient.create_ingredient(get_nutrition_data(368739))
b1.ingredients.append(oats)

raisins = Ingredient.create_ingredient(get_nutrition_data(408107))
b1.ingredients.append(raisins)

sugar = Ingredient.create_ingredient(get_nutrition_data(519364))
b1.ingredients.append(sugar)


# lunch
l1 = Meal(title="Pita and Hummus", 
        type_="lunch"
        )

pita = Ingredient.create_ingredient(get_nutrition_data(384233))
l1.ingredients.append(pita)

hummus = Ingredient.create_ingredient(get_nutrition_data(475281))
l1.ingredients.append(hummus)


# dinner
d1 = Meal(title="Rice and Beans", 
        type_="dinner"
        )

rice = Ingredient.create_ingredient(get_nutrition_data(447921))
d1.ingredients.append(rice)

beans = Ingredient.create_ingredient(get_nutrition_data(381573))
d1.ingredients.append(beans)

db.session.commit()


class TripMealTests(TestCase):

    def setUp(self):
        """Set up a User and a new Trip"""
                
        self.user = User(username="tester1",
                        password="password",
                        email="test@t.com",
                        first_name="john",
                        last_name="smith",
                        guest=False)
        db.session.add(self.user)
        db.session.commit()
        self.trip = Trip(start_date_time=datetime(2020, 4, 8, 10, 00), 
                        end_date_time=datetime(2020, 4, 10, 15, 00),
                        number_of_people=3,
                        name="TestTrip",
                        user_id= self.user.id)
        db.session.add(self.trip)
        db.session.commit()
        tm1 = TripMeal(trip_id=self.trip.id, meal_id=1)
        tm2 = TripMeal(trip_id=self.trip.id, meal_id=1)
        tm3 = TripMeal(trip_id=self.trip.id, meal_id=2)
        tm4 = TripMeal(trip_id=self.trip.id, meal_id=2)
        tm5 = TripMeal(trip_id=self.trip.id, meal_id=2)
        tm6 = TripMeal(trip_id=self.trip.id, meal_id=3)
        tm7 = TripMeal(trip_id=self.trip.id, meal_id=3)
        db.session.add_all([tm1, tm2, tm3, tm4, tm5, tm6, tm7])
        db.session.commit()


    def tearDown(self):
        TripMeal.query.delete()
        Trip.query.delete()
        User.query.delete()
        

        db.session.commit()

    def test_get_bc_days(self):
        """Check if correct number of days are returned"""

        self.assertEqual(self.trip.get_bc_days(), 1)

    def test_get_meal_numbers(self):
        """Check if correct number of meals are returned"""
        
        nums = self.trip.get_meal_numbers()

        self.assertEqual(nums['total_meals'], 7)
        self.assertEqual(nums['Breakfast'], 2)
        self.assertEqual(nums['Lunch'], 3)
        self.assertEqual(nums['Dinner'], 2)

        short_trip = Trip(start_date_time=datetime(2020, 4, 10, 10, 00), 
                        end_date_time=datetime(2020, 4, 11, 9, 00),
                        number_of_people=3,
                        name="short",
                        user_id= self.user.id)
        
        db.session.add(short_trip)
        db.session.commit()

        nums = short_trip.get_meal_numbers()

        self.assertEqual(nums['total_meals'], 3)

    def test_get_total_ingredient_weights(self):
        """Check if ingredients weghts are totaled correctly"""

        weights = self.trip.get_total_ingredient_weights()

        self.assertEqual(weights['OATS'], 1428.84)
        self.assertEqual(weights['PINTO BEANS'], 476.28)
        self.assertEqual(weights['BROWN SUGAR'], 238.14)

    def test_get_total_food_weight(self):
        """Check it total food weight in lbs is given correctly"""

        total = self.trip.get_total_food_weight()

        self.assertEqual(total, 14.67)

    def test_get_ingredient_weights(self):
        """Check if the meal weight is distributed to ingredients in the correct proportions"""

        meal = Meal.query.get(1)

        w = meal.get_ingredient_weights()

        self.assertEqual(w['OATS'], 238.14)
        self.assertEqual(w['RAISINS'], 39.69)
        self.assertEqual(w['BROWN SUGAR'], 39.69)
    
    def test_get_total_nutrition_data(self):
        """Check if the nutrition data per meal is correct"""

        meal = Meal.query.get(1)
        
        n = meal.get_total_nutrition_data()
        
        self.assertEqual(n['fiber'], 25.79)
        self.assertEqual(n['fat'], 14.88)
        self.assertEqual(n['calories'], 1144.26)
        self.assertEqual(n['sodium'], 0)




        

    



    


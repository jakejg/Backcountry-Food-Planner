import os
from unittest import TestCase
from models import db, connect_db, User, Trip, Meal, Ingredient, TripMeal
from datetime import datetime
from flask import json
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


class ViewTests(TestCase):

    def setUp(self):
        """Set up a User and a new Trip and base meals"""

        self.user = User.register("tester1",
                                "password",
                                "test@t.com",
                                "john",
                                "smith")
        db.session.add(self.user)
        db.session.commit()
        
        self.trip = Trip(start_date_time=datetime(2020, 4, 8, 10, 00), 
                        end_date_time=datetime(2020, 4, 9, 15, 00),
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
    
    def test_home(self):
        """Test create trip form  """

        with app.test_client() as client:
            data = {'start_date_time': datetime(2020, 4, 8, 10, 0).strftime('%Y-%m-%dT%H:%M'),
                    'end_date_time': datetime(2020, 4, 9, 15, 0).strftime('%Y-%m-%dT%H:%M'),
                    "number_of_people": 2,
                    "name": "TestTrip2"
                    }
            resp = client.post('/', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            trip = Trip.query.filter_by(name="TestTrip2").first()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(trip.number_of_people, 2)
            self.assertIn("You will need 4 meals.", html)


    # def test_select_meals(self):
    #     """Test select meal form"""

    #     with app.test_client() as client:
    #         data = {'start_date_time': datetime(2020, 4, 8, 10, 0).strftime('%Y-%m-%dT%H:%M'),
    #                 'end_date_time': datetime(2020, 4, 9, 15, 0).strftime('%Y-%m-%dT%H:%M'),
    #                 "number_of_people": 2,
    #                 "name": "TestTrip2"
    #                 }
    #         resp = client.post('/', data=data, follow_redirects=True)
    #         trip = Trip.query.filter_by(name="TestTrip2").first()
    #         meals = {"breakfast0": 1,
    #                 "lunch0": 3,
    #                 "lunch1": 3,
    #                 "dinner0": 5
    #         }
    #         resp = client.post(f'/select-meals/{trip.id}', data=meals, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Rice and Beans", html)

    def test_show_meals(self):
        """Test show meal plan"""

        a = TripMeal(trip_id=self.trip.id, meal_id=1)
        b = TripMeal(trip_id=self.trip.id, meal_id=2)
        db.session.add_all([a,b])
        db.session.commit()

        with app.test_client() as client:
            resp = client.get(f'/meal-plan/{self.trip.id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You have 4 meals", html)

    def test_packing_list(self):
        """Test show packing list"""

        with app.test_client() as client:
            resp = client.get(f'/packing-list/{self.trip.id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Packing List", html)
    
    def test_create_meal(self):
        """Test that a meal can be created from ingredient ids"""

        
        with app.test_client() as client:
            data = {
                'first_i': 792667,
                'second_i': 548596,
                'title': 'testmeal',
                'type_': 'dinner',
            }
            resp = client.post(f'/meal', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            meal = Meal.query.filter_by(title="testmeal").first()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(meal.type_, 'dinner')

    def test_meal_api(self):
        """Test the meal api"""

        with app.test_client() as client:
            j = { "params": 
                {
                "item": "rice",
                "brandOwner": "Lotus"
                }
            }
            resp = client.post('/meal/api', json=j)
            r = resp.json
            self.assertEqual(resp.status_code, 200)
            self.assertEqual("Lotus", r["foodSearchCriteria"]["brandOwner"])
    








        
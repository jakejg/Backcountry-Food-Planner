import os
from unittest import TestCase
from models import db, connect_db, User, Trip, Meal, Ingredient, TripMeal
from datetime import datetime
os.environ['DATABASE_URL'] = "postgresql:///food_planner_test"
from app import app, create_ingredient, get_nutrition_data

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserTests(TestCase):

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

    def test_create_user_good(self):
        """Test a correct user signup"""

        new_user = User.register(
            username="test3",
            password="lkjklj",
            email="test3@test.com",
            first_name="testman",
            last_name="tester")

        db.session.add(new_user)
        db.session.commit()

        new_user_from_database = User.query.filter_by(username="test3").first()
        self.assertEqual(new_user, new_user_from_database)
    
    def test_create_user_bad(self):
        """Test a user signup with duplicate username"""
        try:
            new_user = User.register(
                username="testuser",
                password="oijdssdf",
                email="t@t.com",
                first_name='first',
                last_name="last"
                )

        except IntegrityError:
            self.assertIsNone(new_user)

    def test_login_user_good(self):
        """Test login with a valid username and password"""

        logged_in_user = User.login("tester1", "password")
        self.assertTrue(logged_in_user)
        self.assertEqual(logged_in_user.username, "tester1" )

    def test_login_user_bad_username(self):
        """Test login with a invalid username"""

        logged_in_user = User.login("testuserbad", "pass123")
        self.assertFalse(logged_in_user)

    def test_authenticate_user_bad_password(self):
        """Test login with a invalid passowrd"""

        logged_in_user = User.login("testuser", "pass1234toomany")
        self.assertFalse(logged_in_user)
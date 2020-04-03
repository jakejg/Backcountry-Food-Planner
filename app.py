import os
from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from models import db, connect_db, Trip, Meal, User
from datetime import date, time
from forms import TripForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///food_planner'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

@app.route('/', methods=["GET", "POST"])
def home():

    form = TripForm()

    if form.validate_on_submit():
        trip = Trip(start_date=form.start_date.data,
                    start_time=form.start_time.data,
                    end_date=form.end_date.data,
                    end_time=form.end_time.data,
                    number_of_people=form.number_of_people.data)
        db.session.add(trip)
        db.session.commit()
        

        return redirect(url_for('select_meals'))

    return render_template('create_trip.html', form=form)

@app.route('/select-meals')
def select_meals():

    return "not ready yet"
    # return render_template('select_meals.html')



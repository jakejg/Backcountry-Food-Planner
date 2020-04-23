import os
SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL', 'postgres:///food_planner'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
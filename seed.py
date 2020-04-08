from app import db
from models import Meal, TripMeal, Trip


# Meal.__table__.drop(db.session.bind)

# Meal.__table__.create(db.session.bind)

db.drop_all()
db.create_all()


# # breakfast
# b1 = Meal(title="Oatmeal", 
#         type_="breakfast", 
#         primary_ingredient="Rolled Oats",
#         secondary_ingredient="Brown Sugar")

# b2 = Meal(title="Granola", 
#         type_="breakfast", 
#         primary_ingredient="Granola", 
#         secondary_ingredient="Dry Coconut Milk")

# # lunch
# l1 = Meal(title="Pita and Hummus", 
#         type_="lunch", 
#         primary_ingredient="Dry Hummus", 
#         secondary_ingredient="Pita")

# l2 = Meal(title="Peanut Butter and Raisins", 
#         type_="lunch", 
#         primary_ingredient="Peanut Butter", 
#         secondary_ingredient="Pita", 
#         additional_ingredient1="Raisins")

# # dinner
# d1 = Meal(title="Rice and Beans", 
#         type_="dinner", 
#         primary_ingredient="Rice", 
#         secondary_ingredient="Dry Beans")

# d2 = Meal(title="Pasta", 
#         type_="dinner", 
#         primary_ingredient="Pasta", 
#         secondary_ingredient="Dry Pasta Sauce")

# db.session.add_all([b1,b2,l1,l2,d1,d2])
# db.session.commit()


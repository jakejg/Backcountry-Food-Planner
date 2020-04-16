from app import db, get_nutrition_data
from datetime import datetime, timedelta
from models import Meal, TripMeal, Trip, User, Ingredient


db.drop_all()
db.create_all()

u = User.register("guestuser", "123" , "guest@email.com", "guest", "guest", True)

db.session.add(u)
db.session.commit()

t = Trip(start_date_time=datetime(2020, 4, 8, 10, 00), 
        end_date_time=datetime(2020, 4, 11, 15, 00),
        number_of_people=3,
        user_id=u.id)

db.session.add(t)
db.session.commit()



# breakfast
b1 = Meal(title="Oatmeal", 
        type_="Breakfast",
        user_id=u.id,
        public=True
        )

oats = Ingredient.create_ingredient(get_nutrition_data(368739))
b1.ingredients.append(oats)

raisins = Ingredient.create_ingredient(get_nutrition_data(408107))
b1.ingredients.append(raisins)

sugar = Ingredient.create_ingredient(get_nutrition_data(519364))
b1.ingredients.append(sugar)


b2 = Meal(title="Granola", 
        type_="Breakfast",
        user_id=u.id,
        public=True
       )
granola = Ingredient.create_ingredient(get_nutrition_data(473897))
b2.ingredients.append(granola)

coconut_milk = Ingredient.create_ingredient(get_nutrition_data(624756))
b2.ingredients.append(coconut_milk)

# lunch
l1 = Meal(title="Pita and Hummus", 
        type_="Lunch",
        user_id=u.id,
        public=True
        )

pita = Ingredient.create_ingredient(get_nutrition_data(384233))
l1.ingredients.append(pita)

hummus = Ingredient.create_ingredient(get_nutrition_data(475281))
l1.ingredients.append(hummus)


l2 = Meal(title="Peanut Butter, Raisins, and Honey", 
        type_="Lunch",
        user_id=u.id,
        public=True
        )
pita = Ingredient.create_ingredient(get_nutrition_data(384233))
l2.ingredients.append(pita)

peanut_butter = Ingredient.create_ingredient(get_nutrition_data(399619))
l2.ingredients.append(peanut_butter)

raisins = Ingredient.create_ingredient(get_nutrition_data(408107))
l2.ingredients.append(raisins)

honey = Ingredient.create_ingredient(get_nutrition_data(385796))
l2.ingredients.append(honey)


# dinner
d1 = Meal(title="Rice and Beans", 
        type_="Dinner",
        user_id=u.id,
        public=True
        )

rice = Ingredient.create_ingredient(get_nutrition_data(447921))
d1.ingredients.append(rice)

beans = Ingredient.create_ingredient(get_nutrition_data(381573))
d1.ingredients.append(beans)


d2 = Meal(title="Pasta", 
        type_="Dinner",
        user_id=u.id,
        public=True
        )

pasta = Ingredient.create_ingredient(get_nutrition_data(370815))
d2.ingredients.append(pasta)

sauce = Ingredient.create_ingredient(get_nutrition_data(519400))
d2.ingredients.append(sauce)

mushrooms = Ingredient.create_ingredient(get_nutrition_data(474185))
d2.ingredients.append(mushrooms)

db.session.commit()

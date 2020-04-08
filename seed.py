from app import db, create_ingredient, get_nutrition_info
from datetime import datetime, timedelta
from models import Meal, TripMeal, Trip


db.drop_all()
db.create_all()

t = Trip(start_date_time=datetime(2020, 4, 8, 10, 00), 
        end_date_time=datetime(2020, 4, 11, 15, 00),
        number_of_people=3)

db.session.add(t)
db.session.commit()


# breakfast
b1 = Meal(title="Oatmeal", 
        type_="breakfast"
        )

oats = create_ingredient(get_nutrition_info(368739))
b1.ingredients.append(oats)

raisins = create_ingredient(get_nutrition_info(408107))
b1.ingredients.append(raisins)

sugar = create_ingredient(get_nutrition_info(519364))
b1.ingredients.append(sugar)


b2 = Meal(title="Granola", 
        type_="breakfast"
       )
granola = create_ingredient(get_nutrition_info(473897))
b2.ingredients.append(granola)

coconut_milk = create_ingredient(get_nutrition_info(624756))
b2.ingredients.append(coconut_milk)

# lunch
l1 = Meal(title="Pita and Hummus", 
        type_="lunch"
        )

pita = create_ingredient(get_nutrition_info(384233))
l1.ingredients.append(pita)

hummus = create_ingredient(get_nutrition_info(475281))
l1.ingredients.append(hummus)


l2 = Meal(title="Peanut Butter, Raisins, and Honey", 
        type_="lunch"
        )
pita = create_ingredient(get_nutrition_info(384233))
l2.ingredients.append(pita)

peanut_butter = create_ingredient(get_nutrition_info(399619))
l2.ingredients.append(peanut_butter)

raisins = create_ingredient(get_nutrition_info(408107))
l2.ingredients.append(raisins)

honey = create_ingredient(get_nutrition_info(385796))
l2.ingredients.append(honey)


# dinner
d1 = Meal(title="Rice and Beans", 
        type_="dinner"
        )

rice = create_ingredient(get_nutrition_info(447921))
d1.ingredients.append(rice)

beans = create_ingredient(get_nutrition_info(381573))
d1.ingredients.append(beans)


d2 = Meal(title="Pasta", 
        type_="dinner"
        )

pasta = create_ingredient(get_nutrition_info(370815))
d2.ingredients.append(pasta)

sauce = create_ingredient(get_nutrition_info(519400))
d2.ingredients.append(sauce)

mushrooms = create_ingredient(get_nutrition_info(474185))
d2.ingredients.append(mushrooms)

db.session.commit()

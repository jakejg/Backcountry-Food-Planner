# Backcountry Meal Planner
Vist https://backcountry-meal-planner.herokuapp.com/ to plan the meals for your next backcountry trip.
Backcountry Meal Planner gives you get detailed nutrition info, packing lists and amounts, and dietary restriction information.

## Using the Website
Enter the start/end dates and number of people for your trip on the homepage. Select from pre-made meals or create your own meal with up to four ingredients. Search for ingredients by keyword and brand. Once the meals have been selected, you will get nutrition info and dietary information such as vegetarain, vegan, or gluten free, for each meal. There is an option to generate a printable packing list with how much to pack for each ingredient. Create an account to save your created meal plans for future reference.

## Additional Features to be Added 
Some features I'd like to add: a form to create a custom ingredient. Functionality to change the weight of meals individually and for an entire trip. Price information for each ingredient and meal.

## Technologies Used
This was created with Javascript, Python, Flask and PostgreSQL. The nutrition data comes from the USDA Food Central API

## Instructions for Running Project Code
You will need Python 3 and PostgreSQL installed on your machine.
1. Download the code <br>
    git clone https://github.com/jakejg/Backcountry-Food-Planner.git 
2. Create a virtual environment and install the dependencies <br>
    python -m venv venv <br>
    source venv/scripts/activate (on a pc) source venv/bin/activate (on a mac) <br>
    pip install -r requirements.txt <br>
3. Go to https://fdc.nal.usda.gov/api-key-signup.html and sign up to get an API key
4. Under the instance folder, open the config.py file, and set FDC_KEY = "YOUR API KEY"
5. And, set SECRET_KEY = "your favorite secret key"
6. Create a database called food_planner <br>
    create_db food_planner
7. Run the seed.py file <br>
    python seed.py




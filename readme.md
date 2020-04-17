Backcountry Meal Planner

Vist https://backcountry-meal-planner.herokuapp.com/ to plan the meals for your next backcountry trip.
Backcountry Meal Planner gives you get detailed nutrition info, packing lists and amounts, and dietary restriction information.
Enter the start/end dates and number of people for your trip on the homepage. Select from pre-made meals or create your own meal with up to four ingredients. Search for ingredients by keyword and brand. Once the meals have been selected, you will get nutrition info and dietary information such as vegetarain, vegan, or gluten free, for each meal. There is an option to generate a printable packing list with how much to pack for each ingredient. Create an account to save your created meal plans for future reference.

This was created with Javascript, Python, Flask and PostgreSQL. The nutrition data comes from the USDA Food Central API

To run this code, follow these steps.
You will need Python 3 and PostgreSQL installed on your machine.
1. Download the repository
2. Create a virtual environment and install the dependencies from the requirements.txt folder
3. Go to https://fdc.nal.usda.gov/api-key-signup.html and sign up to get an API key
4. In the api_key.py file, set fdc_key = "YOUR API KEY"
5. Create a database called food_planner
6. Run the seed.py file




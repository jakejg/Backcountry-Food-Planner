from api_key import fdc_key
from flask import jsonify
import requests

base_url = "https://api.nal.usda.gov/fdc/v1"

def search_for_a_food(food, brand):
    """Make search request to fdc api"""

    params = {
        "query": food,
        "requireAllWords": True,
        "dataType": "Branded",
        "brandOwner": brand
    }
    try:
        search_results = requests.get(f"{base_url}/foods/search?api_key={fdc_key}", params).json()

        return search_results

    except:
        error_response = jsonify(error="There is an issue with the Food Data Central API, please try again later")
        return (error_response, 500)

def get_nutrition_data(fdc_id):
    """Get nutrition data for an ingredient with an id"""

    nutrition_data = requests.get(f"{base_url}/food/{fdc_id}?api_key={fdc_key}").json()
   
    return nutrition_data
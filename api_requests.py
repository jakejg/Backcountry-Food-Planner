from api_key import fdc_key
import requests
base_url = "https://api.nal.usda.gov/fdc/v1"

def search_for_a_food(params):
    """Make  make search request to fdc api"""

    resp = requests.get(f"{base_url}/foods/search?api_key={fdc_key}", params).json()

    return resp

def get_nutrition_info(fdc_id):
    """Get nutrition info for an ingredient with an id"""

    resp = requests.get(f"{base_url}/food/{fdc_id}?api_key={fdc_key}").json()
   
    return resp
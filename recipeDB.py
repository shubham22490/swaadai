import requests

api_key = "Bir8n5fgaMxbiDgm6fgQxGwvnpbjuzbKtP5dSZWccJumhMjd"
base = "https://apis-new.foodoscope.com/"

headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

def make_api_call(api_key, api_url, search_text, page_size):

    params = {
        'searchText': search_text,
        'pageSize': page_size
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()  # Parse response JSON
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None


def recipeInfo(recipe_id: int):
    # Get the recipe information from the API
    url: str = base + "recipe/" + str(recipe_id)
    response = requests.get(url, headers=headers)
    return str(response.json()["payload"])


def searchBySubRegion(sub_region: str):
    # Get recipes by sub-region
    url: str = f"https://cosylab.iiitd.edu.in/api/recipeDB/searchBySubRegion/{sub_region}"
    payload, headers = {}, {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def searchRegion(region: str):
    # Get recipes by region
    url: str = f"https://cosylab.iiitd.edu.in/api/recipeDB/searchRegion/{region}"
    payload, headers = {}, {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def getIngredientsByRecipeId(recipe_id: int):
    # Get ingredients by recipe id
    url: str = f"https://cosylab.iiitd.edu.in/api/recipeDB/getIngredientsByRecipeId/{recipe_id}"
    payload, headers = {}, {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def recipeOfTheDay():
    # Get the recipe of the day
    url: str = base + "recipe/recipeOftheDay"
    try:
        response = requests.get(url, headers=headers)
        print(response.raise_for_status())
        print(response.raw)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return None


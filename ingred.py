import requests
import json
#shubham's recipedb key: Bir8n5fgaMxbiDgm6fgQxGwvnpbjuzbKtP5dSZWccJumhMjd
#nishant's recipedb key (DONT USE): FzNRzSGS9M44jgSV85eNV0hpyz8x-9h1-R_kvGT5BquzSna8
def make_api_call(api_key, api_url, search_text, page_size):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
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

def updateDataset(key, url, text, page_size):
    response = make_api_call(key, url, text, page_size)
    final_data = []
    if response:
        print("API call successful.")
        print(response)
        for item in response["payload"]["data"][1:]:
            try:
                final_data.append(item["recipe_no"])
            except KeyError:
                continue

        with open('ingred.txt', 'a') as f:
            for data in final_data:
                f.write(f"{data}, ")

    else:
        print("API call failed.")


key = "FzNRzSGS9M44jgSV85eNV0hpyz8x-9h1-R_kvGT5BquzSna8"
url = "https://apis-new.foodoscope.com/recipe-search/ingredients"

updateDataset(key, url, "Onion", 10)








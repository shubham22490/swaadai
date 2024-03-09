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
    final_data_json = []

    if response:
        print("API call successful.")
        for item in response["payload"]["data"]:
            final_data_json.append({"Recipe_title": item["Recipe_title"], "id": item["Recipe_id"], "url": item["url"]})
            final_data.append([item["Recipe_title"], item["Recipe_id"]])

        with open('filtered_data.json', 'a') as f:
            json.dump(final_data_json, f, indent=2)

        with open('filtered_data_list.txt', 'a') as file:
            for data in final_data:
                data[0] = data[0].replace(',', ' ')
                file.write(f"{data[0]}: {data[1]}, ")

    else:
        print("API call failed.")


key = "FzNRzSGS9M44jgSV85eNV0hpyz8x-9h1-R_kvGT5BquzSna8"
url = "https://apis-new.foodoscope.com/recipe-search/sub-regions"

updateDataset(key, url, "Indian", 700)
updateDataset(key, url, "Italian", 200)
updateDataset(key, url, "Japanese", 200)
updateDataset(key, url, "French", 200)
updateDataset(key, url, "Thai", 200)












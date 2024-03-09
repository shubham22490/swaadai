import requests
def make_api_call(api_key, api_url, page_size):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()  # Parse response JSON
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None

# Example usage
key = "Bir8n5fgaMxbiDgm6fgQxGwvnpbjuzbKtP5dSZWccJumhMjd"
url = "https://apis-new.foodoscope.com/recipe/recipeOftheDay"
page_size = 1  # Adjust as needed
response = make_api_call(key, url, page_size)
print(response)
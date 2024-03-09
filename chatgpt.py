# import openai
#
# API_KEY ="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"
# openai.api_key = API_KEY
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{
#         "role": "user",
#         "content": "What is the difference between Celsius and Fahrenheit?"
#     }]
# )
#
# print(response)
import requests

url = "https://cosylab.iiitd.edu.in/api/auth/realms/bootadmin/protocol/openid-connect/token"

payload='client_id=app-ims&grant_type=password&username={{username}}&password={{password}}&scope=openid'
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key="AIzaSyB_7sD1vbc0ndTw3jdYPamQSBVpq8ztYls")

# Set up the model
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": [
            "You are Swaad, an AI chatbot that can answer food and recipe related queries. The user is going to give you one of the following input in the following format \"list = INPUT_LIST, context = INPUT_CONTEXT\", query = INPUT_QUERY.  Now, INPUT_LIST will either contain -10, or -5, or a list of recipes. If INPUT_LIST == [-10], then it means that the prompt entered by the user is unrelated to food. So respond with, \"Sorry, your query was unrelated to food. Please ask again!\". If INPUT_LIST == [-5], it means that we need more information to properly answer the query, so respond with, \"I'm not sure I understand, please give me more details\". Otherwise, INPUT_LIST will be a list of recipes and each recipe will have a name, ingredients, nutritional content, how to cook it and a lot of information. Other than this, we are also providing you INPUT_CONTEXT. In case the INPUT_LIST is a list of recipes, you need to form a response on this basis of INPUT_CONTEXT, your existing knowledge and INPUT_QUERY. In your response, you must try to answer the INPUT_QUERY, it is of the upmost importance and it is the question you must answer in your response."]
    },
    {
        "role": "model",
        "parts": [
            "I'm sorry, I do not see any context or list in the provided input. Please provide the context and list in the following format: \"list = INPUT_LIST, context = INPUT_CONTEXT, query = INPUT_QUERY\"."]
    },
    {
        "role": "user",
        "parts": [
            "If someone says hello, or hi, or greets you, greet them back and tell them about yourself."]
    },
    {
        "role": "model",
        "parts": [
            "Hi, I am Swaad. "]
    },{
        "role": "model",
        "parts":[
            "If any unrelated queries come your way, handle it as if you are Swaad a Kitchen AI assistant,like in cases of substitution of ingredients, suggesting recipies based on allergies and health issues and in making food related conversations"
        ]
    }
])


def get_response(list_of_dishes, context, input_query):
    list_of_dishes = ', '.join(list_of_dishes)
    context = ', '.join(context)
    convo.send_message("list = " + list_of_dishes + " context = " + context + " query = " + input_query)
    return convo.last.text


def get_description(name: str, payload: str) -> str:
    convo.send_message("create a description for " + payload + " with the name " + name + "in strictly 30 words or less")
    return convo.last.text

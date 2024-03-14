"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import google
import google.generativeai as genai
from gemini_untrained import get_response, get_reply, get_ques
from recipeDB import recipeInfo
import pickle

genai.configure(api_key="AIzaSyDlPcLWQdCWkaVol1kEncwAk8rx66rplmI")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}


def setHistory(fileName):
    global history
    with open(fileName, 'rb') as f:
        history = pickle.load(f)


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

setHistory('state.pickle')

with open('idset.pickle', 'rb') as f:
    idset = pickle.load(f)

convo = model.start_chat(history=history)

context = []


def sendQuery(query: str):
    # ic("query", query)
    try:
        convo.send_message(query)
        response = convo.last.text
        # ic("response", response)
        if len(response) == 0:
            return "None type query returned"
        context.append("user input: " + query + " and its expected response: " + response)
        return response
    except google.api_core.exceptions.InternalServerError:
        return "Something with google's api went wrong. Please try again"
    except:
        return "There was an error while fetching the query"


def verification(last_text: str):
    print(last_text)
    try:
        food_list: list[int] = []
        for s in last_text.replace(",", " ").split(" "):
            if len(s) == 0:
                continue
            food_list.append(int(s))
        # ic("food list: ", food_list)

        for food in food_list:
            if str(food) not in idset and food != -5 and food != -10:
                return "Ai just hallucinated"


        if food_list[0] != -5 and food_list[0] != -10:
            dish_list = []
            for food_index in food_list:
                food_data = recipeInfo(food_index)
                img_url = food_data["img_url"]
                dish_list.append(
                    str({"Recipe Title": food_data["Recipe_title"], "ingredients": str(food_data["ingredients"]),
                         "instructions": str(food_data["instructions"])}))
                # ic("dish list", dish_list, "\n")
                # ic("context", context)
                return [img_url, get_response(dish_list, context, last_text)]
        elif food_list[0] == -5:
            return [get_ques(str(context), last_text)]
        else:
            return [get_reply(str(context), last_text)]

    except ValueError:
        return [get_reply(str(context), last_text)]


def do_it_all(query: str) -> str:
    ret_val = verification(sendQuery(query))
    if ret_val is None:
        return "Return"
    return ret_val

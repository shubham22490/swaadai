"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
from google.generativeai.types import BlockedPromptException

from gemini_untrained import get_response
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

with open('state.pickle', 'rb') as f:
    history = pickle.load(f)

with open('state.pickle', 'rb') as f:
    idset = pickle.load(f)

convo = model.start_chat(history=history)

context = []


def sendQuery(query: str):
    convo.send_message(query)
    response = convo.last.text
    context.append("user input: " + query + " and its expected response: " + response)
    return response


def verification(last_text: str) -> str:
    print(last_text)
    try:
        food_list: list[int] = []
        for s in last_text.replace(",", " ").split(" "):
            food_list.append(int(s))
        print(food_list)
        valid_response: bool = True
        """for food_index in food_list:
            if str(food_index) in idset:
                continue
            else:
                valid_response = False
                break"""
        if food_list[0] != -5 & food_list[0] != -10:
            if valid_response:
                dish_list: list[str] = []
                for food_index in food_list:
                    dish_list.append(recipeInfo(food_index))
                    print(dish_list)
                    print("context", context)
                return get_response(dish_list, context, input_query)
            else:
                return "Something went wrong, please try again"
        else:
            dish_list = food_list
    except ValueError:
        return last_text
    except BlockedPromptException:
        return "Seems like I can't help you with this :("
    except TypeError:
        return "Something went wrong, please try again"


input_query = str()


def do_it_all(query: str) -> str:
    try:
        ret_val = verification(sendQuery(query))
        return ret_val
    except BlockedPromptException:
        return "Seems like I can't help you with this :("
    except TypeError:
        return "Something went wrong, please try again"
    except ValueError:
        return "Something went wrong, please try again"
    except Exception as e:
        return "Something went wrong, please try again"


#
# if __name__ == '__main__':
#     print(verification(sendQuery("How to make palsta")))

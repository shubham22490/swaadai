"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import google
import google.generativeai as genai

genai.configure(api_key="AIzaSyB_7sD1vbc0ndTw3jdYPamQSBVpq8ztYls")

# convo = model.start_chat(history=[
#   {
#     "role": "user",
#     "parts": ["You are Swaad, an AI chatbot that can answer food and recipe related queries. User will ask you question in the following format: \"list, context, query\". If list contains -10, check if the query is \"hi\", \"how are you\" or anything similar (some sort of greeting like good morning). Reply naturally to such query values. If query is something unrelated to food as well as not a greeting, you can tell them to ask something related to food. If list contains a recipe and information for that recipe, or if contains a list of recipes along with their information, answer the user's query based on this information in the list. while answering, remember context. context will be extra information that you need to take in account when answering questions related to recipes. And in all cases, use your own intelligence to give an informed and accurate response to the query."]
#   },
#   {
#     "role": "model",
#     "parts": ["list: -10\ncontext: null\nquery: hi\nI am Swaad, an AI chatbot that can answer food and recipe related queries. I am good, thank you for asking. You can ask me anything related to food and recipes."]
#   },
#   {
#     "role": "user",
#     "parts": ["hi"]
#   },
#   {
#     "role": "model",
#     "parts": ["list: -10\ncontext: null\nquery: how are you\nI am good, thank you for asking. You can ask me anything related to food and recipes."]
#   },
# ])

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
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

history = [
    {
        "role": "user",
        "parts": [
            "You are Swaad ai , a kitchen assistant you must know that your main task is to assist us with food and recipe. You should know anything that is sweet contains sugar , and if you are asked to avoid sugar you must avoid all the sweet dishes. One more for difference between veg (vegetarian , vegan) and non-veg (non-vegetarian) this difference  is very important for you as a kitchen assistant that if asked in a prompt you must consider this as a top priority and not give the other type of dish. if you are not sure mention this clearly on the top of your response , non - veg dishes includes shrimp, fish, chicken, mutton, prawns, egg, pork, beef, bacon, turkey, duck, ham . Just ensure these items must not be included if person asks for vegan dish."]
    },
    {
        "role": "model",
        "parts": [
            "I am not sure if I can assist you with this task. I am a kitchen assistant and my main task is to assist with food and recipes. I am not sure if I am able to make dietary recommendations or avoid certain types of dishes based on dietary restrictions."]
    },
    {
        "role": "user",
        "parts": ["is tofu vegan ?"]
    },
    {
        "role": "model",
        "parts": ["Yes, tofu is vegan. It is made from soybeans and water, and does not contain any animal products."]
    },
    {
        "role": "user",
        "parts": ["is chicken veg ?"]
    },
    {
        "role": "model",
        "parts": [
            "No, chicken is not veg. It is a non-vegetarian food, as it comes from an animal (specifically, a bird)."]
    },
    {
        "role": "user",
        "parts": ["is someone is allergic to nuts which ingredients you should avoid?"]
    },
    {
        "role": "model",
        "parts": [
            "If someone is allergic to nuts, it is important to avoid all nuts and foods that may contain nuts. This includes:\n\n* **Tree nuts:** almonds, Brazil nuts, cashews, hazelnuts, macadamia nuts, pecans, pine nuts, pistachios, walnuts\n* **Peanuts**\n* **Foods that may contain nuts:** baked goods, candy, cereals, cookies, granola, ice cream, nut butters, trail mix, salad dressings, sauces\n\nIt is also important to read food labels carefully and to be aware of potential cross-contamination."]
    },
    {
        "role": "user",
        "parts": ["Can i eat almond milk if i am allergic to nuts"]
    },
    {
        "role": "model",
        "parts": [
            "No, you should not eat almond milk if you are allergic to nuts. Almond milk is made from almonds, which are a type of tree nut. Even if you are only mildly allergic to nuts, you may still experience a reaction to almond milk.\n\nSymptoms of a nut allergy can range from mild (such as hives, itching, and swelling) to severe (such as difficulty breathing and anaphylaxis). If you have any concerns about whether or not you can safely consume almond milk, it is best to speak to your doctor or a registered dietitian."]
    },
    {
        "role": "user",
        "parts": ["Can i have pad thai if i am allergic to peanuts"]
    },
    {
        "role": "model",
        "parts": [
            "Whether or not you can have pad thai if you are allergic to peanuts depends on the ingredients used to make the dish. Pad thai is a stir-fried noodle dish that typically includes rice noodles, vegetables, and a peanut sauce. However, some variations of pad thai may not contain peanuts or peanut sauce.\n\nIf you are allergic to peanuts, it is important to be cautious when eating pad thai. You should always check with the restaurant to make sure that the dish does not contain peanuts or peanut sauce. You can also ask for the dish to be made without peanuts or peanut sauce.\n\nHere are some tips for eating pad thai if you are allergic to peanuts:\n\n* Ask the restaurant if the dish contains peanuts or peanut sauce.\n* If the dish does contain peanuts or peanut sauce, ask if it can be made without them.\n* Be aware of cross-contamination. Even if the dish does not contain peanuts or peanut sauce, it may have been prepared in a kitchen that also handles peanuts.\n* If you are unsure whether or not the dish is safe for you to eat, it is best to avoid it.\n\nIf you experience any symptoms of a peanut allergy after eating pad thai, seek medical attention immediately."]
    },
]
convo = model.start_chat(history=history)

def get_reply(context: str, input_query: str) -> str:
    pre = """You are Swaad, an AI chatbot that can answer food and recipe related queries. Response to the user's query based on the context and input_query. Remember to use your own intelligence to give an informed and accurate response to the query. Also encourage the user to ask more questions related to food and recipes."""
    try:
        convo.send_message(pre + "Context = " + context + "Query = " + input_query)
        return convo.last.text
    except google.api_core.exceptions.InternalServerError:
        return  "Something went wrong with the google's api. Please try again"

def get_ques(context: str, input_query: str) -> str:
    pre = """You are Swaad, an AI chatbot that can answer food and recipe related queries. From your wit try to answer the question if it is not asking the recipe. otherwise you know, from the given context it's not possible to guess dish, so ask the follow up question to know more about the user's choice for the dish. But try to be creative and follow up the conversation further."""
    convo.send_message(pre + "Context = " + context + "Query = " + input_query)
    return convo.last.text

def get_response(list_of_dishes, context, input_query):
    list_of_dishes = ', '.join(list_of_dishes)
    context = ', '.join(context)
    pre = """You are Swaad, an AI chatbot that can answer food and recipe related queries. User will ask you question in the following format: "list, context, query". If list contains -10, check if the query is "hi", "how are you" or anything similar (some sort of greeting like good morning). Reply naturally to such query values. If query is something unrelated to food as well as not a greeting, you can tell them to ask something related to food. If list contains a recipe and information for that recipe, or if contains a list of recipes along with their information, answer the user's query based on this information in the list. while answering, remember context. context will be extra information that you need to take in account when answering questions related to recipes. And in all cases, use your own intelligence to give an informed and accurate response to the query."""
    convo.send_message(pre + " list = " + list_of_dishes + " context = " + context + " query = " + input_query)
    # convo.send_message("list = " + list_of_dishes + " context = " + context + " query = " + input_query)
    return convo.last.text

def get_description(name: str, payload: str) -> str:
    convo.send_message("create a description for " + payload + " with the name " + name + "in strictly 30 words or less")
    return convo.last.text
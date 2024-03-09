# from openai import OpenAI
#
# OpenAI.api_key = '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'
#
#
# client = OpenAI()
#
#
#
# def get_response(list_of_dishes, context, input_query):
#     list_of_dishes = ', '.join(list_of_dishes)
#     context = ', '.join(context)
#
#     pre = """You are Swaad, an AI chatbot that can answer food and recipe related queries. User will ask you question in the following format: "list, context, query". If list contains -10, check if the query is "hi", "how are you" or anything similar (some sort of greeting like good morning). Reply naturally to such query values. If query is something unrelated to food as well as not a greeting, you can tell them to ask something related to food. If list contains a recipe and information for that recipe, or if contains a list of recipes along with their information, answer the user's query based on this information in the list. while answering, remember context. context will be extra information that you need to take in account when answering questions related to recipes. And in all cases, use your own intelligence to give an informed and accurate response to the query."""
#
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": pre},
#             {"role": "user",
#              "content": "list = " + list_of_dishes + " context = " + context + " query = " + input_query}
#         ]
#     )
#     print("OPENAI'S RESPONSE-----------------------------------------------------")
#     print(completion.choices[0].message)
#     print("OPENAI'S RESPONSE-----------------------------------------------------")

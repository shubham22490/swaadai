import streamlit as st

from google.generativeai.types import BlockedPromptException

import recipeDB
import gemini_trained
import gemini_untrained
import gemini_trained

# App title
st.set_page_config(page_title="swaadAI")

st.markdown("""
# Swaad
### Your AI Kitchen Assistant
""")



@st.cache_data
def getDesc():
    dayResponse = recipeDB.recipeOfTheDay()
    payload = dayResponse["payload"]
    dayTitle = str(payload["Recipe_title"])
    path = str(payload["img_url"])
    url = payload["url"]
    desc = gemini_untrained.get_description(dayTitle, str(dayResponse['payload']))
    return dayTitle, path, url, desc


with st.sidebar:

    widget_title = "<h2 style='text-align: center;margin-top:0;'>RECIPE OF THE DAY</h2>"
    widget_separator = "<hr style='margin-top: -5px;'>"

    st.markdown(widget_title, unsafe_allow_html=True)
    st.markdown(widget_separator, unsafe_allow_html=True)   

    name, img_path, url, desc = getDesc()
    st.markdown(f'<a href = "{url}"><img src="{img_path}" style="max-width: 100%; height: auto;"></a>\n', True)
    # st.markdown(f"[![Image]({img_path})]({url})")
    title = "<h2 style='text-align: center;'>" + name + "</h2>"
    st.markdown(title, True)
    st.markdown("<p style='text-align: justify;'>" + desc + "</p>", True)
    
    st.markdown("-----------------------------------------------------")
    st.markdown("Swaad malfunctioning? Try:")
    resetHistory = st.button("Refresh")
    if resetHistory:
        gemini_trained.setHistory('state.pickle')
        # Do delete the chat history when refreshed clicked.
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
# st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_response(prompt_input):
    return gemini_trained.do_it_all(prompt_input)


# User-provided prompt
if promptText := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": promptText})
    with st.chat_message("user"):
        st.write(promptText)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_response = ""
            placeholder = st.empty()
            response = generate_response(promptText)
            if response is None:
                full_response = "Seems like I can't help you with this :("
            elif(type(response) is not list):
                response = [response]
            for item in response:
                # Check if the item is an image URL or file path
                if item.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # If it's an image, display it using Markdown syntax
                    full_response += f"![Image]({item})\n\n\n"
                else:
                    # If it's not an image, just append the text
                    full_response += item + '\n'
            st.markdown(full_response, True)

    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

import streamlit as st
import speech_recognition as sr
from google.generativeai.types import BlockedPromptException

import recipeDB
import gemini_trained
import gemini_untrained



# App title
st.set_page_config(page_title="swaadAI")

# Initialize SpeechRecognition recognizer
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1  # Adjust silence detection sensitivity (seconds)

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
    desc = gemini_untrained.get_description(dayTitle, str(dayResponse['payload']))
    return dayTitle, path, desc


with st.sidebar:
    st.title("Recipe of the day")
    name, img_path, desc = getDesc()
    st.image(img_path)
    title = "<h2 style='text-align: center;'>" + name + "</h2>"
    st.markdown(title, True)
    st.markdown("<p style='text-align: justify;'>" + desc + "</p>", True)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
# st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_response(prompt_input):
    output = "This will be the response..."
    return output


# User-provided prompt
if promptText := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": promptText})
    with st.chat_message("user"):
        st.write(promptText)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = gemini_trained.do_it_all(promptText)
            placeholder = st.empty()
            full_response = ''
            if response is None:
                response = "Seems like I can't help you with this :("
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

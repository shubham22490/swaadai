import streamlit as st
import clipboard
from streamlit_extras.stylable_container import stylable_container

import recipeDB
import gemini_untrained
import gemini_trained
import speech_recognition as sr
# App title
st.set_page_config(page_title="swaadAI")

st.markdown("""
# Swaad
### Your AI Kitchen Assistant
""")

st.markdown("""
<style>

    
    .st-emotion-cache-ocqkz7{
        position: fixed;
        bottom: 3rem;
        width: 48vw;
    }
    .block-container{
        max-height: 85%;
        overflow: scroll;
        auto
    }
    .st-emotion-cache-1y4p8pa{
        padding: 5rem 1rem 0rem;
    }
</style>
""", unsafe_allow_html=True)


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
    title = f'<a style="text-decoration:none; color:white;" href = "{url}"><h2 style="text-align: center;">' + name + "</h2></a>"
    st.markdown(title, True)
    st.markdown("<p style='text-align: justify;'>" + desc + "</p>", True)
    
    st.markdown("-----------------------------------------------------")
    resetHistory = st.button("Clear History")
    if resetHistory:
        gemini_trained.setHistory('state.pickle')
        # Do delete the chat history when refreshed clicked.
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def on_copy_click(text):
    st.session_state.copied = 1
    clipboard.copy(text)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

if "copied" not in st.session_state:
    st.session_state.copied = 0



count = 0
# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if(message["role"] == 'assistant' and message['content'] != "How may I assist you today?"):
            with stylable_container(
                key="copy_button_"+str(count),
                css_styles="""
                        button:hover, button:active{
                            background-color: green;
                            border: none;
                        }
                        """,
            ):
                st.button("📋", on_click=on_copy_click, args=(message["content"],), key=count)
            count += 1



# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
# st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_response(prompt_input):
    return gemini_trained.do_it_all(prompt_input)

recognizer = sr.Recognizer()
def process_voice_input():
    with st.spinner("Listening: "):
        with sr.Microphone() as source:
            audio_data = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio_data)
        print(query)
        return query
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand your query.")
        return ""
    except sr.RequestError:
        st.error("Sorry, I'm unable to access the Google Speech Recognition API.")
        return ""

# User-provided prompt
with st.container():
    col1, col2 = st.columns([10,1])
    promptText = col1.chat_input("Enter your query:")
    if col2.button("🎤") or promptText is not None:
        st.session_state.copied = 0
        if promptText is None or promptText == "":
            promptText = process_voice_input()
        st.session_state.messages.append({"role": "user", "content": promptText})
        with st.chat_message("user"):
            st.write(promptText)


# User-provided prompt
# if promptText := st.chat_input("Try to say something"):
#     st.session_state.messages.append({"role": "user", "content": promptText})
#     with st.chat_message("user"):
#         st.write(promptText)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(promptText)
            placeholder = st.container()
            full_response = ""
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

            with placeholder:
                st.markdown(full_response, True)

                # Copy Button
                with stylable_container(
                        key="copy_button",
                        css_styles="""
                            button:hover, button:active{
                                background-color: green;
                                border: none;
                            }
                            """,
                ):
                    st.button("📋", on_click=on_copy_click, args=(full_response,))

    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

if st.session_state.copied:
    st.toast(f"Response copied to clipboard", icon='✅')




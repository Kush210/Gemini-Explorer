import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = 'river-oxygen-441015-m8'
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

#load model with config
model = GenerativeModel('gemini-pro', generation_config=config)

chat = model.start_chat()


#helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append (
        {
            "role": "user",
            "content":query
        }
    )

    st.session_state.messages.append(
        {
            "role":"model",
            "content":output
        }
    )

st.title("Gemini Explorer")

# initialize streamlit chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display and load chat history 
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role=message["role"],
        parts = [Part.from_text(message["content"])]
    )

    with st.chat_message(message["role"]):  # Used the correct role variable here
        st.markdown(message["content"])
    
    chat.history.append(content)

#Startup message
if len(st.session_state.messages) == 0:
    initial_prompt = "introduce yourself as Rex, an assistant powered by Google Gemini. Use emojis to be interactive"
    llm_function(chat, initial_prompt)

#Capture user input
query = st.chat_input("Gemini Explorer")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)
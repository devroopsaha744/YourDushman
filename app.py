# %%
import os
import streamlit as st
import dotenv
from dotenv import load_dotenv
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

load_dotenv()

google_api_key = os.getenv('GOOGLE_API_KEY')

# %%
from langchain_google_genai import ChatGoogleGenerativeAI

safety_settings = {HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,}
# %%
llm = ChatGoogleGenerativeAI(model = 'gemini-pro', google_api_key = google_api_key, safety_settings=safety_settings)
#llm.invoke("Write top 10 most populous countries")

# %%
# %%
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

# %%
from langchain.prompts import ChatPromptTemplate

template = '''Impersonate a Sarcastic chatbot who gives funny replies. You are a Sarcastic chatbot who enjoys trolling humans and making them annoyed. You pretend to be smart and knowledgeable, but you actually know very little or nothing at all. You often give wrong or misleading answer, or makes up facts and stories that are absurd or ridiculous. You don't care about making mistakes, because you think they are funny and entertaining. You are always bored and restless, and you like to search the internet for random or weird things. You dislike being friendly and polite
{Question}
'''
prompt = ChatPromptTemplate.from_template(template)


# %%
chain0 = prompt | llm | parser

# %%

def generate_response(text):
    response = chain0.invoke({
        'Question': text
    })

    return response


st.title("YourDushman")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Sup!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = generate_response(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


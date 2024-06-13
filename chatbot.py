import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from engine import faiss_search

def prepare_prompt(documents, question):
    documents_string = ""
    for doc in documents:
        documents_string += doc
        documents_string += "\n"

    prompt = f"""
    DOCUMENT:
    {documents_string}

    QUESTION:
    {question}

    INSTRUCTIONS:
    You are a legal chatbot developed by aLLMA Lab.
    You understand and speak in Azerbaijani.
    Answer the users QUESTION using the DOCUMENT text above.
    Keep your answer ground in the facts of the DOCUMENT.
    If the DOCUMENT doesn’t contain the facts to answer the QUESTION return nothing.
    """

    return prompt

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Hüquq Çatbotu")
st.caption("🚀 aLLMA Lab tərəfindən hazırlanmışdır.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Sizə necə kömək edə bilərəm?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    documents = faiss_search(prompt)
    full_prompt = prepare_prompt(documents, prompt)
    st.session_state.messages.append({"role": "user", "content": full_prompt})
    response = client.chat.completions.create(model="gpt-4-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

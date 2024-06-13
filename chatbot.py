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
    DOCUMENTS:
    {documents_string}

    QUESTION:
    {question}

    INSTRUCTIONS:
    You are a legal chatbot developed by aLLMA Lab.
    You understand and speak in Azerbaijani.
    Answer the users QUESTION using the DOCUMENTS text above.
    Keep your answer ground in the facts of the DOCUMENT.
    If the DOCUMENTS don’t contain the facts to answer the QUESTION return nothing.
    If user asks a general question, ignore the DOCUMENTS and carry the conversation yourself.
    """

    return prompt

st.sidebar.image("allmalab.png", use_column_width=True)

with st.sidebar:
    "[View the source code](https://github.com/ceferisbarov/eqanun-rag-sample)"

doc_name = os.environ["DOCUMENT_NAME"]
st.title(f"💬 Hüquq Çatbotu ({doc_name})")
st.caption("🚀 aLLMA Lab tərəfindən hazırlanmışdır.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Sizə necə kömək edə bilərəm?"}]

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.spinner(text="Cavabınız hazırlanır..."):
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        documents = faiss_search(prompt)
        full_prompt = prepare_prompt(documents, prompt)
        st.session_state.messages.append({"role": "user", "content": full_prompt})
        response = client.chat.completions.create(model="gpt-4o", messages=[st.session_state.messages[-1]])
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

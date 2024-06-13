import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from engine import faiss_search, DOCUMENTS

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

st.sidebar.image("allmalab.png", use_column_width=True)

law = st.selectbox(
    "Qanunlar.",
    ("Əmək Məcəlləsi", "Vergi Məcəlləsi", "Cinayət Məcəlləsi"))

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/ceferisbarov/eqanun-rag-sample)"

# doc_name = os.environ["DOCUMENT_NAME"]
st.title(f"💬 Hüquq Çatbotu ({law})")
st.caption("🚀 aLLMA Lab tərəfindən hazırlanmışdır.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Sizə necə kömək edə bilərəm?"}]

if prompt := st.chat_input():
    for i, j in DOCUMENTS.items():
        print(j[1].ntotal)
        print("----------------")
    st.chat_message("user").write(prompt)
    with st.spinner(text="Cavabınız hazırlanır..."):
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        documents = faiss_search(prompt, index=DOCUMENTS[law][1])
        print(documents[0])
        full_prompt = prepare_prompt(documents, prompt)
        st.session_state.messages.append({"role": "user", "content": full_prompt})
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

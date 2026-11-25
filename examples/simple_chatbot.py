import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("Set OPENROUTER_API_KEY in your local .env file.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

st.title("ENG OSAMA CHATBOT")
question = st.text_input("اكتب سؤالك هنا:")

if st.button("إرسال") and question:
    response = client.chat.completions.create(
        model="qwen/qwen3-coder:free",
        messages=[{"role": "user", "content": question}],
        stream=True,
    )
    st.write_stream(response)

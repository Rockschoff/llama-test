from openai import OpenAI
import streamlit as st
from get_prompt import get_prompt
st.title("Llama-70b")

client = OpenAI(api_key=st.secrets["GROQ_API_KEY"],base_url="https://api.groq.com/openai/v1",)

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama-3.1-70b-versatile"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(user_input)
    prompt=get_prompt(user_input=user_input)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["groq_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
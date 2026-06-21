import streamlit as st

from utils.sentiment import detect_sentiment, should_escalate
from utils.retrieval import search_knowledge_base
from utils.llm import generate_support_reply

st.set_page_config(page_title="AI Support Copilot", page_icon="💬", layout="centered")

st.title("💬 AI Support Copilot")
st.caption("A simple RAG-style support assistant with sentiment detection and escalation logic.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Ask a support question...")

if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.chat_message("user"):
        st.markdown(user_message)

    sentiment = detect_sentiment(user_message)
    escalate = should_escalate(user_message, sentiment)
    retrieved_context = search_knowledge_base(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = generate_support_reply(
                user_message=user_message,
                retrieved_context=retrieved_context,
                sentiment=sentiment,
                escalate=escalate,
            )
            st.markdown(reply)

            with st.expander("Debug info"):
                st.write("Sentiment:", sentiment)
                st.write("Escalate:", escalate)
                st.text(retrieved_context)

    st.session_state.messages.append({"role": "assistant", "content": reply})
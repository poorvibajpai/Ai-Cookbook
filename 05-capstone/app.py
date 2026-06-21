import streamlit as st

from utils.sentiment import detect_sentiment, should_escalate
from utils.retrieval import search_knowledge_base
from utils.llm import generate_support_reply

st.set_page_config(page_title="AI Support Copilot", page_icon="💬", layout="centered")

st.title("💬 AI Support Copilot")
st.caption("A support chatbot with retrieval, sentiment detection, and escalation logic.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi — I’m your AI Support Copilot. Ask me about billing, refunds, account access, or technical issues."
        }
    ]

with st.sidebar:
    st.header("Controls")

    if st.button("Clear chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi — I’m your AI Support Copilot. Ask me about billing, refunds, account access, or technical issues."
            }
        ]
        st.rerun()

    chat_text = "\n\n".join(
        [f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages]
    )

    st.download_button(
        label="Download chat",
        data=chat_text,
        file_name="support_chat_history.txt",
        mime="text/plain",
    )

    st.divider()
    st.markdown("### About")
    st.write("This app uses a small FAQ knowledge base, sentiment tagging, and escalation logic.")
    st.write("Provider: Groq via OpenAI-compatible API")

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

    reply = generate_support_reply(
        user_message=user_message,
        retrieved_context=retrieved_context,
        sentiment=sentiment,
        escalate=escalate,
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

        if "temporarily unavailable" in reply.lower() or "api key is missing" in reply.lower():
            st.warning("Model access issue detected. Check your GROQ_API_KEY or API quota.")

        with st.expander("Debug info"):
            st.write("Sentiment:", sentiment)
            st.write("Escalate:", escalate)
            st.text(retrieved_context)

    st.session_state.messages.append({"role": "assistant", "content": reply})
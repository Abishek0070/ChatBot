import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Load API key securely
api_key = st.secrets["GROQ_API_KEY"]

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    api_key=api_key
)

# System prompt
SYSTEM_PROMPT = SystemMessage(
    content="You are a helpful assistant. Answer clearly."
)

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = [SYSTEM_PROMPT]

# Display chat messages
for msg in st.session_state.chat:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif msg != SYSTEM_PROMPT:
        st.chat_message("assistant").write(msg.content)

# User input
user_input = st.text_input("Ask a question:")

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        st.session_state.chat.append(HumanMessage(content=user_input))
        response = llm.invoke(st.session_state.chat)
        st.session_state.chat.append(response)
        st.rerun()

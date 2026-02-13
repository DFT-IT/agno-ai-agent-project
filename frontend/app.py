import streamlit as st
import requests
import json
import uuid

# Page config
st.set_page_config(
    page_title="AI Agent Chat",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Agent Chat")
st.markdown("---")

# Backend URL
API_URL = "http://localhost:7777"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get response from backend
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": user_input,
                    "session_id": st.session_state.session_id
                },
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Display only the response content
            response_text = result.get("response", "No response")
            st.markdown(response_text)
            
            # Add to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })
            
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend at {API_URL}")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

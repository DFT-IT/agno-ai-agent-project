import streamlit as st
import requests
import json
import uuid
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

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

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "input_mode" not in st.session_state:
    st.session_state.input_mode = "text"

if "last_audio_played" not in st.session_state:
    st.session_state.last_audio_played = None

# Display chat history (WITHOUT audio - audio will be shown separately)
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show agents if available
        if "agents" in message and message["agents"]:
            with st.expander("👥 Agents involved"):
                for agent in message["agents"]:
                    st.markdown(f"**{agent['name']}** ({agent['role']})")

# Input mode toggle
st.markdown("### 📝 Input Mode")
col1, col2 = st.columns(2)
with col1:
    if st.button("⌨️ Text Input", use_container_width=True, 
                 type="primary" if st.session_state.input_mode == "text" else "secondary"):
        st.session_state.input_mode = "text"
        st.rerun()

with col2:
    if st.button("🎤 Voice Input", use_container_width=True,
                 type="primary" if st.session_state.input_mode == "voice" else "secondary"):
        st.session_state.input_mode = "voice"
        st.rerun()

st.markdown("---")

# Display selected input method
user_input = None

if st.session_state.input_mode == "text":
    text_input = st.chat_input("Type your message...")
    user_input = text_input
else:  # voice mode
    audio_input = st.audio_input("Record your message", key="audio_input")
    
    if audio_input:
        try:
            # Convert audio to text with Whisper
            with st.spinner("🎯 Transcribing..."):
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=("audio.wav", audio_input, "audio/wav")
                )
                user_input = transcript.text
                st.success(f"Transcribed: {user_input}")
        except Exception as e:
            st.error(f"❌ Transcription failed: {type(e).__name__}: {str(e)}")
            user_input = None

# Process input
if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "agents": []
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
                timeout=180
            )
            response.raise_for_status()
            result = response.json()
            
            # Display the response content
            response_text = result.get("response", "No response")
            st.markdown(response_text)
            
            # Display agents used
            agents_used = result.get("agents_used", [])
            if agents_used:
                with st.expander("👥 Agents involved"):
                    for agent in agents_used:
                        st.markdown(f"**{agent['name']}** - {agent['role']}")
            
            # Convert response to speech
            with st.spinner("🔊 Generating audio..."):
                audio_response = client.audio.speech.create(
                    model="gpt-4o-mini-tts-2025-12-15",
                    voice="echo",
                    input=response_text
                )
                audio_bytes = audio_response.content
                st.audio(audio_bytes, format="audio/mpeg", autoplay=True)
            
            # Add to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "agents": agents_used
            })
            
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend at {API_URL}")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out")
        except Exception as e:
            st.error(f"❌ Error: {type(e).__name__}: {str(e)}")

# Show continue input if chat exists
if st.session_state.messages:
    st.markdown("---")
    st.write("💬 Continue the conversation:")
    
    if st.session_state.input_mode == "text":
        continue_input = st.chat_input("Type your next message...")
    else:  # voice mode
        continue_input = None
        continue_audio = st.audio_input("Record your next message", key="continue_audio")
        if continue_audio:
            try:
                with st.spinner("🎯 Transcribing..."):
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=("audio.wav", continue_audio, "audio/wav")
                    )
                    continue_input = transcript.text
            except Exception as e:
                st.error(f"❌ Transcription failed: {str(e)}")
    
    # Process continue input
    if continue_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": continue_input,
            "agents": []
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(continue_input)
        
        # Get response
        with st.chat_message("assistant"):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "message": continue_input,
                        "session_id": st.session_state.session_id
                    },
                    timeout=180
                )
                response.raise_for_status()
                result = response.json()
                
                # Display response
                response_text = result.get("response", "No response")
                st.markdown(response_text)
                
                # Display agents
                agents_used = result.get("agents_used", [])
                if agents_used:
                    with st.expander("👥 Agents involved"):
                        for agent in agents_used:
                            st.markdown(f"**{agent['name']}** - {agent['role']}")
                
                # Generate and play audio
                with st.spinner("🔊 Generating audio..."):
                    audio_response = client.audio.speech.create(
                        model="gpt-4o-mini-tts-2025-12-15",
                        voice="echo",
                        input=response_text
                    )
                    audio_bytes = audio_response.content
                    st.audio(audio_bytes, format="audio/mpeg", autoplay=True)
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "agents": agents_used
                })
                
            except Exception as e:
                st.error(f"❌ Error: {type(e).__name__}: {str(e)}")

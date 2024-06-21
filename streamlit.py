import streamlit as st
from videototext2 import video_to_transcript_with_whisper

# Title for the chatbot UI
st.title("Chatbot Interface")

# File uploader for videos
uploaded_video = st.file_uploader("Upload your video here", type=["mp4", "mov"])

# Process the uploaded video and transcribe it
if uploaded_video is not None:
    st.video(uploaded_video)
    transcription = video_to_transcript_with_whisper(uploaded_video)
    if transcription:
        user_input = transcription
    else:
        st.error("Could not transcribe the video.")
else:
    user_input = st.text_input("Type your message here:")

# Placeholder for chatbot response
if user_input:
    st.write("Chatbot response will be displayed here...")
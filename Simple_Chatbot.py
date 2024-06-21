import os
import streamlit as st
from helpers.llm_helper import chat, stream_parser
from config import Config
from dotenv import load_dotenv
from Audio_helper import extract_audio_to_file, video_to_transcript_with_whisper
import moviepy.editor as mp
from Video_helper import download_youtube_audio, generate_unique_filename
load_dotenv()

st.set_page_config(
    page_title="Medi-Guardian",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center;'>Medi-Guardian</h1>", unsafe_allow_html=True)

# Ensure the temp directory exists
if not os.path.exists('temp'):
    os.makedirs('temp')

with st.sidebar:
    st.markdown("# Chat Options")
    
    model = st.selectbox('What model would you like to use?', ('gpt-3.5-turbo', 'gpt-4'))
    temperature = st.number_input('Temperature', value=0.7, min_value=0.1, max_value=1.0, step=0.1,
                                  help="The temperature setting to be used when generating output from the model.")
    max_token_length = st.number_input('Max Token Length', value=1000, min_value=200, max_value=1000, step=100, 
                                       help="Maximum number of tokens to be used when generating output.")
    
    st.markdown("# Video Upload")
    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mkv'])
    
    if uploaded_file is not None:
        video_path = os.path.join('temp', uploaded_file.name)
        audio_path = os.path.join('temp', uploaded_file.name.split('.')[0] + '.wav')
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success("Uploaded file: {}".format(uploaded_file.name))
        extract_audio_to_file(video_path,audio_path)

        transcript = video_to_transcript_with_whisper(audio_path)
        st.markdown("### Transcript")

    st.markdown("# YouTube Link")
    youtube_link = st.text_input('Enter YouTube link')
    if youtube_link:
        st.success("Entered YouTube link: {}".format(youtube_link))

        unique_filename = generate_unique_filename('.mp3')
        audio_output_path = os.path.join('temp', unique_filename)
        
        with st.spinner('Downloading and processing YouTube audio...'):
            try:
                download_youtube_audio(youtube_link, audio_output_path)
                audio_output_path = audio_output_path + '.mp3'
                if os.path.exists(audio_output_path):
                    st.success("Downloaded YouTube audio: {}".format(unique_filename))
                    transcript, end_time, start_time = video_to_transcript_with_whisper(audio_output_path)
                    st.markdown("### Transcript")
                    st.text(transcript)
                    st.success(f"Transcription took {end_time - start_time} seconds")
                else:
                    st.error("Failed to download YouTube audio.")
            except Exception as e:
                st.error(f"Error downloading or processing YouTube audio: {e}")

# checks for existing messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Hi, Welcome to Medi-Guardian. Your personal Health assistant"):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner('Generating response...'):
        llm_response = chat(user_prompt, model=model, max_tokens=max_token_length, temp=temperature)
        stream_output = st.write_stream(stream_parser(llm_response))

        st.session_state.messages.append({"role": "assistant", "content": stream_output})

    last_response = st.session_state.messages[-1]['content']

    if str(last_response) != str(stream_output):
        with st.chat_message("assistant"):
            st.markdown(stream_output)

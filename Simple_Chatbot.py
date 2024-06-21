import os
import streamlit as st
from helpers.llm_helper import chat, stream_parser
from config import SPEAKER_TYPES, initial_prompt, Config
from dotenv import load_dotenv
from Audio_helper import extract_audio_to_file, video_to_transcript_with_whisper
from Video_helper import download_youtube_audio, generate_unique_filename
load_dotenv()
from generative_ai import GeminiProModelChat
chat_conversation = GeminiProModelChat()
import pyperclip
from SQLDB import init_db
st.set_page_config(
    page_title="Medi-Guardian",
    initial_sidebar_state="expanded"
)
init_db()
# Initialize a session state to hold the chat history
if 'chat_history' not in st.session_state:
  st.session_state.chat_history = [initial_prompt]

def clear_chat_history():
  st.session_state.chat_history = [initial_prompt]

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
        pyperclip.copy(transcript)
        st.success('Text copied successfully!')
        st.text_area("Transcript", value=transcript, height=300, disabled=True)
        
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
                    pyperclip.copy(transcript)
                    st.success('Text copied successfully!')
                    st.text_area("Transcript", value=transcript, height=300, disabled=True)
                else:
                    st.error("Failed to download YouTube audio.")
            except Exception as e:
                st.error(f"Error downloading or processing YouTube audio: {e}")

# Get user input and generate response
prompt = st.chat_input("Ask Your Queries... ", key="user_input")

# Show the welcome prompt
with st.chat_message(SPEAKER_TYPES.BOT, avatar="🤖"):
  st.write(initial_prompt['content'])

if prompt:
  st.session_state['chat_history'].append({'role': SPEAKER_TYPES.USER, 'content': prompt})
  # Display chat messages
  for message in st.session_state.chat_history[1:]:
    with st.chat_message(message["role"], avatar="👤" if message['role'] == SPEAKER_TYPES.USER else "🤖"):
      st.write(message["content"])
  
  response_stream = chat_conversation.get_gemini_response(prompt, stream=True)
  response_text = ''
  with st.chat_message(SPEAKER_TYPES.BOT, avatar="🤖"):
    placeholder = st.empty()
    with st.spinner(text='Generating response...'):
      for chunk in response_stream:
        response_text += chunk.text
        placeholder.markdown(response_text)
      placeholder.markdown(response_text)
  
  st.session_state['chat_history'].append({'role': SPEAKER_TYPES.BOT, 'content': response_text})

    # with st.spinner('Generating response...'):
    #     llm_response = chat(user_prompt, model=model, max_tokens=max_token_length, temp=temperature)
    #     stream_output = st.write_stream(stream_parser(llm_response))

    #     st.session_state.messages.append({"role": "assistant", "content": stream_output})

    # last_response = st.session_state.messages[-1]['content']

    # if str(last_response) != str(stream_output):
    #     with st.chat_message("assistant"):
    #         st.markdown(stream_output)

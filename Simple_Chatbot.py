import time
import os
import joblib
import google.generativeai as genai
import streamlit as st
# from helpers.llm_helper import chat, stream_parser
from config import initial_prompt
from dotenv import load_dotenv
load_dotenv()
from Audio_helper import extract_audio_to_file, audio_to_transcript_with_whisper
import moviepy.editor as mp
from Video_helper import download_youtube_audio, generate_unique_filename
from generative_ai import GeminiProModelChat
chat_conversation = GeminiProModelChat()
from SQLDB import init_db, insert_video_data, get_video_transcript
st.set_page_config(
    page_title="Medi-Guardian",
    initial_sidebar_state="expanded"
)
print(os.getenv("GOOGLE_API_KEY"))
new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'
# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except:
    # data/ folder already exists
    pass
# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

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
    st.write('# Pick a previous chat')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a previous chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
            label_visibility="collapsed",
        )
    else:
        # This will happen the first time AI response comes in
        st.session_state.chat_id = st.selectbox(
            label='Pick a previous chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
            label_visibility="collapsed",
        )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
    
    st.markdown("# Video Upload")
    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mkv'])
    
    if uploaded_file is not None:
        start_time = time.time()
        with st.spinner('Getting Video...'):
            transcript = get_video_transcript(uploaded_file.name)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to get transcript: {elapsed_time} seconds")

        if transcript:
            # st.markdown("### Transcript")
            # st.success('Text copied successfully!')
            # st.text_area("Transcript", value=transcript, height=300, disabled=True)
            with st.spinner('Sending Response to chat interface...'):
                st.session_state.chat_input = transcript
        else:
          start_time = time.time()
          video_path = os.path.join('temp', uploaded_file.name)
          audio_path = os.path.join('temp', uploaded_file.name.split('.')[0] + '.wav')
          with open(video_path, 'wb') as f:
              f.write(uploaded_file.getbuffer())
          st.success("Uploaded file: {}".format(uploaded_file.name))
          with st.spinner('Extracting audio...'):
            extract_audio_to_file(video_path,audio_path)
          print(audio_path)
          end_time = time.time()
          elapsed_time = end_time - start_time
          print(f"Time taken to extract audio: {elapsed_time} seconds")

        
          with st.spinner('Generating Text...'):
              transcript = audio_to_transcript_with_whisper(audio_path)
          insert_video_data(video_name=uploaded_file.name,audio_name=audio_path, transcript=transcript, youtube_link="")
        #   st.markdown("### Transcript")
        #   st.success('Text copied successfully!')
        #   st.text_area("Transcript", value=transcript, height=300, disabled=True)
        
          with st.spinner('Sending response to chat interface...'):
              st.session_state.chat_input = transcript


    st.markdown("# Social Video Link")
    youtube_link = st.text_input('Enter Social Video link')
    if youtube_link:
        with st.spinner('Generating Text...'):
            transcript = get_video_transcript(youtube_link)
        if transcript:
            # st.markdown("### Transcript")
            # st.success('Text copied successfully!')
            # st.text_area("Transcript", value=transcript, height=300, disabled=True)
            with st.spinner('Sending response to chat interface...'):
                st.session_state.chat_input = transcript
        else:
            # st.success("Entered YouTube link: {}".format(youtube_link))

            video_id = youtube_link.split('/')[-1]
            video_name = f"{video_id}.mp3"
            audio_output_path = os.path.join('temp', video_name)
            try:
                with st.spinner('Downloading YouTube video...'):
                    download_youtube_audio(youtube_link, audio_output_path)
                    with st.spinner('Extracting audio...'):
                        audio_output_path = audio_output_path + '.mp3'
                
                if os.path.exists(audio_output_path):
                    with st.spinner('Processing audio...'):
                        transcript = audio_to_transcript_with_whisper(audio_output_path)
                    
                    # st.success("Downloaded and processed YouTube audio: {}".format(video_name))
                    insert_video_data(video_name=video_name, audio_name=audio_output_path, transcript=transcript, youtube_link=youtube_link)
                    # st.markdown("### Transcript")
                    # st.text_area("Transcript", value=transcript, height=300, disabled=True)
                    with st.spinner('Sending Text to Chat interface...'):
                        st.session_state.chat_input = transcript
                else:
                    st.error("Failed to download YouTube audio.")
            except Exception as e:
                st.error(f"Error downloading or processing YouTube audio: {e}")
    
    # st.markdown("# Chat Options")
    # # model = st.selectbox('What model would you like to use?', ('gpt-3.5-turbo', 'gpt-4'))
    # # temperature = st.number_input('Temperature', value=0.7, min_value=0.1, max_value=1.0, step=0.1,
    # #                               help="The temperature setting to be used when generating output from the model.")
    # max_token_length = st.number_input('Max Token Length', value=1000, min_value=200, max_value=1000, step=100, 
    #                                    help="Maximum number of tokens to be used when generating output.")


#-------------------------------------------------------------------------------


# Chat history (allows to ask multiple questions)
try:
    st.session_state.messages = joblib.load(
        f'data/{st.session_state.chat_id}-st_messages'
    )
    st.session_state.gemini_history = joblib.load(
        f'data/{st.session_state.chat_id}-gemini_messages'
    )
    print('old cache')
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []
    print('new_cache made')
st.session_state.model = genai.GenerativeModel('gemini-pro')
st.session_state.chat = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

# React to user input
# initial_message = "As a medical expert, please evaluate the text presented in the following message. Indicate whether each method is appropriate or not, and provide a definite result with an explanation. Please assist the user however necessary"
initial_message = """"
Act as a medical expert, please evaluate the text in the following structure

Firstly, Give answers only in english.
Assess if each method mentioned is scientifically proven and suitable for medical use. 
Provide a detailed explanation of the scientific basis if the method is valid and suitable, or explain why it is not if otherwise. 
Finally, conclude whether this method can be recommended for immediate use by humans.
"""

if prompt := st.chat_input("Hello and welcome! Please enter the text you would like to be evaluated by our medical expert. ") or st.session_state.get('chat_input'):
    # Save this as a chat for later
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(
        dict(
            role='user',
            content=prompt,
        )
    )
    ## Send message to AI
    response = st.session_state.chat.send_message(
        initial_message + prompt,
        stream=True,
    )
    # Display assistant response in chat message container
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON,
    ):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = response
        # Streams in a chunk at a time
        for chunk in response:
            # Simulate stream of chunk
            # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                # Rewrites with a cursor at end
                message_placeholder.write(full_response + '▌')
        # Write full message with placeholder
        message_placeholder.write(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON,
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history
    # Save to file
    joblib.dump(
        st.session_state.messages,
        f'data/{st.session_state.chat_id}-st_messages',
    )
    joblib.dump(
        st.session_state.gemini_history,
        f'data/{st.session_state.chat_id}-gemini_messages',
    )
#-------------------------------------------------------------------------

# # Show the welcome prompt
# with st.chat_message(SPEAKER_TYPES.BOT, avatar="🤖"):
#   st.write(initial_prompt['content'])

# if prompt:
#   st.session_state['chat_history'].append({'role': SPEAKER_TYPES.USER, 'content': prompt})
#   # Display chat messages
#   for message in st.session_state.chat_history[1:]:
#     with st.chat_message(message["role"], avatar="👤" if message['role'] == SPEAKER_TYPES.USER else "🤖"):
#       st.write(message["content"])
  
#   response_stream = chat_conversation.get_gemini_response(prompt, stream=True)
#   response_text = ''
#   with st.chat_message(SPEAKER_TYPES.BOT, avatar="🤖"):
#     placeholder = st.empty()
#     with st.spinner(text='Generating response...'):
#       for chunk in response_stream:
#         response_text += chunk.text
#         placeholder.markdown(response_text)
#       placeholder.markdown(response_text)
  
#   st.session_state['chat_history'].append({'role': SPEAKER_TYPES.BOT, 'content': response_text})

    # with st.spinner('Generating response...'):
    #     llm_response = chat(user_prompt, model=model, max_tokens=max_token_length, temp=temperature)
    #     stream_output = st.write_stream(stream_parser(llm_response))

    #     st.session_state.messages.append({"role": "assistant", "content": stream_output})

    # last_response = st.session_state.messages[-1]['content']

    # if str(last_response) != str(stream_output):
    #     with st.chat_message("assistant"):
    #         st.markdown(stream_output)

import os
# from dotenv import load_dotenv
# # Load the .env file
# load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SYSTEM_PROMPT = "You are  a medical expert, that will help the user"

class GoogleAIConfig:
    GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")

# Global variables
class SPEAKER_TYPES:
  USER = "user"
  BOT = "bot"


initial_prompt = {"role": SPEAKER_TYPES.BOT, "content": "How may I assist you today?"}

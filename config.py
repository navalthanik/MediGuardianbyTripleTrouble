import os

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SYSTEM_PROMPT = "You are  a medical expert, that will help the user"
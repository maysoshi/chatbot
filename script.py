import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SYSTEM_PROMPT = "You are a helpful chatbot assistant to answer questions for users."






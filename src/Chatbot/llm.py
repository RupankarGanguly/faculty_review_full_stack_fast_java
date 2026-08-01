from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

api = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=api,
    model="llama-3.3-70b-versatile",
    temperature=0.5
)

def get_llm():
    return llm
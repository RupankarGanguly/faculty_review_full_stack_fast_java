import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

_api_key = os.getenv("GROQ_API_KEY")

_llm = None


def get_llm():
    """Lazy-load the Groq LLM so the app can start even if key is missing."""
    global _llm
    if _llm is None:
        if not _api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set in .env. "
                "Get a free key from https://console.groq.com"
            )
        _llm = ChatGroq(
            api_key=_api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )
    return _llm

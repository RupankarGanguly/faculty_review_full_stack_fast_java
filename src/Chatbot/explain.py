from src.Chatbot.llm import get_llm
from src.Chatbot.structure_text import ScreenshotContent


def explain_content(result: ScreenshotContent) -> str:
    llm = get_llm()

    explanation_prompt = f"""
You are an expert teacher.

Explain the following {result.content_type} in simple bullet points.

Topic: {result.topic or "General"}
Subtopic: {result.subtopic or "N/A"}

Content:
{result.content}

Also suggest 2-3 online resources (books, websites, or YouTube videos) to learn these concepts better.
Keep the explanation clear and student-friendly.
"""

    response = llm.invoke(explanation_prompt)
    return response.content

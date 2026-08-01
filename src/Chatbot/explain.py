# from structure_text import process_screenshot
from src.Chatbot.structure_text import process_screenshot
from src.Chatbot.llm import get_llm
llm=get_llm()
def explain_content(result):
    explanation_prompt = f"""
You are an expert teacher.

Explain the following {result.content_type} in simple bullet points.

Topic: {result.topic}
Subtopic: {result.subtopic}

Content:
{result.content}

Also provide online resources like books or youtube videos to learn the concepts
"""

    response = llm.invoke(explanation_prompt)

    return response.content
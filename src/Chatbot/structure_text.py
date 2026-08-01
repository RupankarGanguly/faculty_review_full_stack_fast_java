from typing import Literal

from pydantic import BaseModel

from src.Chatbot.cleaning import clean_text
from src.Chatbot.read_from_paper import extract_text
from src.Chatbot.llm import get_llm


class ScreenshotContent(BaseModel):
    content_type: Literal[
        "question",
        "passage",
        "notes",
        "code",
        "solution",
        "mixed",
        "unknown",
    ]
    title: str | None = None
    content: str
    topic: str | None = None
    subtopic: str | None = None
    marks: int | None = None


def process_screenshot(image_path: str) -> ScreenshotContent:
    text = extract_text(image_path)
    query = clean_text(text)

    if not query.strip():
        return ScreenshotContent(
            content_type="unknown",
            content="No text could be extracted from the image.",
            topic=None,
            subtopic=None,
        )



    llm = get_llm()
    structured_output = llm.with_structured_output(ScreenshotContent)

    prompt = f"""
You are an OCR document parser.

The following text was extracted from a screenshot.

Your task is to:

1. Identify what type of content the screenshot contains.
2. Choose one of:
   - question
   - passage
   - notes
   - code
   - solution
   - mixed
   - unknown
3. Extract the main content.
4. Infer the topic and subtopic if possible.
5. If marks are explicitly mentioned, extract them as an integer.

Do NOT summarize.
Do NOT explain.
Do NOT describe the screenshot.

Copy the main textual content exactly as it appears, correcting only obvious OCR mistakes.

The "content" field must contain the extracted text itself, not a summary of it.

Screenshot Text:

{query}
"""



    return structured_output.invoke(prompt)

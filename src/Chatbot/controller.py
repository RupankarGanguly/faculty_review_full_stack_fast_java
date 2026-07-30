import os
import tempfile
import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException, status

from src.Chatbot.structure_text import process_screenshot
from src.Chatbot.explain import explain_content


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
MAX_FILE_SIZE_MB = 10


async def process_image(file: UploadFile) -> dict:
    """
    1. Save uploaded image temporarily
    2. OCR extract text
    3. Structure with LLM
    4. Generate explanation
    5. Clean up temp file
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided",
        )

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large ({size_mb:.1f} MB). Max {MAX_FILE_SIZE_MB} MB.",
        )

    # Write to a unique temp file
    tmp_dir = tempfile.gettempdir()
    tmp_path = os.path.join(tmp_dir, f"chatbot_{uuid.uuid4().hex}{ext}")

    try:
        with open(tmp_path, "wb") as f:
            f.write(content)

        # OCR + structure
        structured = process_screenshot(tmp_path)

        # Explanation
        explanation = explain_content(structured)

        return {
            "content_type": structured.content_type,
            "title": structured.title,
            "topic": structured.topic,
            "subtopic": structured.subtopic,
            "marks": structured.marks,
            "extracted_content": structured.content,
            "explanation": explanation,
        }

    except RuntimeError as e:
        # Missing GROQ_API_KEY etc.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process image: {str(e)}",
        )
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

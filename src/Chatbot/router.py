from fastapi import APIRouter, Depends, UploadFile, File, status

from src.Chatbot import controller
from src.utils.helper import is_authenticated
from src.user.models import UserModel

chatbot_router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@chatbot_router.post(
    "/process",
    status_code=status.HTTP_200_OK,
    summary="Upload a screenshot and get OCR + explanation",
)
async def process_screenshot(
    file: UploadFile = File(..., description="Image of notes / question / code"),
    user: UserModel = Depends(is_authenticated),
):
    """
    Upload a screenshot (notes, question paper, code, etc.).

    Returns:
    - content_type (question / notes / code / ...)
    - topic & subtopic
    - extracted text
    - simple explanation + learning resources
    """
    return await controller.process_image(file)


@chatbot_router.get("/health")
def chatbot_health():
    """Quick check that the chatbot module is loaded."""
    return {"status": "ok", "module": "chatbot"}

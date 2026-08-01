from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.db import Base, engine
from src.Faculty.models import FacultyModel  # noqa: F401
from src.user.models import UserModel  # noqa: F401
from src.Faculty.router import facultyrouter
from src.user.router import user_routes
from src.Chatbot.router import chatbot_router

app = FastAPI(title="Faculty Review + Chatbot System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://faculty-review-full-stack-fast-java.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
Base.metadata.create_all(bind=engine)

app.include_router(user_routes)
app.include_router(facultyrouter)
app.include_router(chatbot_router)


@app.get("/")
def root():
    return {
        "message": "Faculty Review + Chatbot API is running",
        "docs": "/docs",
        "endpoints": {
            "auth": ["/user/register", "/user/login"],
            "faculty": [
                "/task/create",
                "/task/get_all",
                "/task/update/{id}",
                "/task/delete/{id}",
            ],
            "chatbot": ["/chatbot/process", "/chatbot/health"],
        },
    }

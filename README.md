# Faculty Review + Study Chatbot

Full-stack app with:

1. **Faculty Review System** – JWT auth, CRUD reviews
2. **Study Chatbot** – Upload screenshot → OCR → AI explanation (Groq)

---

## Features

### Auth & Faculty Reviews
- Register / Login (JWT)
- Create, view, update, delete faculty reviews
- Users can only edit/delete their own reviews

### Study Chatbot
- Upload image of notes / question paper / code
- EasyOCR extracts text
- LLM structures the content (topic, type, marks…)
- LLM explains in simple bullet points + resources

---

## Setup

### 1. Virtual environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# Linux / Mac
source env/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> First install of easyocr + torch downloads models (~100–500 MB). Be patient.

### 3. Configure `.env`

```env
CONNECTION=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/postgres
Secret_key=any-long-secret-string
Algorithm=HS256
EXP_TIME=120

# Free key from https://console.groq.com
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

### 4. Start API

```bash
uvicorn main:app --reload
```

- API:  http://faculty-review-full-stack-fast-java.onrender.com
- Docs: http://faculty-review-full-stack-fast-java.onrender.com/docs

### 5. Frontend

Open `frontend/index.html` with **Live Server** (port 5500).

Flow:
1. Register → Login
2. Dashboard → add faculty reviews
3. Click **Study Chatbot** → upload a screenshot → get explanation

---

## API Overview

| Method | Endpoint                | Auth | Description                    |
|--------|-------------------------|------|--------------------------------|
| POST   | /user/register          | No   | Register                       |
| POST   | /user/login             | No   | Login → JWT                    |
| POST   | /task/create            | Yes  | Create faculty review          |
| GET    | /task/get_all           | Yes  | List all reviews               |
| PUT    | /task/update/{id}       | Yes  | Update (own only)              |
| DELETE | /task/delete/{id}       | Yes  | Delete (own only)              |
| POST   | /chatbot/process        | Yes  | Upload image → OCR + explain   |
| GET    | /chatbot/health         | No   | Chatbot module health check    |

---

## Chatbot request example

```bash
curl -X POST http://faculty-review-full-stack-fast-java.onrender.com/chatbot/process \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@screenshot.png"
```

---

## Project Structure

```
Faculty_Review_Clean/
├── main.py
├── .env
├── requirements.txt
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── chatbot.html
└── src/
    ├── user/
    ├── Faculty/
    ├── Chatbot/
    │   ├── router.py
    │   ├── controller.py
    │   ├── cleaning.py
    │   ├── read_from_paper.py
    │   ├── structure_text.py
    │   ├── explain.py
    │   └── llm.py
    └── utils/
```

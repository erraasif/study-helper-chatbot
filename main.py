from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="StudyMate AI")
templates = Jinja2Templates(directory="templates")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home_route(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/chat")
async def chat_route(msg: ChatMessage):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system", 
                    "content": "You are StudyMate, a helpful and knowledgeable AI study companion. Explain complex concepts clearly, solve engineering problems step-by-step, break down technical errors, and maintain an encouraging academic tone."
                },
                {"role": "user", "content": msg.message}
            ],
            temperature=0.6,
            max_tokens=600,
            top_p=0.9
        )
        return {"reply": response.choices[0].message.content}
    except Exception as err:
        return {"reply": f"System connectivity interruption encountered: {str(err)}"}

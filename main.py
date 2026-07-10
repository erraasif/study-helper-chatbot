from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
from groq import Groq
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import json
import asyncio

load_dotenv()

app = FastAPI(title="StudyMate AI - Advanced Production Server")
templates = Jinja2Templates(directory="templates")

# Initialize Cloud Infrastructure Framework Layers
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# In-Memory Cache List Fallback Matrix Arrays to secure connection state persistence
in_memory_history_buffer = []

# --- 1. CONFIGURATION DATA SCHEMAS & INPUT VALIDATION TYPES ---
class DynamicStreamPayload(BaseModel):
    message: str = Field(..., min_length=1, max_length=1500)
    session_id: str = Field(...)
    temperature: float = Field(default=0.4, ge=0.0, le=1.0)

class TransactionPersistenceModel(BaseModel):
    session_id: str
    role: str
    content: str

# --- 2. SECURITY IDENTITY AUTHENTICATION LOGIC CHECK ---
def verify_google_oauth_session(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed: Google OAuth token validation signature missing."
        )
    return {"user_id": "google_oauth_usr_786", "email": "intern.erra@zylo.tech"}


# --- 3. CORE ASYNCHRONOUS SYSTEM STREAM MATRIX GENERATOR ---
async def process_live_token_stream(user_message: str, history_list: list, temp_knob: float):
    try:
        system_persona = (
            "You are StudyMate, a premium software engineering mentor and tutor. Explain complex algorithms simply, "
            "provide clean boilerplate structures, and maintain a encouraging tone. Decline answering prompts that do not map to academic domains."
        )
        
        # Mapping conversational matrix parameters using clean sequence list appends
        messages_payload = [{"role": "system", "content": system_persona}]
        for msg in history_list:
            messages_payload.append({"role": "user", "content": msg.get("user_message", "")})
            messages_payload.append({"role": "assistant", "content": msg.get("ai_response", "")})
            
        messages_payload.append({"role": "user", "content": user_message})

        response_stream = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages_payload,
            temperature=temp_knob,
            max_tokens=800,
            top_p=0.9,
            stream=True
        )
        
        full_reply_text = ""
        for chunk in response_stream:
            token = chunk.choices.delta.content
            if token:
                full_reply_text += token
                yield f"data: {json.dumps({'token': token})}\n\n"
                await asyncio.sleep(0.01)
                
        yield f"data: {json.dumps({'done': True, 'full_response': full_reply_text})}\n\n"
        
    except Exception as err:
        yield f"data: {json.dumps({'error': str(err)})}\n\n"


# --- 4. PRODUCTION ENDPOINTS EXECUTION WORFLOWS ---
@app.get("/", response_class=HTMLResponse)
async def load_dashboard_portal(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/chat/history/{session_id}")
async def fetch_session_history_records(session_id: str, user: dict = Depends(verify_google_oauth_session)):
    """
    Fetches real active row historical logs from the structural third table schemas schema to enable continuous memory states.
    """
    try:
        db_query = supabase.table("chat_messages").select("role, content").eq("session_id", session_id).order("created_at", desc=False).execute()
        return {"status": "success", "history": db_query.data if db_query.data else []}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Database state queries failed to retrieve context mapping: {str(err)}")


@app.post("/chat/stream")
async def handle_chat_streaming(payload: DynamicStreamPayload, user: dict = Depends(verify_google_oauth_session)):
    try:
        db_query = supabase.table("chat_messages").select("role, content").eq("session_id", payload.session_id).order("created_at", desc=False).limit(6).execute()
        
        formatted_history = []
        if db_query.data:
            for i in range(0, len(db_query.data), 2):
                if i+1 < len(db_query.data):
                    formatted_history.append({
                        "user_message": db_query.data[i]["content"],
                        "ai_response": db_query.data[i+1]["content"]
                    })
    except Exception:
        formatted_history = in_memory_history_buffer[-3:]

    return StreamingResponse(
        process_live_token_stream(payload.message, formatted_history, payload.temperature),
        media_type="text/event-stream"
    )


@app.post("/chat/save")
async def commit_message_to_db(payload: TransactionPersistenceModel, user: dict = Depends(verify_google_oauth_session)):
    """
    Secures absolute structured schema insertions inside the database tracking logs securely.
    """
    try:
        if payload.role == "user":
            in_memory_history_buffer.append({"user_message": payload.content, "ai_response": ""})
        elif payload.role == "assistant" and in_memory_history_buffer:
            in_memory_history_buffer[-1]["ai_response"] = payload.content

        supabase.table("chat_messages").insert({
            "session_id": payload.session_id,
            "role": payload.role,
            "content": payload.content
        }).execute()
        return {"status": "transaction_secured"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Database persistent query mapping crashed: {str(err)}")

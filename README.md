# AuraLearn AI - Aesthetic Academic Study Companion

A full-stack, security-hardened academic mentoring application. This system leverages **FastAPI**, **Pydantic**, and **Groq Cloud Inference** to serve interactive software engineering lessons, persisting session history and securing client transactions through **Supabase**.

---

## 🛠️ Technology Stack

* **Backend Gateway:** FastAPI (Asynchronous Python API runtime)
* **Data Verification:** Pydantic (Strict API payload schema enforcement)
* **LLM Core Engine:** Groq SDK (`llama-3.1-8b-instant` model integration)
* **Identity Management:** Google OAuth via Supabase Auth
* **Database & Storage:** Supabase PostgreSQL with active Row-Level Security (RLS)
* **Client-Side Interface:** HTML5, CSS3, native JavaScript routing, and inline SVG vector icons

---

## 📋 Core Architectures

### 1. Three-Panel Cognitive Studio
The interface is structured as an advanced three-panel study studio. It provides a left-hand navigation sidebar for session logs, a central messaging workspace with Marked.js integration, and a right-hand cognitive analytics panel.

### 2. Identity & Session Scoping
The frontend uses the Supabase JS SDK to delegate Google login. The user's active session is securely synced, and a Bearer JWT token is included in the headers of all analytical and chat requests. The backend validates this token against the Supabase Auth tier before rendering workspace data.

### 3. Multi-Turn Contextual Memory
The backend parses previous messages stored inside Supabase under the requested session, rebuilding conversation contexts dynamically for Groq before initiating streaming. If the connection drops or is manually cancelled, the serverless function guarantees the persistence of any partially generated tokens.

### 4. Interactive Study Tools
* **Aesthetic Focus Timer:** A fully functional, local JavaScript Pomodoro study timer with built-in play, pause, and countdown states.
* **Brain Vitals Monitor:** Four real-time indicators tracking focus indices, estimated cognitive load, retention goals, and active study time.
* **Comprehension Diagnostics:** Progress bar trackers estimating student understanding and topic mastery.

---

## 🔒 Security & Git Safety (Non-Negotiables)

To prevent credential leakage, secret keys must **never** be committed to source control.

### 1. Local Git Exclusion
Before staging or committing any code, verify that a `.gitignore` file exists in the root directory and explicitly contains your local environment file:

# Exclude environment secret files
.env
.env.local

# Exclude Python compiled caches
__pycache__/
*.pyc

### 2. Live Production Secrets
For cloud environments, secrets must be injected securely. In Vercel, navigate to **Project Settings -> Environment Variables** to add your keys.

---

## 🚀 Setup & Execution Guide

### 1. Configure the Database Schema
Execute the following setup commands inside your **Supabase SQL Editor** to construct the database schema and enable safety policies:

-- Create conversations mapping
CREATE TABLE public.conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create message transaction history
CREATE TABLE public.messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    conversation_id UUID REFERENCES public.conversations(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Turn on Row-Level Security (RLS)
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

-- Configure database policies restricting records to the owner
CREATE POLICY "Allow authenticated users to manage their own conversations" 
    ON public.conversations FOR ALL TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "Allow authenticated users to manage their own messages" 
    ON public.messages FOR ALL TO authenticated USING (auth.uid() = user_id);

### 2. Local Environment Setup
Create a file named `.env` in the root of your local workspace (do not push this to GitHub):

GROQ_API_KEY=gsk_your_actual_key_here
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_actual_anon_public_key

### 3. Install Requirements
pip install -r requirements.txt

### 4. Execute the Application Server
python -m uvicorn main:app --reload

Navigate to: http://localhost:8000

---

## 🌐 Deploying to Vercel

1. Link your GitHub repository directly to your Vercel project dashboard for automated deployments.
2. Configure the environment variables (GROQ_API_KEY, SUPABASE_URL, and SUPABASE_ANON_KEY) in your Vercel Settings.
3. Ensure you register your live Vercel domain in your Supabase Auth Redirect URLs so that Google OAuth redirects back to your production application successfully.
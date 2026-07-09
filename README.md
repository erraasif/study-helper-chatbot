# StudyMate AI - Conversational Study Assistant

A premium, full-stack AI study companion application built using **FastAPI**, **Pydantic**, and **Groq Cloud Inference** to serve clear, structured academic explanations through a modern glassmorphic web interface.

## 🛠️ Technology Stack
* **Backend Framework:** FastAPI (Asynchronous Python API gateway)
* **Data Validation:** Pydantic (Strict typing constraint schemas)
* **LLM Cloud Engine:** Groq Client SDK (`llama-3.1-8b-instant` inference model)
* **Frontend UI Layout:** Semantic HTML5, embedded CSS3, and native JavaScript routing

## 📋 Features
* **Intelligent Tutoring AI:** Leverages a cloud-hosted LLM configured as a supportive academic mentor.
* **Optimized Inference Controls:** Tuned parameter knobs (Temperature set to 0.6 for accurate, reliable responses).
* **Premium User Dashboard:** Clean dark-mode layout with responsive conversational bubbles.
* **Environment Variable Safety:** Secure credentials management using an decoupled `.env` parsing block.

## 🚀 How to Run Locally

1. Clone or navigate to the project directory and install required system packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your secret variable configuration by adding your key into a `.env` file:
   ```text
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```
3. Start up up the hot-reloading development server gateway:
   ```bash
   python -m uvicorn main:app --reload
   ```
4. Open your web browser and navigate to the active interface engine:
   `http://localhost:8000`

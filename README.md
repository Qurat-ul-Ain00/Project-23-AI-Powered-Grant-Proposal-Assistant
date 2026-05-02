# AI Grant Proposal Assistant

A simple multi-agent AI system that helps users generate grant proposals using local LLMs (Ollama + LLaMA 2).

## Agents:
1. Outline Designer Agent: Creates structured grant proposal sections.
2. Budget Estimator Agent: Generates project budget breakdown.
3. Reviewer Simulation Agent: Gives feedback, risks, and improvement suggestions.

## Features:
- Generate complete grant proposal
- Estimate project budget
- AI reviewer feedback
- Save proposal versions (memory system)

---

## Setup & Run

### 1. Install requirements
pip install -r requirements.txt

### 2. Install Ollama and model
Download Ollama: https://ollama.com

Then run:
ollama pull llama2

### 3. Run Backend (FastAPI)
cd backend
uvicorn main:app --reload --port 8000

### 4. Run Frontend (Streamlit)
cd frontend
streamlit run app.py

### 5. Open in browser
http://localhost:8501

---

## How it works

- Enter topic, goals, and funding agency
- System generates:
  - Proposal outline
  - Budget estimation
  - Reviewer feedback
- Results are stored with version history

---

## API Endpoints

POST /generate/ -> Generate proposal

GET /memory/{topic} -> Get saved versions

---

## Project Structure

grant-ai/
├── backend/
│   ├── main.py
│   └── memory.json
├── frontend/
│   └── app.py
├── requirements.txt
└── README.md

---

## Notes

- Runs fully offline using Ollama
- No API keys required
- Uses local LLaMA 2 model
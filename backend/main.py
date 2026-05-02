from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os
from datetime import datetime

app = FastAPI()

MEMORY_FILE = "backend/memory.json"

# Initialize memory
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

def call_ollama(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

# Request schema
class ProposalInput(BaseModel):
    topic: str
    goals: str
    agency: str

# ---------------- AGENTS ---------------- #

def outline_agent(data):
    prompt = f"""
    Create a detailed grant proposal outline for:

    Topic: {data.topic}
    Goals: {data.goals}
    Funding Agency: {data.agency}

    Include:
    - Executive Summary
    - Problem Statement
    - Objectives
    - Methodology
    - Expected Impact
    - Timeline
    """
    return call_ollama(prompt)

def budget_agent(data):
    prompt = f"""
    Estimate a realistic budget for this project:

    Topic: {data.topic}
    Goals: {data.goals}

    Include:
    - Personnel
    - Equipment
    - Operations
    - Misc
    - Total
    """
    return call_ollama(prompt)

def reviewer_agent(outline, budget):
    prompt = f"""
    You are a strict grant reviewer.

    Evaluate this proposal:

    OUTLINE:
    {outline}

    BUDGET:
    {budget}

    Provide:
    - Strengths
    - Weaknesses
    - Risks
    - Score (1-10)
    - Improvements
    """
    return call_ollama(prompt)

# ---------------- MEMORY ---------------- #

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

def update_memory(topic, result):
    mem = load_memory()

    if topic not in mem:
        mem[topic] = []

    version = len(mem[topic]) + 1

    mem[topic].append({
        "version": version,
        "timestamp": str(datetime.now()),
        "result": result,
        "rationale": "Initial generation" if version == 1 else "Refined version"
    })

    save_memory(mem)

# ---------------- API ---------------- #

@app.post("/generate/")
def generate_proposal(data: ProposalInput):
    outline = outline_agent(data)
    budget = budget_agent(data)
    review = reviewer_agent(outline, budget)

    result = {
        "outline": outline,
        "budget": budget,
        "review": review
    }

    update_memory(data.topic, result)

    return result


@app.get("/memory/{topic}")
def get_memory(topic: str):
    mem = load_memory()
    return mem.get(topic, [])
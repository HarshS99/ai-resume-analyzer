import io
import pdfplumber
import os
import requests

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def extract_text_from_pdf(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n".join(pages)

def analyze_resume(resume_text, target_role):
    system_prompt = (
        "You are an expert resume reviewer. Analyze the given resume text against the target role. "
        "Provide:\n"
        "1. ATS score (0-100).\n"
        "2. Missing skills/keywords.\n"
        "3. Strengths and weaknesses.\n"
        "4. 5-10 improvement suggestions.\n"
        "Return a JSON object with keys: score, missing, strengths, weaknesses, suggestions."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Resume:\n{resume_text}\n\nTarget Role: {target_role}"}
    ]
    response = requests.post(
        GROQ_ENDPOINT,
        json={"model": "llama3-70b-8192", "messages": messages, "temperature": 0.7},
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
    )
    response.raise_for_status()
    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return {"error": "Invalid response from Groq API"}

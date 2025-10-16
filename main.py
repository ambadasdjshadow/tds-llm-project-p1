import os
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel

# --- Configuration ---
# IMPORTANT: Never hardcode your key! Use environment variables.
# You will set this environment variable (e.g., OPENAI_API_KEY) in your deployment environment (like Vercel).
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# The secret value the grader (LLM) expects for verification.
# REPLACE 'YOUR_COURSE_SECRET_VALUE_HERE' with the actual secret from your assignment instructions.
REQUIRED_SECRET_VALUE = "YOUR_COURSE_SECRET_VALUE_HERE" 

# --- FastAPI App Setup ---
app = FastAPI(title="TDS LLM Project P1 API")

# Define the structure for the request body (optional for a simple GET, but good practice)
class LLMRequest(BaseModel):
    prompt: str = "Explain the concept of tokenization in LLMs."

# Initialize OpenAI client
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    # The app will still run, but the /llm endpoint will fail if the key is missing.


# --- 1. LLM Core Endpoint ---
@app.post("/llm")
async def process_prompt(request: LLMRequest):
    """
    Endpoint to process a user prompt using GPT-3.5-turbo.
    """
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured.")

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for data science and programming."},
                {"role": "user", "content": request.prompt}
            ]
        )
        return {
            "status": "success",
            "prompt": request.prompt,
            "response": completion.choices[0].message.content,
            "model_used": completion.model
        }
    except Exception as e:
        # Log the error for debugging but provide a generic error to the user
        print(f"OpenAI API Error: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with the LLM API.")


# --- 2. Grading Verification Endpoint ---
@app.get("/verify")
async def verify_submission():
    """
    This endpoint is for the grading LLM to verify the submission.
    It must return the exact secret string defined in the assignment.
    """
    return {"secret_value": REQUIRED_SECRET_VALUE}


# --- Root Health Check Endpoint ---
@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running. Use /llm for LLM requests and /verify for grading."}
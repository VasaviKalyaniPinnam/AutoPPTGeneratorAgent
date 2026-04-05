import os

class Config:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    MODEL_ID     = "llama-3.3-70b-versatile"
    OUTPUT_FILE  = "output.pptx"
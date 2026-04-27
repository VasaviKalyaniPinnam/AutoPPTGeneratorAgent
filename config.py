import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY") 
    MODEL_ID     = "llama-3.3-70b-versatile"
    OUTPUT_FILE  = "output.pptx"
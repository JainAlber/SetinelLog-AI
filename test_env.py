import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("GROQ_API_KEY") is not None:
    print("Key Loaded")
else:
    print("Key Not Loaded")

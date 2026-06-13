import os
from huggingface_hub import whoami

token = os.getenv("HF_TOKEN")

if not token:
    raise Exception("HF_TOKEN not found")

print("Token found!")

try:
    user = whoami(token)
    print("Connected to Hugging Face")
    print(user)
except Exception as e:
    print("Connection failed:", e)

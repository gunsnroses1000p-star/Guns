import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

prompt = "a futuristic sports car driving through a neon city at night, cinematic, photorealistic"

response = requests.post(
    API_URL,
    headers=headers,
    json={"inputs": prompt},
    timeout=120
)

print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
else:
    with open("output.png", "wb") as f:
        f.write(response.content)
    print("Image generated successfully: output.png")

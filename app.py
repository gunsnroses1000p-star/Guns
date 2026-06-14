image1_path = "in_painting_1781014281355.jpg"
image2_path = "Screenshot_20260614_025608_AIReel.jpg"
import os
import requests

HF_TOKEN = "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"

API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

prompt = ("a red sports car parked on a mountain road at sunset, photorealistic")

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

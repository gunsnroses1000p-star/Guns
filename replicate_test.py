import os
import replicate

api_token = os.environ.get("REPLICATE_API_TOKEN")

if not api_token:
    raise ValueError("Missing REPLICATE_API_TOKEN")

client = replicate.Client(api_token=api_token)

output = client.run(
    "stability-ai/stable-video-diffusion:3f0457b1e1d9a8f3e0f9",
    input={
        "input_image": "PASTE_YOUR_IMAGE_URL_HERE"
    }
)

print(output)

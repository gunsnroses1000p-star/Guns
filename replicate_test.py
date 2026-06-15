import os
import replicate

api_token = os.environ.get("REPLICATE_API_TOKEN")

if not api_token:
    raise ValueError("Missing REPLICATE_API_TOKEN")

client = replicate.Client(api_token=api_token)

output = client.run(
    "black-forest-labs/flux-kontext-pro",
    input={
        "input_image": "https://i.postimg.cc/pL3PfYcY/1781504506599.jpg",
        "prompt": "Create one seamless photorealistic image. Preserve all people and blend the scene naturally with realistic lighting, shadows, and color grading."
    }
)

print("========== OUTPUT ==========")
print(output)
print("============================")

import os
import replicate

api_token = os.environ.get("REPLICATE_API_TOKEN")

if not api_token:
    raise ValueError("Missing REPLICATE_API_TOKEN")

client = replicate.Client(api_token=api_token)

output = client.run(
    "black-forest-labs/flux-kontext-pro",
    input={
        "input_image": "https://i.postimg.cc/LXzwZjGj/1781503790820.jpg",
        "prompt": "Transform this side-by-side reference image into one seamless photorealistic portrait of two adults standing together in a modern indoor setting. Preserve their facial features, hairstyles, skin tones, clothing, and natural proportions. Match the lighting, shadows, camera angle, and color grading so it looks like one real photograph, not a collage."
    }
)

print("========== OUTPUT ==========")
print(output)
print("============================")

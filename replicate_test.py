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
        "prompt": "Create one seamless photorealistic image using both people from the reference image. Preserve both faces, hairstyles, skin tones, clothing, and body proportions. Place them naturally together in the same scene with matching lighting, shadows, camera angle, and color grading. Make it look like one real photograph, not a collage."
    }
)

print("========== OUTPUT ==========")
print(output)
print("============================")

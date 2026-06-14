import os
import requests
import fal_client

FAL_KEY = os.getenv("FAL_KEY")

if not FAL_KEY:
    raise ValueError("FAL_KEY secret is missing")

image_url = "https://i.postimg.cc/jdSN4Q39/merged-output.jpg"

prompt = """
Transform the reference image into a photorealistic nightclub scene.
Create one seamless image featuring both people from the reference image together in the same nightclub.
They are standing close together on a crowded dance floor, smiling and dancing naturally.
Use stylish nightlife clothing, purple and blue neon lights, disco lights, atmospheric haze, realistic shadows, matching lighting on both people, natural body proportions, cinematic photography, high detail.
"""

result = fal_client.subscribe(
    "fal-ai/flux-kontext/dev",
    arguments={
        "prompt": prompt,
        "image_url": image_url,
        "num_images": 1,
        "output_format": "jpeg",
        "acceleration": "regular"
    },
)

print("FAL result:")
print(result)

generated_url = result["images"][0]["url"]
print("Generated image URL:", generated_url)

response = requests.get(generated_url)
response.raise_for_status()

with open("nightclub_output.jpg", "wb") as f:
    f.write(response.content)

print("Saved nightclub_output.jpg")

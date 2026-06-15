import os
import replicate

api_token = os.environ.get("REPLICATE_API_TOKEN")

if not api_token:
    raise ValueError("Missing REPLICATE_API_TOKEN")

client = replicate.Client(api_token=api_token)

output = client.run(
    "wan-video/wan-2.2-i2v-fast",
    input={
        "image": "https://i.postimg.cc/cJ6gkHXs/in-painting-1781014281355.jpg",
        "prompt":  "Animate this image with subtle natural movement, realistic breathing, slight hair movement, soft cinematic camera push-in, smooth motion, realistic lighting, no distortion".
    }
)

print(output)
